# Development

## Requirements

- Node.js 22 or newer, matching `.github/workflows/test.yml`.
- Python 3.10 or newer for the Hermes adapter, benchmark tools, audit utility, and Python tests. CI currently uses Python 3.12.
- Git for the documented `git grep` skill check and agentic benchmark snapshots. If Git is missing, one Node test reports a skip; Git is present in the verified environment.
- No npm packages or Python packages are required for the local unit suite.

## Checks

From the repository root:

```bash
npm test
node scripts/check-rule-copies.js
node scripts/check-versions.js
python benchmarks/agentic/run.py --selftest
python -m unittest discover -s tests -p "test_*.py" -v
```

`npm test` runs the Node test files and the Pi extension suite. The Python unittest command covers the source auditor and process-tree timeout helper. The Hermes tests launch Python with a small stub host API, so they verify registration and mode behavior without Hermes installed. On Windows PowerShell, run `npm.cmd test` if the `npm` shim is blocked by execution policy.

The benchmark correctness checks use Python's standard library and need no Pandas installation. A CSV answer that imports Pandas still requires Pandas in the interpreter selected by the harness; that optional dependency is not installed by this project. The benchmark executes supplied code locally; review that code before running it. The agentic self-test does not call a model or spend API credits. On Windows, timeout cleanup uses a Job Object and attempts `taskkill /T` for early descendants; restricted hosts may deny both process-tree mechanisms, in which case only the parent can be terminated.

The Python audit command is `python tools/codecraft_python_audit.py PATH`. Use `--format json --output report.json` for JSON export and `--fail-on medium` to make the process fail on medium or higher findings. It is a heuristic AST scanner, not a full taint analyzer or security boundary. The intentionally unsafe example at `examples/python-audit-sample/project` is for scanning only and must not be run.

The project's code is mainly JavaScript, with TypeScript/TSX for the task board and Python for the Hermes adapter, benchmarks, and audit utility. POSIX shell and PowerShell are used for status-line helpers. `AGENTS.md`, `skills/`, and host-specific mirrored files are agent instructions, not executable application modules. The `tests/hooks.test.js` smoke that invokes POSIX manifest commands runs only when `/bin/sh` exists; the Windows-specific hook contract has separate assertions. The checked-in `tests/band.test.tsx` imports `claude-code/testing`; the current Node test script does not discover it, and running it requires the Claude Code testing host/runtime.

No formatter or linter is configured in this checkout. The test workflow checks generated rule copies and manifest versions before running the tests.

## Host smoke test

Copy `AGENTS.md` into a disposable sample project and use an agent that reads it. For a plugin-based smoke test, install this checkout through the host's local-plugin workflow, start a new session, switch a mode with `/codecraft ultra`, and run `/codecraft-review` on a small diff. Confirm the host loads the local checkout rather than the published upstream plugin. This environment did not include those host applications, so that workflow remains to be run locally.

## Live benchmarks

Live agentic benchmarks require the Claude Code CLI, credentials, and API spend. They are intentionally separate from `--selftest`; use only a disposable worktree and review the benchmark's process and data handling before running a live matrix.

