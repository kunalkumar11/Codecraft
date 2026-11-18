#!/usr/bin/env node
/**
 * CodeCraft Single-File Installer
 *
 * Usage: Download this file and run with Node.js
 *   curl -fsSL https://raw.githubusercontent.com/kunalkumar11/Codecraft/main/codecraft-install.js > codecraft-install.js
 *   node codecraft-install.js
 *
 * Or give this file to any AI coding agent (Claude Code, Codex, Grok, Cursor, etc.)
 * and ask it to run: node codecraft-install.js
 *
 * The installer detects your AI agent and installs CodeCraft automatically.
 */

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const os = require('os');
const https = require('https');

const REPO = 'kunalkumar11/Codecraft';
const BRANCH = 'main';
const VERSION = '5.3.2';

const AGENTS = {
  claude: {
    name: 'Claude Code (CLI + VS Code)',
    detect: () => checkCommand('claude') || checkCommand('claude-code') || fs.existsSync(path.join(os.homedir(), '.claude')),
    install: installClaude,
    configDir: () => path.join(os.homedir(), '.claude'),
  },
  codex: {
    name: 'Codex CLI / Desktop',
    detect: () => checkCommand('codex'),
    install: installCodex,
    configDir: () => path.join(os.homedir(), '.codex'),
  },
  grok: {
    name: 'Grok Build',
    detect: () => checkCommand('grok') || fs.existsSync(path.join(os.homedir(), '.grok')),
    install: installGrok,
    configDir: () => path.join(os.homedir(), '.grok'),
  },
  cursor: {
    name: 'Cursor',
    detect: () => checkCommand('cursor') || fs.existsSync(path.join(os.homedir(), '.cursor')),
    install: installCursor,
    configDir: () => path.join(os.homedir(), '.cursor'),
  },
  opencode: {
    name: 'OpenCode',
    detect: () => checkCommand('opencode'),
    install: installOpenCode,
    configDir: () => path.join(os.homedir(), '.config', 'opencode'),
  },
  gemini: {
    name: 'Gemini CLI',
    detect: () => checkCommand('gemini'),
    install: installGemini,
    configDir: () => path.join(os.homedir(), '.config', 'gemini'),
  },
  kimi: {
    name: 'Kimi Code',
    detect: () => fs.existsSync(path.join(os.homedir(), '.kimi')),
    install: installKimi,
    configDir: () => path.join(os.homedir(), '.kimi'),
  },
  qoder: {
    name: 'Qoder',
    detect: () => checkCommand('qoder') || fs.existsSync(path.join(os.homedir(), '.qoder')),
    install: installQoder,
    configDir: () => path.join(os.homedir(), '.qoder'),
  },
  hermes: {
    name: 'Hermes Agent',
    detect: () => fs.existsSync(path.join(os.homedir(), '.hermes')),
    install: installHermes,
    configDir: () => path.join(os.homedir(), '.hermes', 'plugins'),
  },
};

function checkCommand(cmd) {
  try {
    const result = spawnSync(cmd, ['--version'], { encoding: 'utf8', timeout: 3000 });
    return result.status === 0;
  } catch {
    return false;
  }
}

function downloadFile(url, dest) {
  return new Promise((resolve, reject) => {
    const request = https.get(url, (response) => {
      // Handle redirects
      if (response.statusCode === 302 || response.statusCode === 301) {
        const redirectUrl = response.headers.location;
        if (redirectUrl) {
          request.destroy();
          downloadFile(redirectUrl, dest).then(resolve).catch(reject);
          return;
        }
      }
      if (response.statusCode !== 200) {
        reject(new Error(`HTTP ${response.statusCode}`));
        return;
      }
      const file = fs.createWriteStream(dest);
      response.pipe(file);
      file.on('finish', () => file.close(resolve));
      file.on('error', (err) => { fs.unlink(dest, () => {}); reject(err); });
    }).on('error', reject);
    request.setTimeout(60000, () => {
      request.destroy();
      reject(new Error('Download timeout'));
    });
  });
}

