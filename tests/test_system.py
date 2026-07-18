import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from core import inspect_repo
from gac import render, validate_graph

class SystemTests(unittest.TestCase):
    def setUp(self):
        self.graph = json.loads((ROOT / "examples/graph.json").read_text())

    def test_example_valid(self):
        self.assertEqual(validate_graph(self.graph), [])

    def test_loop_is_bounded(self):
        bad = json.loads(json.dumps(self.graph))
        edge = next(e for e in bad["edges"] if e.get("loop"))
        edge.pop("max_iterations")
        self.assertTrue(any("max_iterations" in e for e in validate_graph(bad)))

    def test_privilege_requires_approval(self):
        bad = json.loads(json.dumps(self.graph))
        n = next(n for n in bad["nodes"] if n["id"] == "implement")
        n["permissions"]["external_systems"] = ["deploy"]
        self.assertTrue(any("requires approval" in e for e in validate_graph(bad)))

    def test_render(self):
        text = render(self.graph)
        self.assertIn("flowchart TD", text)
        self.assertIn("max 2", text)

    def test_inspect_does_not_read_secret(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d); subprocess.run(["git","init",str(p)],check=True,capture_output=True)
            (p/".env").write_text("TOP_SECRET_VALUE")
            (p/"app.py").write_text("print('ok')")
            out = inspect_repo(p)
            raw = json.dumps(out)
            self.assertNotIn("TOP_SECRET_VALUE", raw)
            self.assertIn("secret-indicator", raw)

    def test_install_and_graphctl(self):
        with tempfile.TemporaryDirectory() as d:
            repo = Path(d)/"repo"; repo.mkdir(); subprocess.run(["git","init",str(repo)],check=True,capture_output=True)
            subprocess.run([sys.executable,str(ROOT/"scripts/gac.py"),"install","--repo",str(repo),"--graph",str(ROOT/"examples/graph.json"),"--goal",str(ROOT/"examples/goal.json"),"--policies",str(ROOT/"examples/policies.json")],check=True,capture_output=True)
            ctl=repo/".graph-architecture/graphctl.py"
            r=subprocess.run([sys.executable,str(ctl),"validate"],text=True,capture_output=True)
            self.assertEqual(r.returncode,0,r.stderr)
            self.assertIn("graph valid",r.stdout)

if __name__ == "__main__": unittest.main()
