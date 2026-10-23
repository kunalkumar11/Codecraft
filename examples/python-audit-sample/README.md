# Python audit sample

This deliberately unsafe, non-runnable sample demonstrates the static audit
rules. Do not execute `project/sample_app.py`; the calls are included so the
scanner can report them.

From the repository root:

```bash
python tools/codecraft_python_audit.py examples/python-audit-sample/project
python tools/codecraft_python_audit.py examples/python-audit-sample/project --format json --output audit-report.json
```

The sample reports high severity findings for `eval` and `subprocess` with
`shell=True`. With the default `--fail-on high`, the command returns exit code
1 when it finds them. The JSON output contains the rule, severity, source
location, message, and counts by severity.
