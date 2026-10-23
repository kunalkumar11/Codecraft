---
name: codecraft-help
description: >
  Quick reference for codecraft levels, skills and commands. One-shot display.
  Use for /codecraft-help, "codecraft help", "how do I use codecraft".
---

# CodeCraft Help

Display this reference card when invoked. One-shot, do NOT change mode,
write flag files, or persist anything.

## Levels

| Level | Trigger | What change |
|-------|---------|-------------|
| **Lite** | `/codecraft lite` | Build what was asked, name the smaller option in one line. |
| **Full** | `/codecraft` | The smallest complete change, a check where the logic needs one, and a reply that names what was skipped and any risk. Default. |
| **Ultra** | `/codecraft ultra` | Also questions the request and pushes back before building. |

Level sticks until changed or session end.

## Skills

| Skill | Trigger | What it does |
|-------|---------|--------------|
| **codecraft** | `/codecraft` | Lazy mode itself: least new code, clear replies that name skipped work and risks. |
| **codecraft-review** | `/codecraft-review` | Quality review of a diff: bugs, security, load, missing tests, speed, what to cut. Each finding says what goes wrong and how to fix it. |
| **codecraft-audit** | `/codecraft-audit` | The same quality review for the whole repo, ranked. |
| **codecraft-debt** | `/codecraft-debt` | Harvest `shortcut:` comments into a tracked ledger. |
| **codecraft-gain** | `/codecraft-gain` | Measured-impact scoreboard: less code, less cost, more speed. |
| **codecraft-help** | `/codecraft-help` | This card. |

In Codex CLI and the IDE extension, invoke skills with `$codecraft:codecraft`,
`$codecraft:codecraft-review`, or `$codecraft:codecraft-help`. Claude Code and OpenCode use the
slash-command forms above (OpenCode ships all six as slash commands).

## Deactivate

Say "stop codecraft" or "normal mode". Resume anytime with `/codecraft`.
`/codecraft off` also works.

## Band (Claude Code)

`/codecraft band` hides the band above the prompt, the same command brings it back.
`/codecraft band on` and `/codecraft band off` set it directly. The level stays.
`/codecraft band import` adds your past Claude Code sessions (cost, agent time, tokens) to the board.

## Configure Default Mode

Default mode = `full`, auto-active every session. Change it:

**Environment variable** (highest priority):
```bash
export CODECRAFT_DEFAULT_MODE=ultra
```

**Config file** (`~/.config/codecraft/config.json`, Windows: `%APPDATA%\codecraft\config.json`):
```json
{ "defaultMode": "lite" }
```

Set `"off"` to disable auto-activation on session start, activate manually
with `/codecraft` when wanted.

Resolution: env var > config file > `full`.

## Update

Enable auto-update once: open `/plugin`, go to Marketplaces, pick codecraft, Enable auto-update. Claude Code then pulls new versions at startup (run `/reload-plugins` when it prompts). Manual refresh: `/plugin marketplace update codecraft` then `/reload-plugins`.

If `/plugin` is not recognized, your Claude Code is out of date. Update it (`npm install -g @anthropic-ai/claude-code@latest`, or `brew upgrade claude-code`) and restart. Other hosts use their own update flow.

## More

Full docs + examples: https://github.com/DietrichGebert/codecraft
