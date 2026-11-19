// OpenCode 2 loads this file automatically from .opencode/plugins/ and does not
// read codecraft.mjs next to it, so keep the one-line entry here. npm consumers
// never see it: package.json main/exports still point at codecraft.mjs.
export { default } from './codecraft.mjs'