async function downloadRepo() {
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'codecraft-'));
  // Use codeload.github.com directly to avoid redirect issues
  const zipUrl = `https://codeload.github.com/${REPO}/zip/refs/heads/${BRANCH}`;
  const zipPath = path.join(tmpDir, 'repo.zip');

  console.log(`Downloading CodeCraft from GitHub...`);
  await downloadFile(zipUrl, zipPath);

  // Extract using node's built-in or system unzip
  const extractResult = spawnSync('unzip', ['-q', zipPath, '-d', tmpDir], { encoding: 'utf8' });
  if (extractResult.status !== 0) {
    throw new Error('Failed to extract repository. Please install unzip or use npm install method.');
  }

  const extractedDir = fs.readdirSync(tmpDir).find(d => d.startsWith('Codecraft-') || d.startsWith('Codecraft'));
  return path.join(tmpDir, extractedDir);
}

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

async function installClaude(opts) {
  const { dryRun, force, root } = opts;
  const pluginDir = path.join(root, '.claude-plugin');
  const targetDir = path.join(os.homedir(), '.claude', 'plugins', 'codecraft');

  if (dryRun) {
    console.log(`  -> ${AGENTS.claude.name}: Would copy plugin to ${targetDir}`);
    return 'skipped';
  }

  fs.mkdirSync(targetDir, { recursive: true });
  copyDir(pluginDir, targetDir);

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

  console.log(`  [OK] ${AGENTS.claude.name}: Installed plugin + commands`);
  return true;
}

async function installCodex(opts) {
  const { dryRun, force, root } = opts;
  const pluginDir = path.join(root, '.codex-plugin');
  const targetDir = path.join(os.homedir(), '.codex', 'plugins', 'codecraft');

  if (dryRun) {
    console.log(`  -> ${AGENTS.codex.name}: Would copy plugin to ${targetDir}`);
    return 'skipped';
  }

  fs.mkdirSync(targetDir, { recursive: true });
  copyDir(pluginDir, targetDir);
  copyDir(path.join(root, 'skills'), path.join(targetDir, 'skills'));
  copyDir(path.join(root, 'hooks'), path.join(targetDir, 'hooks'));

  console.log(`  [OK] ${AGENTS.codex.name}: Installed plugin + skills + hooks`);
  return true;
}

async function installGrok(opts) {
  const { dryRun, force, root } = opts;
  const pluginDir = path.join(root, '.grok-plugin');
  const targetDir = path.join(os.homedir(), '.grok', 'plugins', 'codecraft');

  if (dryRun) {
    console.log(`  -> ${AGENTS.grok.name}: Would copy plugin to ${targetDir}`);
    return 'skipped';
  }

  fs.mkdirSync(targetDir, { recursive: true });
  copyDir(pluginDir, targetDir);
  copyDir(path.join(root, 'skills'), path.join(targetDir, 'skills'));

  console.log(`  [OK] ${AGENTS.grok.name}: Installed plugin + skills`);
  return true;
}

async function installCursor(opts) {
  const { dryRun, force, root, project } = opts;

  if (dryRun) {
    const target = project ? 'project .cursor/hooks.json' : 'global ~/.cursor/hooks.json';
    console.log(`  -> ${AGENTS.cursor.name}: Would run cursor-hooks.js install (${target})`);
    return 'skipped';
  }

  const script = path.join(root, 'scripts', 'cursor-hooks.js');
  const args = ['install'];
  if (project) args.push('--project');

  const result = spawnSync('node', [script, ...args], { cwd: root, encoding: 'utf8', timeout: 30000 });
  if (result.error) throw new Error(result.error.message);
  if (result.status !== 0) throw new Error(result.stderr || 'cursor-hooks.js failed');

  const rulesDir = project ? path.join(process.cwd(), '.cursor', 'rules') : path.join(os.homedir(), '.cursor', 'rules');
  fs.mkdirSync(rulesDir, { recursive: true });
  fs.copyFileSync(path.join(root, '.cursor', 'rules', 'codecraft.mdc'), path.join(rulesDir, 'codecraft.mdc'));

  console.log(`  [OK] ${AGENTS.cursor.name}: Installed hooks${project ? ' (project)' : ' (global)'} + rules`);
  return true;
}

