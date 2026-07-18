#!/usr/bin/env python3
import argparse
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EXCLUDE={".git","dist","__pycache__",".venv"}
p=argparse.ArgumentParser(); p.add_argument("--out",default="dist/skill.zip"); a=p.parse_args()
out=(ROOT/a.out).resolve(); out.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED) as z:
    for f in sorted(ROOT.rglob("*")):
        if not f.is_file() or f==out or any(x in f.parts for x in EXCLUDE) or f.suffix==".pyc": continue
        z.write(f,Path("graph-architecture-compiler")/f.relative_to(ROOT))
if out.stat().st_size>25*1024*1024: raise SystemExit("skill.zip exceeds 25 MB")
print(out)
