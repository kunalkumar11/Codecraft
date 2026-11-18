# CodeCraft — Simple Install Guide (Works Everywhere)

> **One file installs CodeCraft in any AI coding agent.** No clone, no npm, no confusion.

---

## 🎯 Easiest Way — Single File Install (No Clone Needed!)

**Just download and run one file:**

```bash
# Linux/macOS/Git Bash:
curl -fsSL https://raw.githubusercontent.com/kunalkumar11/Codecraft/main/codecraft-install.js > codecraft-install.js && node codecraft-install.js

# Windows PowerShell:
curl -fsSL https://raw.githubusercontent.com/kunalkumar11/Codecraft/main/codecraft-install.js -o codecraft-install.js; node codecraft-install.js
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

## 📦 Traditional Way (Clone + npm)

If you prefer the traditional approach:

```bash
# 1. Get CodeCraft
git clone https://github.com/kunalkumar11/Codecraft.git
cd Codecraft

# 2. Install dependencies
npm install

# 3. Install for ALL your AI agents at once
npm run setup
```

**That's it.** The installer detects which agents you have and sets them up automatically.

---

## 🔍 What Just Happened?

The installer checks for these agents and configures each one:

| Agent | What Gets Installed |
|-------|---------------------|
| **Claude Code** (CLI + VS Code) | Plugin + commands to `~/.claude/plugins/codecraft/` |
| **Codex** (CLI + Desktop) | Plugin + hooks to `~/.codex/plugins/codecraft/` |
| **Grok Build** | Skills to `~/.grok/plugins/codecraft/` |
| **Cursor** | Hooks to `~/.cursor/hooks.json` + rule file |
| **OpenCode** | Plugin to `~/.config/opencode/plugins/codecraft/` |
| **Gemini CLI** | Extension to `~/.config/gemini/extensions/codecraft/` |
| **Kimi Code** | Plugin to `~/.kimi/plugins/codecraft/` |
| **Qoder** | Plugin + rules to `~/.qoder/plugins/codecraft/` |
| **Hermes** | Full repo copy to `~/.hermes/plugins/codecraft/` |

**Don't have some of these?** No problem — it skips missing ones and tells you.

---

## ✅ Verify It Works

```bash
# Check what was installed where
npm run doctor

# Inside your AI agent, type:
/codecraft-help
```

You should see the CodeCraft reference card. If you do, **you're done.**

---

## 🎯 Per-Agent Manual Install (If One-Command Doesn't Work)

### Claude Code (VS Code Extension or CLI)
```bash
# From the CodeCraft folder:
npm run setup -- --agent claude
```
Then in Claude: type `/codecraft-help`

### Codex CLI / Desktop
```bash
npm run setup -- --agent codex
```
Then in Codex: type `/codecraft-help`

### Grok Build
```bash
npm run setup -- --agent grok
```
Then in Grok: type `/codecraft-help` (auto-invokes on coding tasks)

### Cursor
```bash
# Global (all projects):
npm run setup -- --agent cursor

# Current project only:
npm run setup -- --agent cursor --project
```
Then in Cursor: type `/codecraft-help`

### OpenCode
```bash
npm run setup -- --agent opencode
```
Then in OpenCode: type `/codecraft-help`

### Gemini CLI
```bash
npm run setup -- --agent gemini
```
Then in Gemini: type `/codecraft-help`

### Kimi Code
```bash
npm run setup -- --agent kimi
```
Then in Kimi: type `/codecraft-help`

### Qoder
```bash
npm run setup -- --agent qoder
```
Then in Qoder: type `/codecraft-help`

### Hermes Agent
```bash
npm run setup -- --agent hermes
```
Restart Hermes, then type `/codecraft-help`

---

## 📋 For Any Other Agent (Windsurf, Cline, Aider, Zed, Copilot, Junie, Amp, Jules, etc.)

**Just copy one file:**

```bash
# From any project folder:
cp /path/to/Codecraft/AGENTS.md ./AGENTS.md
```

That's it. The agent reads `AGENTS.md` automatically.

---

## 🔧 Troubleshooting

### "command not found: npx"
Install Node.js 22+ from [nodejs.org](https://nodejs.org)

### "Permission denied" on Windows
Run PowerShell as Administrator, or use Git Bash

### Agent not detected
```bash
# Force install anyway:
npm run setup -- --agent claude --force
```

### Want to uninstall?
```bash
npm run setup -- --agent claude --force  # Reinstall clean
# Or manually delete the plugin folder shown by 'doctor'
```

### Node not found in hooks (harmless error)
Install Node.js and make sure it's in your **non-interactive shell PATH** (not just your terminal PATH)

---

## 📖 Quick Reference (After Install)

| Command | What It Does |
|---------|--------------|
| `/codecraft-help` | Show this reference |
| `/codecraft` | Toggle on/off or show level |
| `/codecraft lite` | Minimal mode — just build what's asked |
| `/codecraft full` | Default — lazy senior dev rules |
| `/codecraft ultra` | Question the request before building |
| `/codecraft off` | Disable CodeCraft |
| `/codecraft-review` | Review a diff for bugs, bloat, missing tests |
| `/codecraft-audit` | Audit entire repo, ranked findings |
| `/codecraft-debt` | List all `shortcut:` comments with upgrade paths |
| `/codecraft-gain` | Show benchmark scoreboard |

**All `/ponytail*` commands also work** (backward compatibility).

---

## 🌍 Works On Any Project

CodeCraft doesn't modify your project files. It only:
1. Installs configuration in your **user config folders** (`~/.claude`, `~/.codex`, etc.)
2. Injects guidance into the **AI's context** when you chat

Use it on:
- ✅ New projects
- ✅ Existing projects  
- ✅ Monorepos
- ✅ Any language (JS, Python, Go, Rust, etc.)
- ✅ Any framework
- ✅ Work or personal projects

---

## 🆘 Still Stuck?

1. Run `npm run doctor` — shows exactly what's installed where
2. Check the agent's plugin/settings UI — look for "CodeCraft" or "ponytail"
3. Restart the agent completely (close and reopen)
4. Open an issue at [github.com/kunalkumar11/Codecraft/issues](https://github.com/kunalkumar11/Codecraft/issues)

---

**That's the whole guide. One command, works everywhere.** 🎉