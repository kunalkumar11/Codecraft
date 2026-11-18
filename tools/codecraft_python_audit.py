#!/usr/bin/env python3
"""Read-only, standard-library source checks for common risky patterns and secrets."""
from __future__ import annotations

import argparse
import ast
import json
import os
import re
import subprocess
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

# File extensions to scan for secrets (beyond Python)
SECRET_SCAN_EXTENSIONS = {
    ".py", ".env", ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf",
    ".config", ".properties", ".envrc", ".env.local", ".env.production",
    ".env.development", ".env.staging", ".env.test", ".tf", ".tfvars",
    ".npmrc", ".yarnrc", ".pypirc", ".dockercfg", ".dockerignore",
}

# Patterns that suggest a variable/key holds a secret
SECRET_VAR_PATTERNS = (
    "api_key", "apikey", "api_secret", "api_token",
    "access_token", "access_key", "secret_key", "secret_token",
    "password", "passwd", "passphrase", "pass_key",
    "private_key", "private_token", "client_secret", "client_id",
    "auth_token", "auth_key", "bearer_token", "refresh_token",
    "aws_access_key_id", "aws_secret_access_key", "aws_session_token",
    "github_token", "gitlab_token", "bitbucket_token",
    "slack_token", "slack_webhook", "discord_token", "discord_webhook",
    "stripe_key", "stripe_secret", "paypal_secret",
    "database_url", "db_password", "db_user", "db_pass",
    "redis_password", "redis_url",
    "jwt_secret", "jwt_key", "signing_key", "encryption_key",
    "master_key", "root_key", "admin_token", "service_account",
    "token", "secret", "credential", "auth", "key_id", "access_id",
)

# Regex patterns for common secret formats (high confidence)
SECRET_REGEX_PATTERNS = [
    (r"AKIA[0-9A-Z]{16}", "AWS access key ID"),
    # AWS secret keys are base64 with +/= chars; require at least one +/= to avoid git SHA false positives
    (r"(?=.*[+/=])[0-9a-zA-Z+/=]{40,}", "AWS secret access key"),
    (r"gh[pousr]_[0-9a-zA-Z]{36,}", "GitHub token"),
    (r"glpat-[0-9a-zA-Z\-_]{20,}", "GitLab personal access token"),
    (r"xox[baprs]-[0-9a-zA-Z\-]{10,}", "Slack token"),
    (r"sk_[a-zA-Z0-9]{24,}", "Stripe secret key"),
    (r"pk_[a-zA-Z0-9]{24,}", "Stripe publishable key"),
    (r"eyJ[A-Za-z0-9\-_=]+\.[A-Za-z0-9\-_=]+\.[A-Za-z0-9\-_=]+", "JWT token"),
    # Generic hex secrets - require word boundaries to avoid matching substrings of git SHAs
    (r"(?<![0-9a-f])[0-9a-f]{32}(?![0-9a-f])", "Generic 32-char hex secret"),
    (r"(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])", "Generic 64-char hex secret"),
]

# High-entropy patterns (base64, hex) - only flag if context suggests secret
# Note: 40-char hex = git commit SHA (common false positive in workflows)
# Using 44+ chars to reduce false positives while catching real secrets
HIGH_ENTROPY_PATTERNS = [
    (r"[A-Za-z0-9+/]{44,}={0,2}", "High-entropy base64 string"),
    (r"[0-9a-f]{44,}", "High-entropy hex string"),
]


@dataclass(frozen=True)
class Finding:
    rule_id: str
    severity: str
    category: str
    path: str
    line: int
    column: int
    message: str


