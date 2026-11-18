<p align="center">
  <img src="assets/codecraft-mark.svg" alt="CodeCraft" width="128" height="128">
</p>

<h1 align="center">CodeCraft</h1>

<p align="center">
  <strong>Lazy senior dev mode for AI coding agents — the smallest change that fully solves the problem, and a reply a busy human understands in one read.</strong>
</p>

<p align="center">
  <a href="https://github.com/kunalkumar11/Codecraft/actions"><img alt="Tests" src="https://img.shields.io/github/actions/workflow/status/kunalkumar11/Codecraft/test.yml?label=tests&logo=github"></a>
  <a href="https://github.com/kunalkumar11/Codecraft/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/kunalkumar11/Codecraft?color=0A7"></a>
  <a href="https://nodejs.org/"><img alt="Node" src="https://img.shields.io/badge/node-%3E%3D22-339933?logo=node.js"></a>
  <a href="https://github.com/kunalkumar11/Codecraft/issues"><img alt="Issues" src="https://img.shields.io/github/issues/kunalkumar11/Codecraft?color=E03"></a>
</p>

---

## 🎯 What is CodeCraft?

CodeCraft is a **compatibility-preserving derivative of [Ponytail](https://github.com/DietrichGebert/ponytail)** that gives you `/codecraft*` commands and skills while keeping every `/ponytail*` alias, config path, and env var working for existing users.

| Feature | What it does |
|---------|--------------|
| **Modes** | `/codecraft lite\|full\|ultra\|off` — YAGNI → stdlib → native → one-liner → minimum |
| **Review** | `/codecraft-review` — bugs, security, load, missing tests, speed, bloat (Must/Should/Nice) |
| **Audit** | `/codecraft-audit` — same review, whole repo, ranked |
| **Debt** | `/codecraft-debt` — harvest `shortcut:` comments into a tracked ledger |
| **Gain** | `/codecraft-gain` — benchmark scoreboard: 53% less code, 45% fewer tokens, 26% less cost, 41% faster |
| **Help** | `/codecraft-help` — this reference card |
| **Python Audit** | `python tools/codecraft_python_audit.py` — AST + regex secret detection, risky patterns |

**All `/ponytail*` commands still work.** Drop-in replacement.

---

## 🚀 Quick Start (30 seconds)

### 🎯 Easiest Way — Single File Install (No Clone Needed!)

**Just download and run one file:**

```bash
# Linux/macOS/Git Bash:
curl -fsSL https://raw.githubusercontent.com/kunalkumar11/Codecraft/main/codecraft-install.js > codecraft-install.js && node codecraft-install.js

# Windows PowerShell:
irm https://raw.githubusercontent.com/kunalkumar11/Codecraft/main/codecraft-install.js | Out-File codecraft-install.js; node codecraft-install.js
```

**That's it.** The installer:
1. Detects your AI agents (Claude Code, Codex, Grok, Cursor, OpenCode, Gemini, Kimi, Qoder, Hermes)
2. Downloads CodeCraft from GitHub automatically
3. Installs plugins, skills, hooks, and commands for each detected agent
4. Tells you exactly what was installed where

Then **restart your agent** and type:
```
/codecraft-help
```

> **Give this file to any AI agent** — just hand them `codecraft-install.js` and say "run this with Node.js". It works completely standalone.

---

### 📦 Traditional Way (Clone + npm)

### Prerequisites
- **Node.js 22+** (CI target)
- **Python 3.10+** (for Hermes adapter & Python checks)
- **Git** (for debt-scan & benchmark)

### Install & Verify (One Command!)
```bash
# 1. Clone
git clone https://github.com/kunalkumar11/Codecraft.git
cd Codecraft

# 2. Install deps
npm install

# 3. Install for ALL detected agents automatically
npm run setup

# 4. Run tests (should show 168 passing)
npm test
```

### ✅ Verified Working Install (Copy-Paste This)

**Tested on Windows + Claude Code + Codex + Grok + Cursor:**

```bash
git clone https://github.com/kunalkumar11/Codecraft.git
cd Codecraft
npm install
npm run setup
```

Then **restart your agent** and type:
```
/codecraft-help
```

**That's it.** The installer detects your agents (Claude Code, Codex, Grok, Cursor, etc.) and configures them automatically.

### 📖 Simple Install Guide
> **New to this?** See [SIMPLE_INSTALL.md](SIMPLE_INSTALL.md) — step-by-step with screenshots, troubleshooting, and per-agent instructions.

### Use It (Inside an AI Assistant)

> **Important:** `/codecraft` commands run inside AI coding agents, **not** in your shell.

| Host | How to invoke |
|------|---------------|
| **Claude Code** (VS Code extension) | Open Claude Code panel → type `/codecraft-help` |
| **Cursor** | Open Cursor chat → type `/codecraft-help` |
| **Continue.dev** | Open Continue chat → type `/codecraft-help` |
| **Codex CLI** | Run `codex` → type `/codecraft-help` |
| **Claude Code CLI** | Run `claude-code` → type `/codecraft-help` |
| **OpenCode** | Run `opencode` → type `/codecraft-help` |
| **Grok Build** | Run `grok` → type `/codecraft-help` |
| **Gemini CLI** | Run `gemini` → type `/codecraft-help` |
| **Kimi Code** | Run `kimi` → type `/codecraft-help` |
| **Qoder** | Run `qoder` → type `/codecraft-help` |

### Verify Installation
```bash
# Check what's installed where
npm run doctor

# Test commands in your agent (note: NO dash between codecraft and mode)
/codecraft-help      # Show reference card
/codecraft           # Show current mode
/codecraft ultra     # Switch to ultra (questions requests)
/codecraft lite      # Switch to lite (minimal)
/codecraft full      # Switch to full (default)
/codecraft off       # Disable

# Skills (these USE dashes)
/codecraft-review    # Review a diff
/codecraft-audit     # Audit whole repo
/codecraft-debt      # List shortcut: comments
/codecraft-gain      # Show benchmark scoreboard
```

> **Note:** Mode commands use space (`/codecraft ultra`), skill commands use dash (`/codecraft-audit`).

---

## ⚙️ Configuration

| Variable | Config Key | Default | Notes |
|----------|------------|---------|-------|
| `CODECRAFT_DEFAULT_MODE` | `defaultMode` | `full` | `off\|lite\|full\|ultra` |
| `CODECRAFT_HIDE_STATUS` | `hideStatus` | `false` | Hide Pi status indicator |
| `CODECRAFT_QUIET_STARTUP` | `quietStartup` | `false` | Hide startup toast |
| `CODECRAFT_SUBAGENT_MATCHER` | — | all | Regex to scope subagent injection |
| `CODECRAFT_MAP` | — | `1` | Enable code map (0 to disable) |

**Config file locations:**
- macOS/Linux: `~/.config/ponytail/config.json`
- Windows: `%APPDATA%\ponytail\config.json`
- `XDG_CONFIG_HOME` overrides base location if set

> Legacy `PONYTAIL_*` env vars and config paths still work.

---

## 🏗️ Architecture

```
skills/          # Canonical instructions & task skills (source of truth)
├── codecraft/           # Main lazy-dev skill
├── codecraft-review/    # Diff review skill
├── codecraft-audit/     # Repo audit skill
├── codecraft-debt/      # Shortcut debt ledger
├── codecraft-gain/      # Benchmark scoreboard
└── codecraft-help/      # This reference card

hooks/           # Host lifecycle adapters (Claude, Cursor, Codex, etc.)
pi-extension/    # Local task board (session metrics, CSV, webhooks)
.opencode/       # OpenCode command definitions
commands/        # Claude Code .toml commands
tests/           # Adapter, installer, behavior tests
benchmarks/      # Agentic benchmark harnesses
tools/           # Python source auditor (AST-based, no deps)
    └── codecraft_python_audit.py  # Secret detection + risky pattern scanner
```

The build script (`scripts/build-openclaw-skills.js`) auto-generates `.openclaw/skills/` from `skills/` — **CodeCraft skills are transformed Ponytail skills** (`PONYTAIL→CODECRAFT`, `Ponytail→CodeCraft`, `ponytail→codecraft`). Tests enforce they stay in sync.

---

## 🧪 Test Suite

```bash
# Core commands & skills
node --test tests/commands.test.js                    # 6 tests

# Host adapters (Claude, Cursor, Codex, Gemini, Grok, Hermes, OpenCode, Pi, Qoder, Kimi)
node --test tests/*-plugin.test.js                    # 50 tests

# OpenClaw skill generation
node --test tests/openclaw-skills.test.js             # 36 tests

# Full suite
npm test                                              # 168 tests (2 pre-existing CSV flakes)
```

---

## 🔍 Python Audit Tool (Secret Detection + Risky Patterns)

CodeCraft includes a standalone Python auditor (`tools/codecraft_python_audit.py`) that scans for:

- **Hardcoded secrets** (API keys, tokens, passwords) in variable assignments
- **Secret patterns** in strings/comments (AWS, GitHub, GitLab, Slack, Stripe, JWT, etc.)
- **Risky patterns**: `eval`/`exec`, `os.system`, `subprocess shell=True`, `pickle` deserialization
- **Broad exception handlers** that hide failures

### Quick Start

```bash
# Scan a Python project (includes secret detection by default)
python tools/codecraft_python_audit.py /path/to/project

# Scan ALL config files (.env, .json, .yaml, .toml, .ini, .tf, .npmrc, etc.)
python tools/codecraft_python_audit.py . --all-files

# Scan git commit history for leaked secrets
python tools/codecraft_python_audit.py . --git-history --git-depth 50

# JSON output for CI/CD pipelines
python tools/codecraft_python_audit.py . --all-files --format json --output audit.json

# Disable secret scanning (risky patterns only)
python tools/codecraft_python_audit.py . --no-secrets

# Fail on medium+ findings (default: high)
python tools/codecraft_python_audit.py . --fail-on medium
```

### Detected Secret Formats

| Format | Example Pattern | Rule |
|--------|-----------------|------|
| AWS Access Key ID | `AKIAABCDEFGHIJKLMNOP` | `PYSEC006` / `SEC001` |
| AWS Secret Access Key | `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` | `PYSEC006` / `SEC001` |
| GitHub Token | `ghp_abcdefghijklmnopqrstuvwxyz1234567890` | `PYSEC006` / `SEC001` |
| GitLab PAT | `glpat-abcdefghijklmnopqrst` | `PYSEC006` / `SEC001` |
| Slack Token | `xoxb-1234567890-abcdefghijkl` | `PYSEC006` / `SEC001` |
| Stripe Secret Key | `sk_test_YOUR_TEST_KEY_HERE` | `PYSEC006` / `SEC001` |
| JWT Token | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` | `PYSEC006` / `SEC001` |
| Generic 32-char Hex | `a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6` | `PYSEC006` / `SEC001` |
| Generic 64-char Hex | `a1b2...` (64 chars) | `PYSEC006` / `SEC001` |

### Supported File Types (with `--all-files`)

| Extension | Description |
|-----------|-------------|
| `.py` | Python source (AST + token scan) |
| `.env`, `.env.local`, `.env.production`, etc. | Environment files |
| `.json`, `.yaml`, `.yml`, `.toml` | Config files |
| `.ini`, `.cfg`, `.conf`, `.config`, `.properties` | INI-style configs |
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

### CI/CD Integration

```yaml
# GitHub Actions example
- name: Run CodeCraft Python Audit
  run: |
    python tools/codecraft_python_audit.py . --all-files --format json --output audit.json
    # Fail on high+ findings
    python tools/codecraft_python_audit.py . --all-files --fail-on high
```

### Smart False Positive Filtering

- **Git commit SHAs** (40-char hex) are ignored via word boundaries
- **Test/fake values** skipped: `test_key`, `your_token`, `placeholder`, `sk_test_*`, `pk_test_*`, `change_me`, `xxx`, `yyy`, `zzz`
- **AWS secrets** require `+/=` chars to distinguish from SHAs
- **High-entropy strings** only flagged near secret context keywords (`key`, `secret`, `token`, `password`, `api`, etc.)

---

## 📦 Host Support

| Host | Status | Notes |
|------|--------|-------|
| **Claude Code** | ✅ Full | Extension + CLI |
| **Cursor** | ✅ Full | Hooks + skills |
| **Codex CLI** | ✅ Full | Native skills |
| **OpenCode** | ✅ Full | Native commands |
| **Gemini CLI** | ✅ Commands | Reuses .toml files |
| **Hermes** | ✅ Full | Python plugin + hooks |
| **Pi** | ✅ Full | Local task board |
| **Qoder** | ✅ Skills | Auto-invocation |
| **Kimi** | ✅ Skills | AGENTS.md + skills |

---

## 📚 Documentation

- [Architecture](docs/ARCHITECTURE.md) — data flow & trust boundaries
- [Development](docs/DEVELOPMENT.md) — contributing & testing
- [Origin](docs/ORIGIN.md) — upstream attribution
- [Install](INSTALL.md) — host-native plugin installation
- [Changelog](CHANGELOG.md) — release history

---

## ⚖️ License

MIT — preserves upstream copyright. See [LICENSE](LICENSE) and [docs/ORIGIN.md](docs/ORIGIN.md).

---

<p align="center">
  <sub>Built for engineers who think the best code is the code never written.</sub>
</p>