#!/usr/bin/env node
// Every CodeCraft and compatibility command the pi extension registers must ship as a
// file-based command for the hosts that need one: Claude Code (commands/*.toml,
// which Gemini CLI reuses) and OpenCode (.opencode/command/*.md). /ponytail-help
// was advertised in the README and the help card but missing both files; this
// guards that drift -- a registered command with no adapter file fails here.

const test = require('node:test');
const assert = require('node:assert/strict');
const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');

// pi-extension registers the canonical command set.
const piSource = fs.readFileSync(path.join(root, 'pi-extension', 'index.js'), 'utf8');
const commands = [...new Set([
  ...[...piSource.matchAll(/registerCommand\(["']([\w-]+)["']/g)].map((m) => m[1]),
  ...(piSource.includes('["codecraft", "ponytail"]') ? ['codecraft', 'ponytail'] : []),
  ...['review', 'audit', 'debt', 'gain', 'help'].map((name) => `codecraft-${name}`),
])];

test('pi registers at least the base command', () => {
  assert.ok(commands.includes('codecraft'), 'expected pi to register /codecraft');
  assert.ok(commands.includes('ponytail'), 'expected pi to register a ponytail command');
});

test('every registered command ships a Claude commands/*.toml', () => {
  for (const name of commands) {
    assert.ok(
      fs.existsSync(path.join(root, 'commands', `${name}.toml`)),
      `missing commands/${name}.toml`,
    );
  }
});

test('every registered command ships an OpenCode .opencode/command/*.md', () => {
  for (const name of commands) {
    assert.ok(
      fs.existsSync(path.join(root, '.opencode', 'command', `${name}.md`)),
      `missing .opencode/command/${name}.md`,
    );
  }
});

test('CodeCraft command and skill aliases stay in sync with their legacy source', () => {
  const toCodeCraft = (text) => text.replaceAll('PONYTAIL', 'CODECRAFT')
    .replaceAll('Ponytail', 'CodeCraft').replaceAll('ponytail', 'codecraft');
  for (const prefix of ['ponytail', 'ponytail-review', 'ponytail-audit', 'ponytail-debt', 'ponytail-gain', 'ponytail-help']) {
    const alias = prefix.replace('ponytail', 'codecraft');
    assert.equal(
      fs.readFileSync(path.join(root, 'skills', alias, 'SKILL.md'), 'utf8'),
      toCodeCraft(fs.readFileSync(path.join(root, 'skills', prefix, 'SKILL.md'), 'utf8')),
      `${alias} skill must follow ${prefix}`,
    );
    assert.equal(
      fs.readFileSync(path.join(root, 'commands', `${alias}.toml`), 'utf8'),
      toCodeCraft(fs.readFileSync(path.join(root, 'commands', `${prefix}.toml`), 'utf8')),
      `${alias} command must follow ${prefix}`,
    );
    assert.equal(
      fs.readFileSync(path.join(root, '.opencode', 'command', `${alias}.md`), 'utf8'),
      toCodeCraft(fs.readFileSync(path.join(root, '.opencode', 'command', `${prefix}.md`), 'utf8')),
      `${alias} OpenCode command must follow ${prefix}`,
    );
  }
});

// /ponytail-debt documents one grep for the whole tree, shipped in four copies.
// It missed C-style /* ponytail: */ block comments (#810), so the ledger silently
// skipped every C/Java/CSS marker. Feed each shipped expression to real grep
// rather than restating it here: a copied regex only tests the copy.
const debtCopies = [
  'skills/ponytail-debt/SKILL.md',
  '.openclaw/skills/ponytail-debt/SKILL.md',
  'commands/ponytail-debt.toml',
  '.opencode/command/ponytail-debt.md',
];
const debtSamples = [
  ['# ponytail: hash marker', true],
  ['#ponytail: hash marker, no space', true],
  ['// ponytail: slash marker', true],
  ['//ponytail: slash marker, no space', true],
  ['/* ponytail: block marker, closed here */', true],
  ['/*ponytail: block marker, no space */', true],
  ['/* ponytail: block opener, closed some lines below', true],
  ['prose that merely mentions ponytail: markers stays out of the ledger', false],
];

test('every ponytail-debt copy pattern matches comment markers but not prose', () => {
  const input = debtSamples.map(([line]) => line).join('\n') + '\n';
  const expected = debtSamples.flatMap(([line, hit], i) => (hit ? [`${i + 1}:${line}`] : []));

  for (const rel of debtCopies) {
    const documented = fs.readFileSync(path.join(root, rel), 'utf8').match(/git grep [^']*-nE '([^']+)'/);
    assert.ok(documented, `${rel} no longer documents a git grep ... -nE '<pattern>'`);
    const actual = input.split(/\r?\n/).flatMap((line, index) =>
      line && new RegExp(documented[1]).test(line) ? [`${index + 1}:${line}`] : []);
    assert.deepEqual(actual, expected, `${rel} misses or over-matches markers`);
  }
});

// The full documented command must skip .git and whatever .gitignore ignores, in any stack (#948, #1100).
test('the ponytail-debt scan skips .git and ignored dirs like node_modules, dist, build and .next', (t) => {
  const command = fs.readFileSync(path.join(root, 'skills/ponytail-debt/SKILL.md'), 'utf8').match(/`(git grep [^`]+)`/);
  assert.ok(command, 'skill must document a git grep command');
  const documented = command[1].match(/^git grep (--no-index) (--exclude-standard) (-nE) '([^']+)'$/);
  assert.ok(documented, `unrecognized portable grep command: ${command[1]}`);
  const dir = fs.mkdtempSync(path.join(require('os').tmpdir(), 'ponytail-debt-'));
  let result;
  try {
    for (const sub of ['src', '.git', 'node_modules/pkg', 'dist', 'build', '.next']) {
      fs.mkdirSync(path.join(dir, sub), { recursive: true });
      fs.writeFileSync(path.join(dir, sub, 'a.js'), '// ponytail: marker\n');
    }
    fs.writeFileSync(path.join(dir, '.gitignore'), 'node_modules/\ndist/\nbuild/\n.next/\n');
    result = spawnSync('git', ['grep', documented[1], documented[2], documented[3], documented[4]], {
      cwd: dir, encoding: 'utf8', timeout: 5000,
    });
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
  if (result.error?.code === 'ENOENT') return t.skip('Git is required to run the documented git grep command');
  assert.equal(result.error, undefined, result.error?.message);
  assert.equal(result.status, 0, `git grep failed: ${result.stderr}`);
  assert.deepEqual(result.stdout.split('\n').filter(Boolean), ['src/a.js:1:// ponytail: marker']);
});
