#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import uuid
from pathlib import Path

from core import dump, load, sha256
from gac import render, validate_graph

ROOT = Path(__file__).resolve().parent
GRAPH = ROOT / "graph.json"
RUNS = ROOT / "runs"


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def graph() -> dict:
    return load(GRAPH)


def run_path(run_id: str) -> Path:
    return RUNS / f"{run_id}.json"


def start(mode: str, goal: str) -> None:
    g = graph()
    if mode not in g["entrypoints"]: raise SystemExit(f"unknown mode: {mode}")
    run_id = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    record = {"schema_version": "1.0", "run_id": run_id, "graph_id": g["id"], "graph_version": g["version"], "graph_hash": sha256(GRAPH), "mode": mode, "goal": goal, "status": "running", "started_at": now(), "updated_at": now(), "nodes": {}, "approvals": [], "failures": [], "result": None, "residual_risk": [], "unverified_assumptions": []}
    dump(run_path(run_id), record); print(run_id)


def update(run_id: str, node: str, status: str, evidence: list[str]) -> None:
    r = load(run_path(run_id)); g = graph(); ids = {n["id"] for n in g["nodes"]}
    if node not in ids: raise SystemExit(f"unknown node: {node}")
    r["nodes"][node] = {"status": status, "updated_at": now(), "evidence": evidence}
    r["updated_at"] = now(); dump(run_path(run_id), r)


def approve(run_id: str, node: str, decision: str, note: str) -> None:
    r = load(run_path(run_id)); r["approvals"].append({"node": node, "decision": decision, "note": note, "at": now()}); r["updated_at"] = now(); dump(run_path(run_id), r)


def finish(run_id: str, status: str, result: str) -> None:
    r = load(run_path(run_id)); r["status"] = status; r["result"] = result; r["updated_at"] = now(); dump(run_path(run_id), r)


def main() -> None:
    p = argparse.ArgumentParser(); sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate")
    s = sub.add_parser("render"); s.add_argument("--out", required=True)
    s = sub.add_parser("start"); s.add_argument("--mode", required=True); s.add_argument("--goal", required=True)
    s = sub.add_parser("update"); s.add_argument("--run", required=True); s.add_argument("--node", required=True); s.add_argument("--status", required=True); s.add_argument("--evidence", action="append", default=[])
    s = sub.add_parser("approve"); s.add_argument("--run", required=True); s.add_argument("--node", required=True); s.add_argument("--decision", required=True); s.add_argument("--note", default="")
    s = sub.add_parser("finish"); s.add_argument("--run", required=True); s.add_argument("--status", required=True); s.add_argument("--result", required=True)
    sub.add_parser("status")
    a = p.parse_args(); RUNS.mkdir(exist_ok=True)
    if a.cmd == "validate":
        errors = validate_graph(graph())
        if errors: raise SystemExit("\n".join(errors))
        print("graph valid")
    elif a.cmd == "render": Path(a.out).write_text(render(graph()), encoding="utf-8")
    elif a.cmd == "start": start(a.mode, a.goal)
    elif a.cmd == "update": update(a.run, a.node, a.status, a.evidence)
    elif a.cmd == "approve": approve(a.run, a.node, a.decision, a.note)
    elif a.cmd == "finish": finish(a.run, a.status, a.result)
    else:
        for path in sorted(RUNS.glob("*.json")): print(json.dumps(load(path), sort_keys=True))

if __name__ == "__main__": main()
