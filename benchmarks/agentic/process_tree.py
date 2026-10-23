"""Process-tree helpers shared by the agentic benchmark and its task scorers."""
import os
import signal
import subprocess
import sys
import tempfile
import time


def _windows_job(proc):
    """Attach the process to a kill-on-close Job Object so later children inherit it."""
    if os.name != "nt":
        return None, None
    import ctypes
    from ctypes import wintypes

    class BasicLimitInformation(ctypes.Structure):
        _fields_ = [
            ("PerProcessUserTimeLimit", ctypes.c_longlong),
            ("PerJobUserTimeLimit", ctypes.c_longlong),
            ("LimitFlags", wintypes.DWORD),
            ("MinimumWorkingSetSize", ctypes.c_size_t),
            ("MaximumWorkingSetSize", ctypes.c_size_t),
            ("ActiveProcessLimit", wintypes.DWORD),
            ("Affinity", ctypes.c_size_t),
            ("PriorityClass", wintypes.DWORD),
            ("SchedulingClass", wintypes.DWORD),
        ]

    class IoCounters(ctypes.Structure):
        _fields_ = [(name, ctypes.c_ulonglong) for name in (
            "ReadOperationCount", "WriteOperationCount", "OtherOperationCount",
            "ReadTransferCount", "WriteTransferCount", "OtherTransferCount")]

    class ExtendedLimitInformation(ctypes.Structure):
        _fields_ = [
            ("BasicLimitInformation", BasicLimitInformation),
            ("IoInfo", IoCounters),
            ("ProcessMemoryLimit", ctypes.c_size_t),
            ("JobMemoryLimit", ctypes.c_size_t),
            ("PeakProcessMemoryUsed", ctypes.c_size_t),
            ("PeakJobMemoryUsed", ctypes.c_size_t),
        ]

    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
    kernel.CreateJobObjectW.restype = wintypes.HANDLE
    kernel.SetInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
    kernel.SetInformationJobObject.restype = wintypes.BOOL
    kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    kernel.OpenProcess.restype = wintypes.HANDLE
    kernel.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
    kernel.AssignProcessToJobObject.restype = wintypes.BOOL
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel.CloseHandle.restype = wintypes.BOOL

    job = kernel.CreateJobObjectW(None, None)
    if not job:
        return None, f"CreateJobObjectW failed ({ctypes.get_last_error()})"
    limits = ExtendedLimitInformation()
    limits.BasicLimitInformation.LimitFlags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
    if not kernel.SetInformationJobObject(job, 9, ctypes.byref(limits), ctypes.sizeof(limits)):
        error = ctypes.get_last_error()
        kernel.CloseHandle(job)
        return None, f"SetInformationJobObject failed ({error})"
    process = kernel.OpenProcess(0x0101, False, proc.pid)  # PROCESS_SET_QUOTA | PROCESS_TERMINATE
    if not process:
        error = ctypes.get_last_error()
        kernel.CloseHandle(job)
        return None, f"OpenProcess failed ({error})"
    assigned = kernel.AssignProcessToJobObject(job, process)
    error = ctypes.get_last_error() if not assigned else 0
    kernel.CloseHandle(process)
    if not assigned:
        kernel.CloseHandle(job)
        return None, f"AssignProcessToJobObject failed ({error})"
    return job, None


def close_windows_job(job):
    if not job or os.name != "nt":
        return False
    import ctypes
    from ctypes import wintypes
    close = ctypes.WinDLL("kernel32", use_last_error=True).CloseHandle
    close.argtypes = [wintypes.HANDLE]
    close.restype = wintypes.BOOL
    return bool(close(job))


def spawn_process_tree(args, **kwargs):
    """Start a process in its own POSIX group or a Windows Job Object when permitted."""
    proc = subprocess.Popen(args, start_new_session=(os.name != "nt"), **kwargs)
    job, error = _windows_job(proc)
    return proc, job, error


