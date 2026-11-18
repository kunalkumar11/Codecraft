<p align="center">
  <img src="assets/codecraft-mark.svg" alt="CodeCraft" width="128" height="128">
</p>

<h1 align="center">CodeCraft</h1>

<p align="center">
  <strong>The lazy senior dev mindset — packaged for AI coding agents. The best code is the code never written.</strong>
</p>

<p align="center">
  <a href="https://github.com/kunalkumar11/Codecraft/actions"><img alt="Tests" src="https://img.shields.io/github/actions/workflow/status/kunalkumar11/Codecraft/test.yml?label=tests&logo=github"></a>
  <a href="https://github.com/kunalkumar11/Codecraft/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/kunalkumar11/Codecraft?color=0A7"></a>
  <a href="https://nodejs.org/"><img alt="Node" src="https://img.shields.io/badge/node-%3E%3D22-339933?logo=node.js"></a>
  <a href="https://github.com/kunalkumar11/Codecraft/issues"><img alt="Issues" src="https://img.shields.io/github/issues/kunalkumar11/Codecraft?color=E03"></a>
</p>

---

## 🎯 What is CodeCraft?

CodeCraft is a set of commands and skills that teach your AI coding assistant to work like a **lazy senior developer** — meaning: solve the whole problem with the least new code, no fluff, no over-engineering.

| Command | What it does |
|---------|--------------|
| `/codecraft-help` | Show this reference card |
| `/codecraft` | Show current mode (lite/full/ultra/off) |
| `/codecraft lite\|full\|ultra\|off` | Switch modes — from minimal to "question everything" |
| `/codecraft-review` | Review a code change for bugs, security, bloat, missing tests |
| `/codecraft-audit` | Audit entire repo, ranked by severity |
| `/codecraft-debt` | Find all `shortcut:` comments in your codebase |
| `/codecraft-gain` | Show benchmarks: less code, fewer tokens, less cost, faster |
| **Python Audit** | `python tools/codecraft_python_audit.py` — finds secrets & risky patterns |

---

## 🚀 Install in 30 Seconds (Easiest Way)

**You don't need to clone anything. Just run one file:**

```bash
# Linux / macOS / Git Bash:
curl -fsSL https://raw.githubusercontent.com/kunalkumar11/Codecraft/main/codecraft-install.js > codecraft-install.js && node codecraft-install.js

# Windows PowerShell:
irm https://raw.githubusercontent.com/kunalkumar11/Codecraft/main/codecraft-install.js | Out-File codecraft-install.js; node codecraft-install.js
```

That's it. The installer:
1. **Detects your AI agents** (Claude Code, Codex, Cursor, Grok, Gemini, Kimi, Qoder, OpenCode, Hermes)
2. **Downloads CodeCraft automatically** from GitHub
3. **Installs everything** — commands, skills, hooks, configs — for each agent it finds
4. **Tells you exactly what was installed where**

Then **restart your AI agent** and type:
```
/codecraft-help
```

> 💡 **Share with any AI agent** — just give them `codecraft-install.js` and say "run this with Node.js". Works completely standalone.

---

## 📦 Traditional Way (Clone + npm)

If you prefer to clone and build yourself:

```bash
git clone https://github.com/kunalkumar11/Codecraft.git
cd Codecraft
npm install
npm run setup
npm test   # should show 168 passing
```

**Requirements:** Node.js 22+, Python 3.10+, Git

---

## 🎮 How to Use (Inside Your AI Agent)

**Important:** These commands run **inside your AI coding assistant**, not in your terminal.

| Your AI Agent | How to Start |
|---------------|--------------|
| **Claude Code** (VS Code extension or CLI) | Open Claude Code → type `/codecraft-help` |
| **Cursor** | Open Cursor chat → type `/codecraft-help` |
| **Codex CLI** | Run `codex` → type `/codecraft-help` |
| **OpenCode** | Run `opencode` → type `/codecraft-help` |
| **Gemini CLI** | Run `gemini` → type `/codecraft-help` |
| **Grok Build** | Run `grok` → type `/codecraft-help` |
| **Kimi Code** | Run `kimi` → type `/codecraft-help` |
| **Qoder** | Run `qoder` → type `/codecraft-help` |
| **Continue.dev** | Open Continue chat → type `/codecraft-help` |

### Quick Commands Cheat Sheet

