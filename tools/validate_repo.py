#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ["SKILL.md","README.md","agents/openai.yaml","scripts/gac.py","scripts/core.py","scripts/graphctl.py","references/OPERATING_MODEL.md","references/GRAPH_STANDARD.md","references/SECURITY.md","references/CODEX.md","references/EVIDENCE.md","references/EVALUATION.md","examples/graph.json","tests/test_system.py"]
errors=[]
for name in REQUIRED:
    if not (ROOT/name).is_file(): errors.append(f"missing {name}")
skill=(ROOT/"SKILL.md").read_text() if (ROOT/"SKILL.md").exists() else ""
if not skill.startswith("---\nname: graph-architecture-compiler\ndescription:"): errors.append("invalid SKILL.md frontmatter")
if skill.count("\n---\n") < 1: errors.append("unclosed SKILL.md frontmatter")
if len(skill.splitlines()) > 500: errors.append("SKILL.md exceeds 500 lines")
try: json.loads((ROOT/"examples/graph.json").read_text())
except Exception as exc: errors.append(f"invalid example JSON: {exc}")
for path in ROOT.rglob("*"):
    if path.is_file() and any(x in path.parts for x in ("__pycache__","dist",".git")): errors.append(f"transient file included: {path.relative_to(ROOT)}")
if errors:
    print("\n".join(errors),file=sys.stderr); raise SystemExit(1)
print(f"repository valid: {sum(1 for p in ROOT.rglob('*') if p.is_file())} files")
