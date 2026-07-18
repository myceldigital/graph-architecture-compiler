from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Any

SECRET_NAMES = {".env", ".npmrc", ".pypirc", "credentials.json", "secrets.yml", "secrets.yaml"}
SKIP_DIRS = {".git", "node_modules", "vendor", "dist", "build", ".venv", "venv", "__pycache__"}
LANGS = {
    ".py": "Python", ".go": "Go", ".rs": "Rust", ".ts": "TypeScript",
    ".tsx": "TypeScript/TSX", ".js": "JavaScript", ".jsx": "JavaScript/JSX",
    ".java": "Java", ".kt": "Kotlin", ".rb": "Ruby", ".php": "PHP",
    ".cs": "C#", ".swift": "Swift", ".sql": "SQL", ".tf": "Terraform",
}
MANIFESTS = {"pyproject.toml", "requirements.txt", "package.json", "go.mod", "Cargo.toml", "pom.xml", "build.gradle", "Dockerfile", "docker-compose.yml"}


def run_git(repo: Path, *args: str, check: bool = True) -> str:
    p = subprocess.run(["git", "-C", str(repo), *args], text=True, capture_output=True)
    if check and p.returncode:
        raise RuntimeError(p.stderr.strip() or "git command failed")
    return p.stdout.strip()


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def walk_files(root: Path):
    for base, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for name in sorted(files):
            path = Path(base) / name
            rel = path.relative_to(root)
            yield path, rel


def classify(rel: Path) -> set[str]:
    s = rel.as_posix().lower()
    name = rel.name
    tags: set[str] = set()
    if name in SECRET_NAMES or any(x in s for x in ("secret", "credential", "private_key")):
        tags.add("secret-indicator")
    if name in MANIFESTS or name.lower() in {x.lower() for x in MANIFESTS}:
        tags.add("manifest")
    if "test" in s or "spec" in s:
        tags.add("test")
    if s.startswith(".github/workflows/") or "ci" in s:
        tags.add("ci")
    if any(x in s for x in ("terraform", "infra/", "k8s", "helm", "docker")):
        tags.add("infrastructure")
    if name.lower() in {"agents.md", "claude.md"}:
        tags.add("agent-instruction")
    if rel.suffix.lower() in {".md", ".rst", ".adoc"}:
        tags.add("documentation")
    return tags


def inspect_repo(repo: Path, max_commits: int = 5000) -> dict[str, Any]:
    repo = repo.resolve()
    if not (repo / ".git").exists() and not run_git(repo, "rev-parse", "--git-dir", check=False):
        raise ValueError(f"not a Git repository: {repo}")
    files, languages, categories = [], {}, {}
    for path, rel in walk_files(repo):
        try:
            size = path.stat().st_size
        except OSError:
            continue
        tags = sorted(classify(rel))
        files.append({"path": rel.as_posix(), "size": size, "tags": tags})
        lang = LANGS.get(rel.suffix.lower())
        if lang:
            languages[lang] = languages.get(lang, 0) + 1
        for tag in tags:
            categories.setdefault(tag, []).append(rel.as_posix())
    shallow = run_git(repo, "rev-parse", "--is-shallow-repository", check=False) == "true"
    refs = run_git(repo, "for-each-ref", "--format=%(refname:short)", "refs/heads", "refs/remotes", "refs/tags", check=False).splitlines()
    log = run_git(repo, "log", "--all", f"--max-count={max_commits}", "--format=%H%x09%s", "--name-only", check=False)
    commits, current, changed, hotspots, pairs, reverts = [], None, [], {}, {}, []
    for line in log.splitlines() + [""]:
        if "\t" in line and len(line.split("\t", 1)[0]) >= 7:
            if current:
                commits.append({**current, "files": sorted(set(changed))})
                for f in set(changed): hotspots[f] = hotspots.get(f, 0) + 1
                unique = sorted(set(changed))[:80]
                for i, a in enumerate(unique):
                    for b in unique[i + 1:]: pairs[(a, b)] = pairs.get((a, b), 0) + 1
            sha, subject = line.split("\t", 1); current = {"sha": sha, "subject": subject}; changed = []
            if subject.lower().startswith(("revert", "rollback", "back out")): reverts.append({"sha": sha, "subject": subject})
        elif line.strip(): changed.append(line.strip())
    if current:
        commits.append({**current, "files": sorted(set(changed))})
        for f in set(changed): hotspots[f] = hotspots.get(f, 0) + 1
    return {
        "repository": str(repo), "head": run_git(repo, "rev-parse", "HEAD", check=False) or None,
        "branch": run_git(repo, "branch", "--show-current", check=False) or None,
        "dirty": bool(run_git(repo, "status", "--porcelain", check=False)), "shallow": shallow,
        "available_refs": refs, "history_limit": max_commits, "commits_analysed": len(commits),
        "history_complete_claimed": False, "languages": dict(sorted(languages.items())),
        "categories": {k: v for k, v in sorted(categories.items())}, "files": files,
        "history_hotspots": sorted(({"path": k, "commits": v} for k, v in hotspots.items()), key=lambda x: (-x["commits"], x["path"]))[:100],
        "cochange_signals": sorted(({"files": list(k), "commits": v} for k, v in pairs.items() if v > 1), key=lambda x: (-x["commits"], x["files"]))[:100],
        "revert_like_commits": reverts[:100],
        "limitations": (["repository is shallow"] if shallow else []) + ["co-change and churn are signals, not proof of intent or quality"],
    }