```bash
# Mode commands (use SPACE)
/codecraft-help      # Show all commands
/codecraft           # Show current mode
/codecraft lite      # Minimal — just the essentials
/codecraft full      # Default — balanced
/codecraft ultra     # Maximum — questions every request
/codecraft off       # Disable CodeCraft

# Skill commands (use DASH)
/codecraft-review    # Review a diff/PR
/codecraft-audit     # Audit whole repo
/codecraft-debt      # List all shortcut: comments
/codecraft-gain      # Show benchmark scoreboard
```

> **Tip:** Mode = space (`/codecraft ultra`), Skill = dash (`/codecraft-audit`)

---

## 🔍 Python Audit Tool — Find Secrets & Bugs

CodeCraft includes a **standalone Python script** that scans your code for:
- **Hardcoded secrets** — API keys, tokens, passwords in variables
- **Secret patterns** — AWS keys, GitHub tokens, GitLab PATs, Slack, Stripe, JWT
- **Risky code** — `eval`/`exec`, `os.system`, `shell=True`, `pickle.loads`
- **Broad exception handlers** — `except:` that hide real bugs

### Run It (No Install Needed — Just Python)

```bash
# Scan a Python project (secret detection ON by default)
python tools/codecraft_python_audit.py /path/to/your/project

# Scan ALL config files too (.env, .json, .yaml, .toml, .ini, .tf, .npmrc, etc.)
python tools/codecraft_python_audit.py . --all-files

# Scan git history for leaked secrets (last 50 commits)
python tools/codecraft_python_audit.py . --git-history --git-depth 50

# JSON output for CI/CD pipelines
python tools/codecraft_python_audit.py . --all-files --format json --output audit.json

# Only risky patterns, no secret scanning
python tools/codecraft_python_audit.py . --no-secrets

# Fail on medium+ severity (default: high only)
python tools/codecraft_python_audit.py . --fail-on medium
```

### What It Catches

| Secret Type | Example (fake/test values shown) |
|-------------|-----------------------------------|
| AWS Access Key ID | `AKIAABCDEFGHIJKLMNOP` |
| AWS Secret Access Key | `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` |
| GitHub Token | `ghp_abcdefghijklmnopqrstuvwxyz1234567890` |
| GitLab PAT | `glpat-abcdefghijklmnopqrst` |
| Slack Token | `xoxb-1234567890-abcdefghijkl` |
| Stripe Secret Key | `sk_test_YOUR_TEST_KEY_HERE` |
| JWT Token | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` |
| Generic 32-char Hex | `a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6` |
| Generic 64-char Hex | `a1b2...` (64 chars) |

### File Types Scanned (with `--all-files`)

| Extension | Description |
|-----------|-------------|
| `.py` | Python source (AST + token scan) |
| `.env`, `.env.local`, `.env.production` | Environment files |
| `.json`, `.yaml`, `.yml`, `.toml` | Config files |
| `.ini`, `.cfg`, `.conf`, `.properties` | INI-style configs |
| `.tf`, `.tfvars` | Terraform |
| `.npmrc`, `.yarnrc`, `.pypirc` | Package manager configs |
| `.dockercfg`, `.dockerignore` | Docker configs |

### Example Output

```
HIGH     PYSEC005 config.py:12:1 [security] hardcoded secret in variable 'api_key'; use environment variables or a secrets manager
HIGH     PYSEC006 config.py:12:11 [security] potential AWS access key ID in source; use environment variables or a secrets manager
HIGH     SEC001 .env:1:19 [security] potential AWS secret access key in .env:1; use environment variables or a secrets manager
HIGH     SEC001 config.json:1:12 [security] potential GitHub token in config.json:1; use environment variables or a secrets manager
MEDIUM   PYREL002 utils.py:45:5 [reliability] broad Exception handler may hide unrelated failures
HIGH     PYSEC001 handler.py:8:12 [security] eval executes dynamically constructed Python code

Scanned 15 Python file(s); 6 finding(s) (critical=0, high=4, medium=2, low=0, info=0).
```

### CI/CD Integration (GitHub Actions)

```yaml
- name: Run CodeCraft Python Audit
  run: |
    python tools/codecraft_python_audit.py . --all-files --format json --output audit.json
    python tools/codecraft_python_audit.py . --all-files --fail-on high
