#!/usr/bin/env node
// Unified installer for CodeCraft across all supported AI agents.
// Detects available agents and installs the appropriate plugin/skill/hook configuration.
// Run with --dry-run to see what would be installed without making changes.

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const os = require('os');

const ROOT = path.join(__dirname, '..');
const VERSION = JSON.parse(fs.readFileSync(path.join(ROOT, 'package.json'), 'utf8')).version;

const AGENTS = {
  claude: {
    name: 'Claude Code (CLI + VS Code)',
    detect: () => checkCommand('claude') || checkCommand('claude-code') || fs.existsSync(path.join(os.homedir(), '.claude')),
    install: (opts) => installClaude(opts),
    configDir: () => path.join(os.homedir(), '.claude'),
  },
  codex: {
    name: 'Codex CLI / Desktop',
    detect: () => checkCommand('codex'),
    install: (opts) => installCodex(opts),
    configDir: () => path.join(os.homedir(), '.codex'),
  },
  grok: {
    name: 'Grok Build',
    detect: () => checkCommand('grok') || fs.existsSync(path.join(os.homedir(), '.grok')),
    install: (opts) => installGrok(opts),
    configDir: () => path.join(os.homedir(), '.grok'),
  },
  cursor: {
    name: 'Cursor',
    detect: () => checkCommand('cursor') || fs.existsSync(path.join(os.homedir(), '.cursor')),
    install: (opts) => installCursor(opts),
    configDir: () => path.join(os.homedir(), '.cursor'),
  },
  opencode: {
    name: 'OpenCode',
    detect: () => checkCommand('opencode'),
    install: (opts) => installOpenCode(opts),
    configDir: () => path.join(os.homedir(), '.config', 'opencode'),
  },
  gemini: {
    name: 'Gemini CLI',
    detect: () => checkCommand('gemini'),
    install: (opts) => installGemini(opts),
    configDir: () => path.join(os.homedir(), '.config', 'gemini'),
  },
  kimi: {
    name: 'Kimi Code',
    detect: () => fs.existsSync(path.join(os.homedir(), '.kimi')),
    install: (opts) => installKimi(opts),
    configDir: () => path.join(os.homedir(), '.kimi'),
  },
  qoder: {
    name: 'Qoder',
    detect: () => checkCommand('qoder') || fs.existsSync(path.join(os.homedir(), '.qoder')),
    install: (opts) => installQoder(opts),
    configDir: () => path.join(os.homedir(), '.qoder'),
  },
  hermes: {
    name: 'Hermes Agent',
    detect: () => fs.existsSync(path.join(os.homedir(), '.hermes')),
    install: (opts) => installHermes(opts),
    configDir: () => path.join(os.homedir(), '.hermes', 'plugins'),
  },
  // windsurf, cline, aider, kiro, etc. use AGENTS.md copy - handled generically
};

function checkCommand(cmd) {
  try {
    const result = spawnSync(cmd, ['--version'], { encoding: 'utf8', timeout: 3000 });
    return result.status === 0;
  } catch {
    return false;
  }
}

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = {
    dryRun: false,
    agents: null, // null = all detected
    project: false, // --project flag for Cursor
    force: false,
    list: false,
    help: false,
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--dry-run' || arg === '-n') opts.dryRun = true;
    else if (arg === '--agent' || arg === '-a') opts.agents = args[++i].split(',');
    else if (arg === '--project' || arg === '-p') opts.project = true;
    else if (arg === '--force' || arg === '-f') opts.force = true;
    else if (arg === '--list' || arg === '-l') opts.list = true;
    else if (arg === '--help' || arg === '-h') opts.help = true;
  }
  return opts;
}

function printHelp() {
  console.log(`
CodeCraft Unified Installer v${VERSION}

Usage: npx codecraft install [options]

Options:
  --dry-run, -n       Show what would be installed without making changes
  --agent, -a <list>  Comma-separated list of agents to install (default: all detected)
  --project, -p       For Cursor: install to project .cursor/ instead of global
  --force, -f         Overwrite existing installations
  --list, -l          List all supported agents and detection status
  --help, -h          Show this help

Examples:
  npx codecraft install                    # Install for all detected agents
  npx codecraft install --dry-run          # Preview what would happen
  npx codecraft install -a claude,codex    # Install only for Claude and Codex
  npx codecraft install -p                 # Cursor project-level install
`);
}

