'use strict';

const safeCommandToken = /^[A-Za-z0-9_./:@+-]+$/;
const safeDisplayName = /^[A-Za-z][A-Za-z ]*$/;

function buildPublishArgs(slug, version, passthrough = []) {
  if (!/^[a-z0-9][a-z0-9-]*$/.test(slug)) throw new Error(`Unsafe OpenClaw skill slug: ${slug}`);
  if (!/^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$/.test(version)) {
    throw new Error(`Invalid package version: ${version}`);
  }
  return [
    'skill', 'publish', `.openclaw/skills/${slug}`,
    '--slug', slug,
    '--name', slug.split('-').map((word) => word.charAt(0).toUpperCase() + word.slice(1)).join(' '),
    '--version', version,
    '--tags', 'latest',
    ...passthrough,
  ];
}

function windowsCommand(executable, args) {
  const quote = (arg) => {
    if (safeCommandToken.test(arg)) return arg;
    if (safeDisplayName.test(arg)) return `"${arg}"`;
    throw new Error(`Windows publishing only accepts simple, unquoted CLI arguments; rejected: ${arg}`);
  };
  return [executable, ...args].map(quote).join(' ');
}

module.exports = { buildPublishArgs, windowsCommand };