async function installOpenCode(opts) {
  const { dryRun, force, root } = opts;
  const pluginDir = path.join(root, '.opencode', 'plugins');
  const targetDir = path.join(os.homedir(), '.config', 'opencode', 'plugins', 'codecraft');

  if (dryRun) {
    console.log(`  -> ${AGENTS.opencode.name}: Would copy plugin to ${targetDir}`);
    return 'skipped';
  }

  fs.mkdirSync(targetDir, { recursive: true });
  copyDir(pluginDir, targetDir);

  console.log(`  [OK] ${AGENTS.opencode.name}: Installed plugin (V1+V2 compatible)`);
  return true;
}

async function installGemini(opts) {
  const { dryRun, force, root } = opts;
  const targetDir = path.join(os.homedir(), '.config', 'gemini', 'extensions', 'codecraft');

  if (dryRun) {
    console.log(`  -> ${AGENTS.gemini.name}: Would install extension to ${targetDir}`);
    return 'skipped';
  }

  fs.mkdirSync(targetDir, { recursive: true });
  copyDir(path.join(root, 'skills'), path.join(targetDir, 'skills'));
  copyDir(path.join(root, 'commands'), path.join(targetDir, 'commands'));
  fs.copyFileSync(path.join(root, 'AGENTS.md'), path.join(targetDir, 'AGENTS.md'));

  console.log(`  [OK] ${AGENTS.gemini.name}: Installed extension`);
  return true;
}

async function installKimi(opts) {
  const { dryRun, force, root } = opts;
  const pluginDir = path.join(root, '.kimi-plugin');
  const targetDir = path.join(os.homedir(), '.kimi', 'plugins', 'codecraft');

  if (dryRun) {
    console.log(`  -> ${AGENTS.kimi.name}: Would copy plugin to ${targetDir}`);
    return 'skipped';
  }

  fs.mkdirSync(targetDir, { recursive: true });
  copyDir(pluginDir, targetDir);
  copyDir(path.join(root, 'skills'), path.join(targetDir, 'skills'));
  fs.copyFileSync(path.join(root, 'AGENTS.md'), path.join(targetDir, 'AGENTS.md'));

  console.log(`  [OK] ${AGENTS.kimi.name}: Installed plugin + skills + AGENTS.md`);
  return true;
}

async function installQoder(opts) {
  const { dryRun, force, root } = opts;
  const pluginDir = path.join(root, '.qoder-plugin');
  const targetDir = path.join(os.homedir(), '.qoder', 'plugins', 'codecraft');

  if (dryRun) {
    console.log(`  -> ${AGENTS.qoder.name}: Would copy plugin to ${targetDir}`);
    return 'skipped';
  }

  fs.mkdirSync(targetDir, { recursive: true });
  copyDir(pluginDir, targetDir);
  copyDir(path.join(root, 'skills'), path.join(targetDir, 'skills'));
  copyDir(path.join(root, '.qoder', 'rules'), path.join(targetDir, '.qoder', 'rules'));
  copyDir(path.join(root, 'hooks'), path.join(targetDir, 'hooks'));

  console.log(`  [OK] ${AGENTS.qoder.name}: Installed plugin + skills + rules + hooks`);
  return true;
}

async function installHermes(opts) {
  const { dryRun, force, root } = opts;
  const targetDir = path.join(os.homedir(), '.hermes', 'plugins', 'codecraft');

  if (dryRun) {
    console.log(`  -> ${AGENTS.hermes.name}: Would copy plugin to ${targetDir}`);
    return 'skipped';
  }

  fs.mkdirSync(targetDir, { recursive: true });
  copyDir(root, targetDir, ['node_modules', '.git', 'benchmarks', 'examples', 'assets', 'tests', 'scripts', 'docs']);

  console.log(`  [OK] ${AGENTS.hermes.name}: Installed plugin (full repo copy)`);
  return true;
}

