import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "benchmarks" / "agentic"))

from process_tree import pid_running, run_captured, terminate_pid, wait_pid_exit


class AgenticProcessTreeTests(unittest.TestCase):
    def test_capture_returns_stdout_and_stderr(self):
        result = run_captured(
            [sys.executable, "-c", "import sys; print('out'); print('err', file=sys.stderr)"],
            text=True, timeout=5,
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.splitlines(), ["out"])
        self.assertEqual(result.stderr.splitlines(), ["err"])

    def test_timeout_terminates_process_with_a_child_holding_output_handles(self):
        with tempfile.TemporaryDirectory() as directory:
            pid_file = Path(directory) / "child.pid"
            child_code = "import time; time.sleep(30)"
            parent_code = (
                "import subprocess,sys,time\n"
                f"child=subprocess.Popen([sys.executable,'-c',{child_code!r}])\n"
                f"open({str(pid_file)!r},'w').write(str(child.pid))\n"
                "print('started', flush=True)\n"
                "time.sleep(30)\n"
            )
            with self.assertRaises(subprocess.TimeoutExpired) as raised:
                run_captured([sys.executable, "-c", parent_code], text=True, timeout=0.5)
            self.assertIn("started", raised.exception.output)
            self.assertTrue(pid_file.exists())
            child_pid = int(pid_file.read_text(encoding="utf-8"))
            try:
                exited = wait_pid_exit(child_pid, 3)
                self.assertIs(exited, True, f"timed-out child {child_pid} remained alive")
            finally:
                if pid_running(child_pid):
                    terminate_pid(child_pid)

    def test_completed_parent_does_not_leave_a_background_child(self):
        with tempfile.TemporaryDirectory() as directory:
            pid_file = Path(directory) / "child.pid"
            child_code = "import time; time.sleep(30)"
            parent_code = (
                "import subprocess,sys\n"
                f"child=subprocess.Popen([sys.executable,'-c',{child_code!r}])\n"
                f"open({str(pid_file)!r},'w').write(str(child.pid))\n"
            )
            result = run_captured([sys.executable, "-c", parent_code], text=True, timeout=5)
            self.assertEqual(result.returncode, 0)
            child_pid = int(pid_file.read_text(encoding="utf-8"))
            try:
                self.assertIs(wait_pid_exit(child_pid, 3), True,
                              f"completed checker left child {child_pid} alive")
            finally:
                if pid_running(child_pid):
                    terminate_pid(child_pid)


if __name__ == "__main__":
    unittest.main()
