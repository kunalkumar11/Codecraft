# CodeCraft

![CodeCraft mark](assets/codecraft-mark.svg)

**Practical engineering guidance and lifecycle tools for AI coding agents.**

CodeCraft is the name of this compatibility-preserving derivative of
[Ponytail](https://github.com/DietrichGebert/ponytail). It provides `/codecraft*`
commands and skills while retaining the old `/ponytail*` routes, environment
variables, and configuration paths for existing installs. Upstream origin and derived material are
recorded in [docs/ORIGIN.md](docs/ORIGIN.md).

## What it includes

- A shared coding-guidance skill with `lite`, `full`, `ultra`, and `off` modes.
- Host adapters and instruction files for Claude Code, Codex, Cursor, Gemini,
  Hermes, OpenCode, Pi, and other compatible agents.
- Review, audit, shortcut-debt, benchmark, and help commands under `/codecraft-*`.
- A local Claude Code task board with session metrics, search, CSV export, and
  optional webhook delivery.
- Correctness and agentic benchmark harnesses for checking behavior and safety.
- A read-only Python source auditor with structured findings and JSON export.

The task board stores its ledger under the user's configuration directory.
Webhook delivery is optional. The benchmark correctness harness executes code
from its input; it is **not a security sandbox**, so only evaluate answers you
trust.

## Set up and run

Requirements:

- Node.js 22 or newer (the repository CI target).
- Python 3.10 or newer for the Hermes adapter and Python checks.
- Git for the documented debt-scan command and agentic benchmark snapshots.
- No npm or pip dependencies are needed for the core test suite or Python auditor.

### Install from a checkout

This project is a set of agent instructions and host adapters, not a standalone
server or pip package. From a trusted source checkout, install the generic
instruction and skill files into the project you want an agent to work on.

PowerShell:

```powershell
$repo = 'C:\path\to\codecraft-main'
Copy-Item "$repo\AGENTS.md" '.\AGENTS.md'
New-Item -ItemType Directory -Force '.\.agents\skills' | Out-Null
Copy-Item -Path "$repo\skills\*" -Destination '.\.agents\skills' -Recurse
```

macOS/Linux:

```sh
REPO=/absolute/path/to/codecraft-main
cp "$REPO/AGENTS.md" ./AGENTS.md
mkdir -p .agents/skills
cp -R "$REPO/skills/." .agents/skills/
```

No `npm install` or `pip install` is required for this source-checkout setup.
For host-native plugin installation, see [INSTALL.md](INSTALL.md); its remote
marketplace commands currently install upstream Ponytail. This checkout has no
Git remote or published CodeCraft package URL, so it does not provide a
canonical public clone/install URL.

Run the checks from the repository root:

```bash
npm test
node scripts/check-rule-copies.js
node scripts/check-versions.js
python benchmarks/agentic/run.py --selftest
python -m unittest discover -s tests -p "test_*.py" -v
```

On Windows PowerShell, use `npm.cmd test` if the execution policy blocks the
`npm` PowerShell shim.

For a quick demonstration, copy `AGENTS.md` into a small sample project and ask
a compatible coding agent to make a focused change. Then try `/codecraft-review`
or `/codecraft-audit` if the host supports skills. For Hermes adapter behavior,
run `node --test tests/hermes-plugin.test.js`; it exercises the Python plugin
with a stub host context.

The Python source auditor is available as `python tools/codecraft_python_audit.py PATH`.
It reports common risky patterns without importing or executing scanned
code; add `--format json --output report.json` to export structured results.
The deliberately unsafe fixture and expected findings are documented in
[`examples/python-audit-sample/`](examples/python-audit-sample/README.md).

Example:

```text
HIGH     PYSEC001 sample_app.py:6:12 [security] eval executes dynamically constructed Python code
HIGH     PYSEC003 sample_app.py:10:12 [security] subprocess is configured with shell=True; review command construction
Scanned 1 Python file(s); 2 finding(s) (critical=0, high=2, medium=0, low=0, info=0).
```

The default `--fail-on high` makes that sample command exit with status 1.

## Commands and configuration

- `/codecraft lite|full|ultra|off` selects guidance intensity where the host supports persistent modes.
- `/codecraft-review`, `/codecraft-audit`, `/codecraft-debt`, `/codecraft-gain`, and `/codecraft-help` load the matching task skill.
- `/ponytail*` command names remain available as compatibility aliases.
- `CODECRAFT_DEFAULT_MODE` sets the default mode; the fallback is `full`. Existing `PONYTAIL_DEFAULT_MODE` remains accepted. It can also be set in `config.json` under `defaultMode`.
- `CODECRAFT_HIDE_STATUS=1` hides the Pi status indicator; `CODECRAFT_QUIET_STARTUP=1` hides its startup toast. The old `PONYTAIL_*` variables remain accepted. Both options also accept config-file booleans `hideStatus` and `quietStartup`.
- `CODECRAFT_SUBAGENT_MATCHER` scopes subagent instruction injection by a case-insensitive regular expression; unset means all subagents. The old variable remains accepted.
- `CODECRAFT_MAP=0` disables the optional code map; `CODECRAFT_MAP_CHARS` changes its character budget (default 2000). The old `PONYTAIL_MAP*` variables remain accepted.

Configuration still uses `~/.config/ponytail/config.json` on macOS/Linux and
`%APPDATA%\ponytail\config.json` on Windows so existing settings continue to
work. `XDG_CONFIG_HOME`, when set, overrides the base location on any platform.

The inherited host setup guide is [INSTALL.md](INSTALL.md). Its remote install
commands point to the original Ponytail repository. To load this local
derivative, use the host's local plugin workflow or copy its instruction and
skill files into a sample project. Host applications are not bundled here.

## Architecture

The prompt and host adapters are deliberately separate:

1. `skills/` holds the canonical instructions and task-specific skills.
2. `AGENTS.md` is the compact always-on form; generated host copies are checked
   by `scripts/check-rule-copies.js`.
3. `hooks/`, `__init__.py`, `pi-extension/`, and `.opencode/` adapt modes and
   commands to host lifecycle APIs.
4. `hooks/band/` builds the local task board from CSV ledgers.
5. `tests/` checks the adapters, installer scripts, and core behavior. The
   benchmark harnesses live in `benchmarks/`.
6. `tools/codecraft_python_audit.py` scans Python syntax trees for a small set
   of security and reliability patterns. It is separate from the host adapters
   and has no third-party dependencies.

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the data flow and trust
boundaries, and [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for development and
testing details.

## Known limits

- The checkout arrived without `.git`, so its commit history, branch, and
  working-tree state could not be inspected.
- The npm package name, author, and repository URL still identify the upstream owner.
  Do not publish CodeCraft under that package identity. A public CodeCraft release
  needs a maintainer-owned package name and repository metadata.
- The host applications are not installed here, so plugin activation and GUI
  workflows still need a smoke test in their actual hosts.
- The Windows process-tree self-test needs at least one allowed termination
  mechanism (`taskkill /T` or a Job Object); some locked-down hosts may deny both.
- The benchmark runs model-generated code as the current user and cannot
  isolate filesystem or network access.
- The Python auditor uses syntax-based heuristics. It cannot resolve aliases,
  understand runtime data flow, or prove that a finding is exploitable; it can
  also miss unsafe behavior outside its rules. Review findings in context.
- Existing translations and many host-specific instruction copies are inherited
  upstream material; see [docs/ORIGIN.md](docs/ORIGIN.md).

## Development and release

Contributing instructions are in [`.github/CONTRIBUTING.md`](.github/CONTRIBUTING.md).
The release history is in [CHANGELOG.md](CHANGELOG.md). The GitHub test workflow
is configured for Ubuntu, macOS, and Windows; this local checkout was exercised
on Windows, while actual hosted CI runs depend on a repository remote.

## License

The upstream MIT license and copyright notice are preserved in [LICENSE](LICENSE).
See [docs/ORIGIN.md](docs/ORIGIN.md) for attribution and the scope of the local
derivative.