async function main() {
  const args = process.argv.slice(2);
  const opts = {
    dryRun: args.includes('--dry-run') || args.includes('-n'),
    agents: args.includes('--agent') || args.includes('-a')
      ? args[args.indexOf('--agent') !== -1 ? args.indexOf('--agent') + 1 : args.indexOf('-a') + 1].split(',')
      : null,
    project: args.includes('--project') || args.includes('-p'),
    force: args.includes('--force') || args.includes('-f'),
    list: args.includes('--list') || args.includes('-l'),
    help: args.includes('--help') || args.includes('-h'),
  };

  if (opts.help) {
    console.log(`
CodeCraft Single-File Installer v${VERSION}

Usage: node codecraft-install.js [options]

Options:
  --dry-run, -n       Show what would be installed without making changes
  --agent, -a <list>  Comma-separated list of agents to install (default: all detected)
  --project, -p       For Cursor: install to project .cursor/ instead of global
  --force, -f         Overwrite existing installations
  --list, -l          List all supported agents and detection status
  --help, -h          Show this help

Examples:
  node codecraft-install.js                    # Install for all detected agents
  node codecraft-install.js --dry-run          # Preview what would happen
  node codecraft-install.js -a claude,codex    # Install only for Claude and Codex
  node codecraft-install.js -p                 # Cursor project-level install
`);
    return;
  }

  console.log(`\n=== CodeCraft Single-File Installer v${VERSION}\n`);

  // Download repo if not running from a local checkout
  let root = __dirname;
  if (!fs.existsSync(path.join(root, '.claude-plugin'))) {
    console.log('-> Not running from a local checkout -> downloading CodeCraft from GitHub...');
    root = await downloadRepo();
    console.log(`   Downloaded to: ${root}\n`);
  }

  // Detect available agents
  const detected = {};
  for (const [key, agent] of Object.entries(AGENTS)) {
    const available = agent.detect();
    detected[key] = { ...agent, available };
    const status = available ? '[OK] detected' : '[--] not found';
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
    console.log('\n[--] No agents selected or detected. Use --agent to specify manually.\n');
    process.exit(1);
  }

  console.log(`\n-> Installing for: ${targets.map(t => AGENTS[t].name).join(', ')}`);
  if (opts.dryRun) console.log('   (dry run - no changes will be made)\n');

  const results = { success: [], failed: [], skipped: [] };

  for (const key of targets) {
    const agent = detected[key];
    if (!agent.available && !opts.force) {
      console.log(`  [!]  ${agent.name}: not detected (use --force to install anyway)`);
      results.skipped.push(key);
      continue;
    }

    try {
      const result = await agent.install({ ...opts, root, version: VERSION });
      if (result === 'skipped') {
        results.skipped.push(key);
      } else if (result) {
        results.success.push(key);
      } else {
        results.failed.push(key);
      }
    } catch (e) {
      console.log(`  [X] ${agent.name}: ${e.message}`);
      results.failed.push(key);
    }
  }

  // Summary
  console.log('\n=== Summary:');
  if (results.success.length) console.log(`  [OK] Installed: ${results.success.map(k => AGENTS[k].name).join(', ')}`);
  if (results.skipped.length) console.log(`  [!]  Skipped: ${results.skipped.map(k => AGENTS[k].name).join(', ')}`);
  if (results.failed.length) console.log(`  [X] Failed: ${results.failed.map(k => AGENTS[k].name).join(', ')}`);

  // Generic AGENTS.md copy instruction for rule-only agents
  const ruleOnlyAgents = ['windsurf', 'cline', 'aider', 'kiro', 'zed', 'codewhale', 'copilot', 'junie', 'amp', 'jules'];
  console.log('\n-> For other agents (Windsurf, Cline, Aider, Kiro, Zed, CodeWhale, Copilot, Junie, Amp, Jules):');
  console.log(`   Copy AGENTS.md to your project root or global config:`);
  console.log(`   cp ${path.join(root, 'AGENTS.md')} <project>/AGENTS.md`);

  if (opts.dryRun) {
    console.log('\n-> Run without --dry-run to apply changes.\n');
  } else {
    console.log('\n[OK] Done! Restart your agent to pick up the changes.\n');
  }

  if (results.failed.length) process.exit(1);
}

main().catch(e => {
  console.error('Fatal:', e.message);
  process.exit(1);
});