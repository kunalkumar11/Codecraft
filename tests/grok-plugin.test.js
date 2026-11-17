#!/usr/bin/env node
// Grok Build loads Ponytail through its native skill system. Lifecycle-hook
// stdout is passive in Grok, so this adapter must not register any hooks.

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');

test('Grok manifest is a skill-only adapter with no lifecycle hooks', () => {
  const manifest = JSON.parse(fs.readFileSync(path.join(root, 'plugin.json'), 'utf8'));
  assert.equal(manifest.name, 'codecraft');
  assert.equal(manifest.hooks, undefined);
  assert.equal(manifest.mcpServers, undefined);
  assert.ok(!fs.existsSync(path.join(root, 'hooks', 'hooks.json')));
  assert.ok(!fs.existsSync(path.join(root, '.grok-plugin', 'hooks.json')));
});

test('Ponytail skill describes every coding task for Grok auto-invocation', () => {
  const skill = fs.readFileSync(path.join(root, 'skills', 'ponytail', 'SKILL.md'), 'utf8');
  assert.match(skill, /Use on any\s+coding task/i);
  assert.match(skill, /writing,\s+fixing, refactoring, reviewing/i);
  assert.doesNotMatch(skill, /disable-model-invocation:\s*true/i);
});

test('Grok marketplace resolves a subdirectory with the same skills as direct installation', () => {
  const catalog = JSON.parse(fs.readFileSync(path.join(root, '.grok-plugin', 'marketplace.json'), 'utf8'));
  const entry = catalog.plugins.find((plugin) => plugin.name === 'codecraft');
  const pluginRoot = path.resolve(root, entry.source);
  // Grok rejects a marketplace source of "./", even though direct installation works.
  assert.notEqual(pluginRoot, root, 'marketplace source must name a subdirectory');
  // The marketplace source points to skills/ directly (not a full plugin package),
  // so verify the skills directory exists and has the expected skills.
  assert.ok(fs.existsSync(pluginRoot), 'marketplace source directory must exist');
  assert.equal(path.resolve(pluginRoot), path.join(root, 'skills'), 'source must point to skills/');
  for (const name of ['codecraft', 'codecraft-review', 'codecraft-audit', 'codecraft-debt', 'codecraft-gain', 'codecraft-help', 'ponytail', 'ponytail-review', 'ponytail-audit', 'ponytail-debt', 'ponytail-gain', 'ponytail-help']) {
    assert.ok(fs.existsSync(path.join(pluginRoot, name, 'SKILL.md')), `${name} must ship in skills/`);
  }
});