async function main() {
  const opts = parseArgs();

  if (opts.help) {
    printHelp();
    return;
  }

  console.log(`\n🔧 CodeCraft Unified Installer v${VERSION}\n`);

  // Detect available agents
  const detected = {};
  for (const [key, agent] of Object.entries(AGENTS)) {
    const available = agent.detect();
    detected[key] = { ...agent, available };
    const status = available ? '✅ detected' : '❌ not found';
    console.log(`  ${agent.name}: ${status}`);
  }

  if (opts.list) {
    console.log('\nDone.\n');
    return;
  }

  // Determine targets
  let targets = opts.agents
    ? opts.agents.map(a => a.toLowerCase()).filter(a => AGENTS[a])
    : Object.keys(detected).filter(k => detected[k].available);

  if (targets.length === 0) {
    console.log('\n❌ No agents selected or detected. Use --agent to specify manually.\n');
    process.exit(1);
  }

  console.log(`\n📦 Installing for: ${targets.map(t => AGENTS[t].name).join(', ')}`);
  if (opts.dryRun) console.log('   (dry run - no changes will be made)\n');

  const results = { success: [], failed: [], skipped: [] };

  for (const key of targets) {
    const agent = detected[key];
    if (!agent.available && !opts.force) {
      console.log(`  ⏭️  ${agent.name}: not detected (use --force to install anyway)`);
      results.skipped.push(key);
      continue;
    }

    try {
      const result = await agent.install({ ...opts, root: ROOT, version: VERSION });
      if (result === 'skipped') {
        results.skipped.push(key);
      } else if (result) {
        results.success.push(key);
      } else {
        results.failed.push(key);
      }
    } catch (e) {
      console.log(`  ❌ ${agent.name}: ${e.message}`);
      results.failed.push(key);
    }
  }

  // Summary
  console.log('\n📋 Summary:');
  if (results.success.length) console.log(`  ✅ Installed: ${results.success.map(k => AGENTS[k].name).join(', ')}`);
  if (results.skipped.length) console.log(`  ⏭️  Skipped: ${results.skipped.map(k => AGENTS[k].name).join(', ')}`);
  if (results.failed.length) console.log(`  ❌ Failed: ${results.failed.map(k => AGENTS[k].name).join(', ')}`);

  // Generic AGENTS.md copy instruction for rule-only agents
  const ruleOnlyAgents = ['windsurf', 'cline', 'aider', 'kiro', 'zed', 'codewhale', 'copilot', 'junie', 'amp', 'jules'];
  console.log('\n📝 For other agents (Windsurf, Cline, Aider, Kiro, Zed, CodeWhale, Copilot, Junie, Amp, Jules):');
  console.log(`   Copy AGENTS.md to your project root or global config:`);
  console.log(`   cp ${path.join(ROOT, 'AGENTS.md')} <project>/AGENTS.md`);

  if (opts.dryRun) {
    console.log('\n💡 Run without --dry-run to apply changes.\n');
  } else {
    console.log('\n✨ Done! Restart your agent to pick up the changes.\n');
  }

  if (results.failed.length) process.exit(1);
}

// ============ Agent-specific installers ============

async function installClaude(opts) {
  const { dryRun, force, root } = opts;
  const pluginDir = path.join(root, '.claude-plugin');
  const targetDir = path.join(os.homedir(), '.claude', 'plugins', 'codecraft');

  if (dryRun) {
    console.log(`  📋 ${AGENTS.claude.name}: Would copy plugin to ${targetDir}`);
    return 'skipped';
  }

  // Copy plugin directory
  fs.mkdirSync(targetDir, { recursive: true });
  copyDir(pluginDir, targetDir);

  // Also install commands if they exist
  const commandsDir = path.join(root, 'commands');
  const claudeCommandsDir = path.join(os.homedir(), '.claude', 'commands');
  if (fs.existsSync(commandsDir)) {
    fs.mkdirSync(claudeCommandsDir, { recursive: true });
    for (const file of fs.readdirSync(commandsDir)) {
      if (file.startsWith('codecraft') && file.endsWith('.toml')) {
        fs.copyFileSync(path.join(commandsDir, file), path.join(claudeCommandsDir, file));
      }
    }
  }

  console.log(`  ✅ ${AGENTS.claude.name}: Installed plugin + commands`);
  return true;
}

