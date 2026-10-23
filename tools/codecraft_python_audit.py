#!/usr/bin/env python3
"""Read-only, standard-library Python source checks for common risky patterns."""
from __future__ import annotations

import argparse
import ast
import json
import os
import sys
import tokenize
from dataclasses import asdict, dataclass
from pathlib import Path

SEVERITIES = ("critical", "high", "medium", "low", "info")
SEVERITY_RANK = {severity: index for index, severity in enumerate(SEVERITIES)}
SKIP_DIRS = {
    ".git", ".hg", ".svn", ".venv", "venv", "env", "node_modules", "__pycache__",
    ".tox", ".mypy_cache", ".pytest_cache", ".ruff_cache", "build", "dist",
}


@dataclass(frozen=True)
class Finding:
    rule_id: str
    severity: str
    category: str
    path: str
    line: int
    column: int
    message: str


class _Checks(ast.NodeVisitor):
    def __init__(self, relative_path: str):
        self.path = relative_path
        self.findings: list[Finding] = []

    def add(self, node: ast.AST, rule_id: str, severity: str, category: str, message: str) -> None:
        self.findings.append(Finding(
            rule_id, severity, category, self.path,
            getattr(node, "lineno", 1), getattr(node, "col_offset", 0) + 1, message,
        ))

    def visit_Call(self, node: ast.Call) -> None:
        func = node.func
        if isinstance(func, ast.Name) and func.id in {"eval", "exec"}:
            self.add(node, "PYSEC001", "high", "security",
                     f"{func.id} executes dynamically constructed Python code")
        if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
            module, name = func.value.id, func.attr
            if module == "os" and name == "system":
                self.add(node, "PYSEC002", "high", "security",
                         "os.system invokes a command through the platform shell")
            elif module == "subprocess" and name in {"run", "Popen", "call", "check_call", "check_output"}:
                if any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant)
                       and keyword.value.value is True for keyword in node.keywords):
                    self.add(node, "PYSEC003", "high", "security",
                             "subprocess is configured with shell=True; review command construction")
            elif module == "pickle" and name in {"load", "loads"}:
                self.add(node, "PYSEC004", "high", "security",
                         "pickle deserialization can execute code from untrusted input")
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        if node.type is None:
            self.add(node, "PYREL001", "medium", "reliability",
                     "bare except catches system-exiting exceptions; catch a specific error")
        elif isinstance(node.type, ast.Name) and node.type.id in {"Exception", "BaseException"}:
            self.add(node, "PYREL002", "medium", "reliability",
                     f"broad {node.type.id} handler may hide unrelated failures")
        self.generic_visit(node)


def _python_files(root: Path, *, onerror=None):
    if root.is_file():
        if root.suffix.lower() == ".py" and not root.is_symlink():
            yield root
        return
    for current, directories, filenames in os.walk(root, followlinks=False, onerror=onerror):
        directories[:] = sorted(
            name for name in directories
            if name not in SKIP_DIRS and not (Path(current) / name).is_symlink()
        )
        for filename in sorted(filenames):
            candidate = Path(current) / filename
            if candidate.suffix.lower() == ".py" and not candidate.is_symlink():
                yield candidate


def audit(root: str | Path) -> dict:
    """Scan a Python file or directory and return a stable structured report."""
    target = Path(root).expanduser().resolve()
    if not target.exists():
        raise FileNotFoundError(f"path does not exist: {target}")
    if not target.is_dir() and not target.is_file():
        raise ValueError(f"not a file or directory: {target}")

    findings: list[Finding] = []
    scanned_files = 0
    base = target if target.is_dir() else target.parent

    def record_walk_error(error: OSError) -> None:
        failed_path = Path(error.filename) if error.filename else target
        try:
            relative = failed_path.relative_to(base).as_posix()
        except ValueError:
            relative = failed_path.name or "."
        findings.append(Finding("PY002", "medium", "correctness", relative, 1, 1,
                                f"could not scan directory: {error.strerror or error}"))

    for source_path in _python_files(target, onerror=record_walk_error):
        scanned_files += 1
        relative = source_path.relative_to(base).as_posix()
        try:
            with tokenize.open(source_path) as source_file:
                source = source_file.read()
            tree = ast.parse(source, filename=relative)
        except (OSError, UnicodeError) as error:
            findings.append(Finding("PY001", "medium", "correctness", relative, 1, 1,
                                    f"could not read Python source: {error}"))
            continue
        except SyntaxError as error:
            findings.append(Finding("PY001", "high", "correctness", relative,
                                    error.lineno or 1, error.offset or 1,
                                    f"Python syntax error: {error.msg}"))
            continue
        checks = _Checks(relative)
        checks.visit(tree)
        findings.extend(checks.findings)

    findings.sort(key=lambda item: (item.path, item.line, item.column, item.rule_id))
    counts = {severity: 0 for severity in SEVERITIES}
    for finding in findings:
        counts[finding.severity] += 1
    return {
        "schema_version": 1,
        "root": str(target),
        "scanned_files": scanned_files,
        "finding_count": len(findings),
        "summary": counts,
        "findings": [asdict(finding) for finding in findings],
    }


def _text_report(report: dict) -> str:
    if not report["findings"]:
        lines = ["No findings."]
    else:
        lines = [
            f"{item['severity'].upper():8} {item['rule_id']} {item['path']}:{item['line']}:{item['column']} "
            f"[{item['category']}] {item['message']}"
            for item in report["findings"]
        ]
    counts = ", ".join(f"{severity}={report['summary'][severity]}" for severity in SEVERITIES)
    lines.append(f"Scanned {report['scanned_files']} Python file(s); {report['finding_count']} finding(s) ({counts}).")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=".", help="Python file or project directory (default: .)")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--output", help="write the selected report format to this file")
    parser.add_argument("--fail-on", choices=("none", *SEVERITIES), default="high",
                        help="exit 1 when this severity or a more severe finding is present (default: high)")
    args = parser.parse_args(argv)
    try:
        report = audit(args.path)
        output = (json.dumps(report, indent=2, ensure_ascii=False) + "\n"
                  if args.format == "json" else _text_report(report))
        if args.output:
            Path(args.output).expanduser().write_text(output, encoding="utf-8")
            print(f"Wrote {args.format} report to {Path(args.output).expanduser()}", file=sys.stderr)
        else:
            sys.stdout.write(output)
    except (OSError, ValueError) as error:
        print(f"python-audit: {error}", file=sys.stderr)
        return 2

    threshold = SEVERITY_RANK.get(args.fail_on)
    if threshold is not None and any(SEVERITY_RANK[item["severity"]] <= threshold
                                     for item in report["findings"]):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