```

### Smart False Positive Filtering (Built-In)

- **Git commit SHAs** (40-char hex) are ignored
- **Test/fake values** skipped: `test_key`, `your_token`, `placeholder`, `sk_test_*`, `pk_test_*`, `change_me`, `xxx`, `yyy`, `zzz`
- **AWS secrets** require `+/=` chars to distinguish from SHAs
- **High-entropy strings** only flagged near secret keywords (`key`, `secret`, `token`, `password`, `api`, etc.)

---

## ⚙️ Configuration (Optional)

Create a config file if you want to customize defaults:

**Location:**
- macOS/Linux: `~/.config/codecraft/config.json`
- Windows: `%APPDATA%\codecraft\config.json`

**Options:**

| Setting | Config Key | Default | Description |
|---------|------------|---------|-------------|
| Default mode | `defaultMode` | `full` | `off` \| `lite` \| `full` \| `ultra` |
| Hide status indicator | `hideStatus` | `false` | Hide the Pi status bar |
| Quiet startup | `quietStartup` | `false` | Hide startup toast |
| Enable code map | `codeMap` | `true` | Set `false` to disable |

**Example `config.json`:**
```json
{
  "defaultMode": "ultra",
  "hideStatus": false,
  "quietStartup": true
}
```

---

## 🛠️ Troubleshooting — Common Errors & Fixes

### "Command not found: /codecraft-help"
**Cause:** CodeCraft isn't installed for your AI agent, or you need to restart the agent.
**Fix:** Run the installer again, then **fully restart your AI agent** (close and reopen VS Code, restart Cursor, restart terminal for CLI tools).

### "npm run setup says 'No agents detected'"
**Cause:** Your AI agent isn't installed, or it's installed in a non-standard location.
**Fix:** 
- Make sure the agent is installed and you've run it at least once
- For Claude Code: run `claude-code` once first
- For Cursor: open Cursor at least once
- Then run `npm run setup` again

### "Python audit script fails with 'ModuleNotFoundError'"
**Cause:** Python version too old, or missing stdlib modules.
**Fix:** Use Python 3.10+. The script uses **only standard library** — no pip install needed.

### "Git history scan finds nothing"
**Cause:** Not in a git repo, or no commits to scan.
**Fix:** Run from inside a git repository (`git init` if needed), make sure you have commits.

### "Tests fail with 'Permission denied' on Windows"
**Cause:** Windows file locking or antivirus.
**Fix:** Run terminal as Administrator, or exclude the CodeCraft folder from antivirus.

### "Installer says 'Node.js not found'"
**Cause:** Node.js not installed or not in PATH.
**Fix:** Install Node.js 22+ from [nodejs.org](https://nodejs.org/), restart terminal, verify with `node --version`.

### "Skills not showing up in OpenCode / Codex / Qoder"
**Cause:** Skills need to be rebuilt after install.
**Fix:** Run `npm run build:skills` then restart your agent.

### "Config file changes don't take effect"
**Cause:** Config cached or wrong location.
**Fix:** Restart your AI agent. Verify config path with `npm run doctor`.

### "Secret scan flags my test files"
**Cause:** Test values look like real secrets.
**Fix:** Use fake prefixes: `test_`, `fake_`, `dummy_`, `placeholder_`, `sk_test_`, `pk_test_` — these are automatically ignored.

---

## 📚 More Documentation

- [Simple Install Guide](SIMPLE_INSTALL.md) — step-by-step with screenshots
- [Architecture](docs/ARCHITECTURE.md) — how it works under the hood
- [Development](docs/DEVELOPMENT.md) — contributing & testing
- [Changelog](CHANGELOG.md) — release history
- [License](LICENSE) — MIT

---

## 🏗️ Project Structure (For Curious Folks)

```
skills/              # Core skills (source of truth)
├── codecraft/           # Main lazy-dev skill
├── codecraft-review/    # Diff review
├── codecraft-audit/     # Repo audit
├── codecraft-debt/      # Shortcut debt ledger
├── codecraft-gain/      # Benchmarks
└── codecraft-help/      # This reference

hooks/               # Agent adapters (Claude, Cursor, Codex, etc.)
tools/
└── codecraft_python_audit.py   # Secret scanner (stdlib only)
commands/            # Claude Code .toml commands
tests/               # 168 tests
.opencode/           # OpenCode commands
```

---

## ⚖️ License

MIT — see [LICENSE](LICENSE).

---

<p align="center">
  <sub>Built for engineers who think the best code is the code never written.</sub>
</p>