async function installCodex(opts) {
  const { dryRun, force, root } = opts;
  const pluginDir = path.join(root, '.codex-plugin');
  const targetDir = path.join(os.homedir(), '.codex', 'plugins', 'codecraft');

  if (dryRun) {
    console.log(`  📋 ${AGENTS.codex.name}: Would copy plugin to ${targetDir}`);
    return 'skipped';
  }

  fs.mkdirSync(targetDir, { recursive: true });
  copyDir(pluginDir, targetDir);

  // Codex plugin.json references ./skills/ and ./hooks/ — copy them
  copyDir(path.join(root, 'skills'), path.join(targetDir, 'skills'));
  copyDir(path.join(root, 'hooks'), path.join(targetDir, 'hooks'));

  console.log(`  ✅ ${AGENTS.codex.name}: Installed plugin + skills + hooks`);
  return true;
}

async function installGrok(opts) {
  const { dryRun, force, root } = opts;
  const pluginDir = path.join(root, '.grok-plugin');
  const targetDir = path.join(os.homedir(), '.grok', 'plugins', 'codecraft');

  if (dryRun) {
    console.log(`  📋 ${AGENTS.grok.name}: Would copy plugin to ${targetDir}`);
    return 'skipped';
  }

  fs.mkdirSync(targetDir, { recursive: true });
  copyDir(pluginDir, targetDir);

  // Grok marketplace.json references ./skills/ — copy them
  copyDir(path.join(root, 'skills'), path.join(targetDir, 'skills'));

  console.log(`  ✅ ${AGENTS.grok.name}: Installed plugin + skills`);
  return true;
}

async function installCursor(opts) {
  const { dryRun, force, root, project } = opts;

  if (dryRun) {
    const target = project ? 'project .cursor/hooks.json' : 'global ~/.cursor/hooks.json';
    console.log(`  📋 ${AGENTS.cursor.name}: Would run cursor-hooks.js install (${target})`);
    return 'skipped';
  }

  const script = path.join(root, 'scripts', 'cursor-hooks.js');
  const args = ['install'];
  if (project) args.push('--project');

  const result = spawnSync('node', [script, ...args], { cwd: root, encoding: 'utf8', timeout: 30000 });
  if (result.error) throw new Error(result.error.message);
  if (result.status !== 0) throw new Error(result.stderr || 'cursor-hooks.js failed');

  // Also copy rules file for rule-only fallback
  const rulesDir = project ? path.join(process.cwd(), '.cursor', 'rules') : path.join(os.homedir(), '.cursor', 'rules');
  fs.mkdirSync(rulesDir, { recursive: true });
  fs.copyFileSync(path.join(root, '.cursor', 'rules', 'codecraft.mdc'), path.join(rulesDir, 'codecraft.mdc'));

  console.log(`  ✅ ${AGENTS.cursor.name}: Installed hooks${project ? ' (project)' : ' (global)'} + rules`);
  return true;
}

async function installOpenCode(opts) {
  const { dryRun, force, root } = opts;
  const pluginDir = path.join(root, '.opencode', 'plugins');
  const targetDir = path.join(os.homedir(), '.config', 'opencode', 'plugins', 'codecraft');

  if (dryRun) {
    console.log(`  📋 ${AGENTS.opencode.name}: Would copy plugin to ${targetDir}`);
    return 'skipped';
  }

  fs.mkdirSync(targetDir, { recursive: true });
  copyDir(pluginDir, targetDir);

  console.log(`  ✅ ${AGENTS.opencode.name}: Installed plugin (V1+V2 compatible)`);
  return true;
}

