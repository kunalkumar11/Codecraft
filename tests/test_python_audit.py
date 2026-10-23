import json
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.codecraft_python_audit import audit


class PythonAuditTests(unittest.TestCase):
    def test_clean_project_skips_virtual_environments_and_generated_dirs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "app.py").write_text("def add(a, b):\n    return a + b\n", encoding="utf-8")
            (root / "node_modules").mkdir()
            (root / "node_modules" / "bad.py").write_text("eval('1')\n", encoding="utf-8")
            (root / ".venv").mkdir()
            (root / ".venv" / "bad.py").write_text("eval('1')\n", encoding="utf-8")
            report = audit(root)
        self.assertEqual(report["scanned_files"], 1)
        self.assertEqual(report["finding_count"], 0)
        self.assertEqual(report["summary"]["high"], 0)

    def test_reports_security_and_broad_exception_findings_with_locations(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "unsafe.py"
            source.write_text(
                "import os, pickle, subprocess\n"
                "subprocess.run(user_input, shell=True)\n"
                "os.system(user_input)\n"
                "pickle.loads(payload)\n"
                "eval(expression)\n"
                "try:\n    work()\nexcept Exception:\n    pass\n",
                encoding="utf-8",
            )
            report = audit(directory)
        by_rule = {finding["rule_id"]: finding for finding in report["findings"]}
        self.assertEqual(set(by_rule), {"PYSEC001", "PYSEC002", "PYSEC003", "PYSEC004", "PYREL002"})
        self.assertEqual(by_rule["PYSEC003"]["severity"], "high")
        self.assertEqual(by_rule["PYSEC003"]["line"], 2)
        self.assertEqual(by_rule["PYREL002"]["severity"], "medium")
        self.assertEqual(report["summary"]["high"], 4)

    def test_syntax_errors_are_structured_findings(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "broken.py").write_text("def broken(:\n", encoding="utf-8")
            report = audit(directory)
        finding, = report["findings"]
        self.assertEqual(finding["rule_id"], "PY001")
        self.assertEqual(finding["severity"], "high")
        self.assertEqual(finding["path"], "broken.py")

    def test_unreadable_directory_is_a_reported_incomplete_scan(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            blocked = root / "blocked"
            error = PermissionError("permission denied")
            error.filename = str(blocked)

            def fail_walk(_root, *, followlinks, onerror):
                self.assertFalse(followlinks)
                onerror(error)
                return iter(())

            with patch("tools.codecraft_python_audit.os.walk", side_effect=fail_walk):
                report = audit(root)

        finding, = report["findings"]
        self.assertEqual(report["scanned_files"], 0)
        self.assertEqual(finding["rule_id"], "PY002")
        self.assertEqual(finding["severity"], "medium")
        self.assertEqual(finding["path"], "blocked")

    def test_cli_exports_json_and_applies_fail_threshold(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "sample.py"
            project.write_text("eval('1')\n", encoding="utf-8")
            output = root / "report.json"
            result = subprocess.run(
                [sys.executable, str(ROOT / "tools" / "codecraft_python_audit.py"),
                 str(root), "--format", "json", "--output", str(output)],
                cwd=ROOT, capture_output=True, text=True, check=False,
            )
            report = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["schema_version"], 1)
        self.assertEqual(report["finding_count"], 1)
        self.assertEqual(report["findings"][0]["rule_id"], "PYSEC001")


if __name__ == "__main__":
    unittest.main()
