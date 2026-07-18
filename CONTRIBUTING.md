# Contributing

Improve correctness, evidence quality, security, least privilege, simplicity, Codex usability, portability, deterministic validation, empirical evaluation, or documentation. More agents or nodes are not inherently better.

Run:

```bash
python tools/validate_repo.py
python -m unittest discover -s tests -v
python scripts/gac.py validate --graph examples/graph.json
```

A pull request must explain the observed failure, why the change belongs in the reusable Skill, validation evidence, security and compatibility impact, and new assumptions. Keep runtime code standard-library-only unless a dependency has demonstrated indispensable value. Contributions are MIT licensed.
