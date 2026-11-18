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

        self.assertEqual(report["scanned_files"], 0)
        # May have multiple PY002 findings due to new scanner, check at least one
        py002_findings = [f for f in report["findings"] if f["rule_id"] == "PY002"]
        self.assertGreaterEqual(len(py002_findings), 1)
        self.assertEqual(py002_findings[0]["severity"], "medium")
        self.assertEqual(py002_findings[0]["path"], "blocked")

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
        self.assertEqual(report["schema_version"], 2)
        self.assertEqual(report["finding_count"], 1)
        self.assertEqual(report["findings"][0]["rule_id"], "PYSEC001")

    def test_reports_hardcoded_secrets_in_variable_names(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "secrets.py"
            source.write_text(
                "api_key = \"AKIAABCDEFGHIJKLMNOP\"\n"
                "github_token = \"ghp_abcdefghijklmnopqrstuvwxyz123456\"\n"
                "password = \"supersecret123\"\n"
                "secret_key = \"sk_test_abcdefghijklmnopqrstuvwxyz\"\n"
                "jwt_token = \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c\"\n",
                encoding="utf-8",
            )
            report = audit(directory)
        by_rule = {finding["rule_id"]: finding for finding in report["findings"]}
        # PYSEC005: hardcoded secret in variable assignment
        self.assertIn("PYSEC005", by_rule)
        # PYSEC006: secret patterns in tokens (strings/comments) - also catches AKIA, JWT, etc.
        self.assertIn("PYSEC006", by_rule)
        # 5 PYSEC005 (one per var) + PYSEC006 for each matched pattern (AKIA, ghp, sk_live, JWT)
        self.assertGreaterEqual(report["summary"]["high"], 7)

    def test_skips_fake_test_secrets(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "test_secrets.py"
            source.write_text(
                "test_api_key = \"test_fake_key_123\"\n"
                "dummy_password = \"placeholder_change_me\"\n"
                "example_token = \"your_token_here\"\n"
                "sk_test_fakekey123456789012345\n"
                "api_key = \"AKIAABCDEFGHIJKLMNOP\"  # only this one should be flagged\n",
                encoding="utf-8",
            )
            report = audit(directory)
        # Only real secret should be flagged: PYSEC005 for api_key + PYSEC006 for AKIA pattern
        rules = {f["rule_id"] for f in report["findings"]}
        self.assertEqual(rules, {"PYSEC005", "PYSEC006"})
        self.assertEqual(report["finding_count"], 2)

    def test_annotated_assignments_with_secrets(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "typed_secrets.py"
            source.write_text(
                "api_key: str = \"AKIAABCDEFGHIJKLMNOP\"\n"
                "password: str = \"test_fake_123\"  # fake, should be skipped\n"
                "normal_var: str = \"hello\"\n",
                encoding="utf-8",
            )
            report = audit(directory)
        # 2 findings: PYSEC005 for api_key var name + PYSEC006 for AKIA pattern in string
        rules = {f["rule_id"] for f in report["findings"]}
        self.assertEqual(rules, {"PYSEC005", "PYSEC006"})
        self.assertEqual(report["finding_count"], 2)
        self.assertIn("api_key", report["findings"][0]["message"])

    def test_all_files_flag_scans_env_json_yaml(self):
        """Test --all-files flag scans .env, .json, .yaml files."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            # Real secret formats that match our patterns
            # AWS secret key (base64 with +/=)
            (root / ".env").write_text("AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYREALKEY123\n", encoding="utf-8")
            # GitHub token: ghp_ + 36+ alphanumeric chars
            (root / "config.json").write_text('{"token": "ghp_abcdefghijklmnopqrstuvwxyz1234567890"}\n', encoding="utf-8")
            # High-entropy hex string (44+ chars) with secret context
            (root / "settings.yaml").write_text("api_key: a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f\n", encoding="utf-8")
            (root / "normal.txt").write_text("no secrets here\n", encoding="utf-8")
            # Default: should not scan non-Python files
            report_default = audit(root)
            # With --all-files: should scan all supported extensions
            report_all = audit(root, scan_all_files=True)

        # Default only scans Python files (none here), so 0 findings
        self.assertEqual(report_default["finding_count"], 0)
        # All files should find secrets in .env, .json, .yaml
        self.assertGreaterEqual(report_all["finding_count"], 3)
        rules = {f["rule_id"] for f in report_all["findings"]}
        self.assertIn("SEC001", rules)

    def test_git_history_flag_scans_commits(self):
        """Test --git-history flag (requires git repo)."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            # Initialize git repo
            subprocess.run(["git", "init"], cwd=root, capture_output=True, check=True)
            subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=root, capture_output=True, check=True)
            subprocess.run(["git", "config", "user.name", "Test"], cwd=root, capture_output=True, check=True)

            # Create a file with a secret and commit
            (root / "secrets.py").write_text('api_key = "AKIAABCDEFGHIJKLMNOP"\n', encoding="utf-8")
            subprocess.run(["git", "add", "secrets.py"], cwd=root, capture_output=True, check=True)
            subprocess.run(["git", "commit", "-m", "add secret"], cwd=root, capture_output=True, check=True)

            # Scan with git history
            report = audit(root, scan_git_history=True, git_history_depth=10)

        # Should find the secret in git history
        self.assertGreaterEqual(report.get("git_history_scanned", 0), 1)
        git_findings = [f for f in report["findings"] if f["rule_id"] == "GITSEC001"]
        self.assertGreaterEqual(len(git_findings), 1)


if __name__ == "__main__":
    unittest.main()
