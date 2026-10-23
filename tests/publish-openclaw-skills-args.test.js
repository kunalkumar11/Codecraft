'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const { buildPublishArgs, windowsCommand } = require('../scripts/publish-openclaw-skills-args');

test('publisher builds argv without a shell and preserves ClawHub metadata', () => {
  assert.deepEqual(buildPublishArgs('ponytail-review', '5.3.2', ['--dry-run']), [
    'skill', 'publish', '.openclaw/skills/ponytail-review',
    '--slug', 'ponytail-review', '--name', 'Ponytail Review', '--version', '5.3.2',
    '--tags', 'latest', '--dry-run',
  ]);
});

test('Windows shell command accepts the generated display name and rejects metacharacters', () => {
  assert.equal(windowsCommand('clawhub', ['--name', 'Ponytail Review']), 'clawhub --name "Ponytail Review"');
  for (const malicious of ['--name=$(whoami)', 'x&whoami', '%PATH%', 'a"b']) {
    assert.throws(() => windowsCommand('clawhub', [malicious]), /only accepts simple/);
  }
});

test('publisher rejects invalid slugs and package versions', () => {
  assert.throws(() => buildPublishArgs('../outside', '5.3.2'), /Unsafe OpenClaw skill slug/);
  assert.throws(() => buildPublishArgs('ponytail', '5.3.2 & whoami'), /Invalid package version/);
});
