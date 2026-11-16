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

**All `/ponytail*` commands still work.** Drop-in replacement.

---

## 🚀 Quick Start (30 seconds)

### Prerequisites
- **Node.js 22+** (CI target)
- **Python 3.10+** (for Hermes adapter & Python checks)
- **Git** (for debt-scan & benchmark)

### Install & Verify
```bash
# 1. Clone
git clone https://github.com/kunalkumar11/Codecraft.git
cd Codecraft

# 2. Install deps
npm install

# 3. Run tests (should show 6 passing)
node --test tests/commands.test.js
```

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