class _PythonChecks(ast.NodeVisitor):
    """AST-based checks for Python files only."""

    def __init__(self, relative_path: str, source: str):
        self.path = relative_path
        self.source = source
        self.findings: list[Finding] = []

    def add(self, node: ast.AST, rule_id: str, severity: str, category: str, message: str) -> None:
        self.findings.append(Finding(
            rule_id, severity, category, self.path,
            getattr(node, "lineno", 1), getattr(node, "col_offset", 0) + 1, message,
        ))

    def add_at_line(self, line: int, column: int, rule_id: str, severity: str, category: str, message: str) -> None:
        self.findings.append(Finding(
            rule_id, severity, category, self.path, line, column, message,
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

    def _is_secret_var_name(self, name: str) -> bool:
        name_lower = name.lower()
        return any(pattern in name_lower for pattern in SECRET_VAR_PATTERNS)

    def _is_likely_fake_value(self, value: str) -> bool:
        """Filter out obvious test/fake/placeholder string values."""
        value_lower = value.lower()
        fake_indicators = (
            "test", "fake", "dummy", "placeholder", "example", "sample",
            "your_key", "your_secret", "your_token", "your_password",
            "change_me", "replace_me", "insert_here", "xxx", "yyy", "zzz",
            "sk_test_", "pk_test_", "sk_live_test", "pk_live_test",
        )
        return any(indicator in value_lower for indicator in fake_indicators)

    def visit_Assign(self, node: ast.Assign) -> None:
        for target in node.targets:
            if isinstance(target, ast.Name) and self._is_secret_var_name(target.id):
                if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                    value = node.value.value
                    if value.strip() and not self._is_likely_fake_value(value):
                        self.add(node, "PYSEC005", "high", "security",
                                 f"hardcoded secret in variable '{target.id}'; use environment variables or a secrets manager")
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        if isinstance(node.target, ast.Name) and self._is_secret_var_name(node.target.id):
            if node.value and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                value = node.value.value
                if value.strip() and not self._is_likely_fake_value(value):
                    self.add(node, "PYSEC005", "high", "security",
                             f"hardcoded secret in variable '{node.target.id}'; use environment variables or a secrets manager")
        self.generic_visit(node)

    def check_secrets_in_tokens(self) -> None:
        """Scan string literals and comments for secret patterns using tokenize."""
        try:
            tokens = tokenize.generate_tokens(iter(self.source.splitlines(keepends=True)).__next__)
            for tok in tokens:
                if tok.type in (tokenize.STRING, tokenize.COMMENT):
                    text = tok.string
                    line = tok.start[0]
                    col = tok.start[1] + 1
                    self._check_text_for_secrets(text, line, col)
        except (tokenize.TokenError, StopIteration, ValueError):
            pass  # Ignore tokenization errors

    def _check_text_for_secrets(self, text: str, line: int, col: int) -> None:
        """Check a text string for secret patterns."""
        # High-confidence patterns
        for pattern, desc in SECRET_REGEX_PATTERNS:
            if re.search(pattern, text):
                if self._is_likely_fake_secret(text):
                    continue
                self.add_at_line(line, col, "PYSEC006", "high", "security",
                                 f"potential {desc} in source; use environment variables or a secrets manager")

        # High-entropy patterns - only flag if near secret-like keywords
        for pattern, desc in HIGH_ENTROPY_PATTERNS:
            if re.search(pattern, text):
                if self._is_likely_fake_secret(text):
                    continue
                # Check if the line contains secret-indicating keywords
                if self._has_secret_context(text):
                    self.add_at_line(line, col, "PYSEC007", "medium", "security",
                                     f"high-entropy {desc.lower()} near secret context; verify if sensitive")

    def _is_likely_fake_secret(self, text: str) -> bool:
        """Filter out obvious test/fake/placeholder values."""
        text_lower = text.lower()
        fake_indicators = (
            "test", "fake", "dummy", "placeholder", "example", "sample",
            "your_key", "your_secret", "your_token", "your_password",
            "change_me", "replace_me", "insert_here", "xxx", "yyy", "zzz",
            "sk_test_", "pk_test_", "sk_live_test", "pk_live_test",
        )
        return any(indicator in text_lower for indicator in fake_indicators)

    def _has_secret_context(self, text: str) -> bool:
        """Check if text contains secret-indicating keywords."""
        text_lower = text.lower()
        context_keywords = (
            "key", "secret", "token", "password", "passwd", "credential",
            "auth", "api", "access", "private", "client", "bearer",
        )
        return any(kw in text_lower for kw in context_keywords)


class _GenericSecretScanner:
    """Line-by-line secret scanner for non-Python files."""

    def __init__(self, relative_path: str, source: str):
        self.path = relative_path
        self.source = source
        self.findings: list[Finding] = []

    def add_at_line(self, line: int, column: int, rule_id: str, severity: str, category: str, message: str) -> None:
        self.findings.append(Finding(
            rule_id, severity, category, self.path, line, column, message,
        ))

    def _is_likely_fake_secret(self, text: str) -> bool:
        text_lower = text.lower()
        # Only flag as fake if the ENTIRE matched string looks like a placeholder
        # Check for obvious placeholder patterns, not just keywords appearing in variable names
        fake_patterns = (
            "test", "fake", "dummy", "placeholder", "example", "sample",
            "your_key", "your_secret", "your_token", "your_password",
            "change_me", "replace_me", "insert_here", "xxx", "yyy", "zzz",
            "sk_test_", "pk_test_", "sk_live_test", "pk_live_test",
        )
        # Require the fake indicator to be a significant portion of the string
        # or appear in a clearly placeholder context
        for indicator in fake_patterns:
            if indicator in text_lower:
                # If the indicator is the whole value or a large prefix, it's fake
                # But don't flag just because "key" appears in "AWS_SECRET_ACCESS_KEY=..."
                if indicator in ("key", "secret", "token", "password", "auth", "api"):
                    continue  # These are too common in real secret variable names
                return True
        return False

    def _has_secret_context(self, text: str) -> bool:
        text_lower = text.lower()
        context_keywords = (
            "key", "secret", "token", "password", "passwd", "credential",
            "auth", "api", "access", "private", "client", "bearer",
            "aws", "github", "gitlab", "slack", "stripe", "jwt",
        )
        return any(kw in text_lower for kw in context_keywords)

    def scan(self) -> None:
        """Scan source line by line for secrets."""
        lines = self.source.splitlines()
        for i, line in enumerate(lines, 1):
            self._check_line(line, i)

    def _check_line(self, line: str, line_num: int) -> None:
        # High-confidence patterns
        for pattern, desc in SECRET_REGEX_PATTERNS:
            for match in re.finditer(pattern, line):
                if self._is_likely_fake_secret(match.group()):
                    continue
                col = match.start() + 1
                self.add_at_line(line_num, col, "SEC001", "high", "security",
                                 f"potential {desc} in {self.path}:{line_num}; use environment variables or a secrets manager")

        # High-entropy patterns with context
        for pattern, desc in HIGH_ENTROPY_PATTERNS:
            for match in re.finditer(pattern, line):
                if self._is_likely_fake_secret(match.group()):
                    continue
                # Only flag if line has secret context or key=value pattern
                if self._has_secret_context(line) or re.search(r"[\w\-]+\s*[:=]\s*\S+", line):
                    col = match.start() + 1
                    self.add_at_line(line_num, col, "SEC002", "medium", "security",
                                     f"high-entropy {desc.lower()} in {self.path}:{line_num}; verify if sensitive")


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


def _matches_secret_extension(path: Path) -> bool:
    """Check if file matches any secret scan extension (handles dotfiles like .env)."""
    name = path.name.lower()
    # Check full filename matches (for dotfiles like .env, .envrc, .npmrc)
    if name in SECRET_SCAN_EXTENSIONS:
        return True
    # Check suffix matches (for .json, .yaml, etc.)
    if path.suffix.lower() in SECRET_SCAN_EXTENSIONS:
        return True
    # Check for compound extensions like .env.local, .env.production
    for ext in SECRET_SCAN_EXTENSIONS:
        if ext.startswith(".") and name.endswith(ext):
            return True
    return False


def _secret_scan_files(root: Path, *, onerror=None):
    """Yield files with extensions in SECRET_SCAN_EXTENSIONS (including .py)."""
    if root.is_file():
        if _matches_secret_extension(root) and not root.is_symlink():
            yield root
        return
    for current, directories, filenames in os.walk(root, followlinks=False, onerror=onerror):
        directories[:] = sorted(
            name for name in directories
            if name not in SKIP_DIRS and not (Path(current) / name).is_symlink()
        )
        for filename in sorted(filenames):
            candidate = Path(current) / filename
            if _matches_secret_extension(candidate) and not candidate.is_symlink():
                yield candidate


def _get_git_files(root: Path) -> set[str]:
    """Get list of files tracked by git in the repository."""
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=root, capture_output=True, text=True, check=False
        )
        if result.returncode == 0:
            return set(result.stdout.strip().splitlines())
    except (subprocess.SubprocessError, OSError):
        pass
    return set()


def _scan_git_history(root: Path, max_commits: int = 100) -> dict:
    """Scan git history for secrets in commits."""
    findings: list[Finding] = []
    try:
        # Get commit hashes
        result = subprocess.run(
            ["git", "log", "--oneline", "-n", str(max_commits)],
            cwd=root, capture_output=True, text=True, check=False
        )
        if result.returncode != 0:
            return {"scanned_commits": 0, "findings": []}

        commits = [line.split()[0] for line in result.stdout.strip().splitlines() if line]
        scanned = 0

        for commit_hash in commits:
            # Get diff for this commit
            diff_result = subprocess.run(
                ["git", "show", "--no-merges", "--patch", commit_hash],
                cwd=root, capture_output=True, text=True, check=False
            )
            if diff_result.returncode != 0:
                continue

            scanned += 1
            diff_text = diff_result.stdout
            # Scan added lines (lines starting with +)
            for line in diff_text.splitlines():
                if line.startswith("+++") or line.startswith("---"):
                    continue
                if line.startswith("+"):
                    content = line[1:]
                    # Check for secrets in added content
                    for pattern, desc in SECRET_REGEX_PATTERNS:
                        if re.search(pattern, content):
                            if not _is_likely_fake_git_secret(content):
                                findings.append(Finding(
                                    "GITSEC001", "high", "security",
                                    f"git:{commit_hash[:8]}", 0, 0,
                                    f"potential {desc} added in commit {commit_hash[:8]}; rotate if exposed"
                                ))
    except (subprocess.SubprocessError, OSError):
        pass

    return {"scanned_commits": scanned, "findings": findings}


def _is_likely_fake_git_secret(text: str) -> bool:
    text_lower = text.lower()
    fake_indicators = (
        "test", "fake", "dummy", "placeholder", "example", "sample",
        "your_key", "your_secret", "your_token", "your_password",
        "change_me", "replace_me", "insert_here", "xxx", "yyy", "zzz",
        "sk_test_", "pk_test_", "sk_live_test", "pk_live_test",
    )
    return any(indicator in text_lower for indicator in fake_indicators)


def audit(root: str | Path, *, scan_secrets: bool = True, scan_git_history: bool = False,
          git_history_depth: int = 100, scan_all_files: bool = False) -> dict:
    """Scan a file or directory and return a stable structured report."""
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

    # 1. Python-specific AST checks (always run for .py files)
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
        checks = _PythonChecks(relative, source)
        checks.visit(tree)
        if scan_secrets:
            checks.check_secrets_in_tokens()
        findings.extend(checks.findings)

    # 2. Generic secret scanning (all supported file types) - opt-in
    if scan_secrets and scan_all_files:
        for source_path in _secret_scan_files(target, onerror=record_walk_error):
            # Skip .py files already scanned above (but still scan them for line-based secrets)
            relative = source_path.relative_to(base).as_posix()
            if relative.endswith(".py"):
                continue  # Already scanned with AST checks
            try:
                with open(source_path, "r", encoding="utf-8", errors="ignore") as f:
                    source = f.read()
            except (OSError, UnicodeError):
                continue
            scanner = _GenericSecretScanner(relative, source)
            scanner.scan()
            findings.extend(scanner.findings)

    # 3. Git history scanning - opt-in
    if scan_git_history and base.is_dir():
        git_result = _scan_git_history(base, git_history_depth)
        findings.extend(git_result["findings"])

    findings.sort(key=lambda item: (item.path, item.line, item.column, item.rule_id))
    counts = {severity: 0 for severity in SEVERITIES}
    for finding in findings:
        counts[finding.severity] += 1

    result = {
        "schema_version": 2,
        "root": str(target),
        "scanned_files": scanned_files,
        "finding_count": len(findings),
        "summary": counts,
        "findings": [asdict(finding) for finding in findings],
    }

    if scan_git_history:
        result["git_history_scanned"] = git_result.get("scanned_commits", 0)

    return result


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
    scanned = report.get("scanned_files", 0)
    lines.append(f"Scanned {scanned} Python file(s); {report['finding_count']} finding(s) ({counts}).")
    if "git_history_scanned" in report:
        lines.append(f"Git history: {report['git_history_scanned']} commits scanned.")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=".", help="File or project directory (default: .)")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--output", help="write the selected report format to this file")
    parser.add_argument("--fail-on", choices=("none", *SEVERITIES), default="high",
                        help="exit 1 when this severity or a more severe finding is present (default: high)")
    parser.add_argument("--no-secrets", action="store_true", help="disable secret scanning in Python files")
    parser.add_argument("--all-files", action="store_true", help="scan all supported file types (.env, .json, .yaml, etc.)")
    parser.add_argument("--git-history", action="store_true", help="scan git commit history for secrets")
    parser.add_argument("--git-depth", type=int, default=100, help="max commits to scan in git history (default: 100)")
    args = parser.parse_args(argv)

    try:
        report = audit(args.path, scan_secrets=not args.no_secrets,
                       scan_git_history=args.git_history, git_history_depth=args.git_depth,
                       scan_all_files=args.all_files)
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