async function installGemini(opts) {
  const { dryRun, force, root } = opts;
  const extDir = path.join(root, '.gemini-extension'); // if exists, else use skills/
  const targetDir = path.join(os.homedir(), '.config', 'gemini', 'extensions', 'codecraft');

  if (dryRun) {
    console.log(`  📋 ${AGENTS.gemini.name}: Would install extension to ${targetDir}`);
    return 'skipped';
  }

  // Gemini uses the same structure as the repo root for extensions
  fs.mkdirSync(targetDir, { recursive: true });
  // Copy skills, commands, AGENTS.md
  copyDir(path.join(root, 'skills'), path.join(targetDir, 'skills'));
  copyDir(path.join(root, 'commands'), path.join(targetDir, 'commands'));
  fs.copyFileSync(path.join(root, 'AGENTS.md'), path.join(targetDir, 'AGENTS.md'));

  console.log(`  ✅ ${AGENTS.gemini.name}: Installed extension`);
  return true;
}

async function installKimi(opts) {
  const { dryRun, force, root } = opts;
  const pluginDir = path.join(root, '.kimi-plugin');
  const targetDir = path.join(os.homedir(), '.kimi', 'plugins', 'codecraft');

  if (dryRun) {
    console.log(`  📋 ${AGENTS.kimi.name}: Would copy plugin to ${targetDir}`);
    return 'skipped';
  }

  fs.mkdirSync(targetDir, { recursive: true });
  copyDir(pluginDir, targetDir);

  // Kimi plugin.json references ./skills/ and ./AGENTS.md
  copyDir(path.join(root, 'skills'), path.join(targetDir, 'skills'));
  fs.copyFileSync(path.join(root, 'AGENTS.md'), path.join(targetDir, 'AGENTS.md'));

  console.log(`  ✅ ${AGENTS.kimi.name}: Installed plugin + skills + AGENTS.md`);
  return true;
}

async function installQoder(opts) {
  const { dryRun, force, root } = opts;
  const pluginDir = path.join(root, '.qoder-plugin');
  const targetDir = path.join(os.homedir(), '.qoder', 'plugins', 'codecraft');

  if (dryRun) {
    console.log(`  📋 ${AGENTS.qoder.name}: Would copy plugin to ${targetDir}`);
    return 'skipped';
  }

  fs.mkdirSync(targetDir, { recursive: true });
  copyDir(pluginDir, targetDir);

  // Qoder plugin.json references ./skills/, ./rules/, and ./hooks/
  copyDir(path.join(root, 'skills'), path.join(targetDir, 'skills'));
  copyDir(path.join(root, '.qoder', 'rules'), path.join(targetDir, '.qoder', 'rules'));
  copyDir(path.join(root, 'hooks'), path.join(targetDir, 'hooks'));

  console.log(`  ✅ ${AGENTS.qoder.name}: Installed plugin + skills + rules + hooks`);
  return true;
}

async function installHermes(opts) {
  const { dryRun, force, root } = opts;
  const targetDir = path.join(os.homedir(), '.hermes', 'plugins', 'codecraft');

  if (dryRun) {
    console.log(`  📋 ${AGENTS.hermes.name}: Would copy plugin to ${targetDir}`);
    return 'skipped';
  }

  fs.mkdirSync(targetDir, { recursive: true });
  // Copy the whole repo as Hermes expects the Python adapter at root
  copyDir(root, targetDir, ['node_modules', '.git', 'benchmarks', 'examples', 'assets', 'tests', 'scripts', 'docs']);

  console.log(`  ✅ ${AGENTS.hermes.name}: Installed plugin (full repo copy)`);
  return true;
}

// ============ Helpers ============

function copyDir(src, dest, exclude = []) {
  if (!fs.existsSync(src)) return;
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    if (exclude.includes(entry.name)) continue;
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      copyDir(srcPath, destPath, exclude);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

if (require.main === module) {
  main().catch(e => {
    console.error('Fatal:', e.message);
    process.exit(1);
  });
}

module.exports = { AGENTS, installClaude, installCodex, installGrok, installCursor, installOpenCode, installGemini, installKimi, installQoder, installHermes };