def terminate_process_tree(proc, job=None, job_error=None):
    """Kill only this process tree and report if the host allowed only a parent kill."""
    if os.name == "nt":
        try:
            result = subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                                    capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                close_windows_job(job)
                return "taskkill /T"
            reason = result.stderr.strip() or result.stdout.strip() or f"taskkill exit {result.returncode}"
        except (OSError, subprocess.TimeoutExpired) as error:
            reason = str(error)
        if job and close_windows_job(job):
            return "Windows Job Object"
        try:
            proc.kill()
        except ProcessLookupError:
            pass
        return f"parent-only: {job_error + '; ' if job_error else ''}{reason}"
    try:
        # start_new_session=True makes the child PID the process-group ID. Use
        # it directly: after wait() reaps the group leader, os.getpgid(pid)
        # fails even if descendants are still holding the group open.
        os.killpg(proc.pid, signal.SIGKILL)
        return "POSIX process group"
    except ProcessLookupError:
        return "process group already exited"
    except OSError as error:
        try:
            proc.kill()
        except ProcessLookupError:
            pass
        return f"parent-only: {error}"


def cleanup_process_tree(proc, job=None):
    """Close a Windows job or kill any descendants left after a command exits."""
    if os.name == "nt":
        close_windows_job(job)
        return
    try:
        # The leader may already have exited while background descendants live.
        os.killpg(proc.pid, signal.SIGKILL)
    except OSError:
        pass


def _read_output(stream, text, encoding, errors):
    stream.seek(0)
    data = stream.read()
    return data.decode(encoding, errors) if text else data


def run_captured(args, *, cwd=None, env=None, timeout=None, text=False, encoding=None, errors=None):
    """Capture output without pipes, and terminate descendants when a timeout expires."""
    with tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
        proc, job, job_error = spawn_process_tree(args, cwd=cwd, env=env, stdout=stdout, stderr=stderr)
        try:
            try:
                proc.wait(timeout=timeout)
            except subprocess.TimeoutExpired as expired:
                terminate_process_tree(proc, job, job_error)
                job = None
                try:
                    proc.wait(timeout=15)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait()
                out = _read_output(stdout, text, encoding or "utf-8", errors or "strict")
                err = _read_output(stderr, text, encoding or "utf-8", errors or "strict")
                raise subprocess.TimeoutExpired(args, timeout, output=out, stderr=err) from expired
            cleanup_process_tree(proc, job)
            job = None
            out = _read_output(stdout, text, encoding or "utf-8", errors or "strict")
            err = _read_output(stderr, text, encoding or "utf-8", errors or "strict")
            return subprocess.CompletedProcess(args, proc.returncode, out, err)
        finally:
            if proc is not None:
                cleanup_process_tree(proc, job)


def pid_running(pid):
    if os.name == "nt":
        import ctypes
        from ctypes import wintypes
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        kernel.OpenProcess.restype = wintypes.HANDLE
        kernel.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
        kernel.WaitForSingleObject.restype = wintypes.DWORD
        kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        handle = kernel.OpenProcess(0x00100000, False, pid)  # SYNCHRONIZE
        if not handle:
            return None if ctypes.get_last_error() == 5 else False
        try:
            result = kernel.WaitForSingleObject(handle, 0)
            if result == 0x00000102:  # WAIT_TIMEOUT
                return True
            if result == 0:
                return False
            return None  # WAIT_FAILED or an unexpected status is unverifiable.
        finally:
            kernel.CloseHandle(handle)
    try:
        os.kill(pid, 0)
        if sys.platform.startswith("linux"):
            from pathlib import Path
            stat = Path(f"/proc/{pid}/stat")
            if stat.exists() and stat.read_text().split(") ", 1)[-1].startswith("Z "):
                return False
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True

def wait_pid_exit(pid, timeout):
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        state = pid_running(pid)
        if state is False:
            return True
        if state is None:
            return None
        time.sleep(0.05)
    state = pid_running(pid)
    return None if state is None else not state


def terminate_pid(pid):
    if os.name == "nt":
        import ctypes
        from ctypes import wintypes
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        kernel.OpenProcess.restype = wintypes.HANDLE
        kernel.TerminateProcess.argtypes = [wintypes.HANDLE, wintypes.UINT]
        kernel.TerminateProcess.restype = wintypes.BOOL
        kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        handle = kernel.OpenProcess(0x0001, False, pid)  # PROCESS_TERMINATE
        if not handle:
            return False
        try:
            return bool(kernel.TerminateProcess(handle, 1))
        finally:
            kernel.CloseHandle(handle)
    try:
        os.kill(pid, signal.SIGKILL)
        return True
    except ProcessLookupError:
        return True
    except OSError:
        return False
