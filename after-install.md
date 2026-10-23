# CodeCraft for Hermes installed

The command starts in `full` mode. Set `CODECRAFT_DEFAULT_MODE=lite` before launching Hermes to change the default. The legacy `PONYTAIL_DEFAULT_MODE` variable is also accepted.

In shared gateways, restrict `/codecraft` to trusted users with Hermes slash-command access controls; runtime mode is process-local.

- `/codecraft [lite|full|ultra|off]`
- `/codecraft-review [target]`
- `/codecraft-audit [target]`
- `/codecraft-debt`
- `/codecraft-gain`
- `/codecraft-help`

The old `/ponytail*` commands and `ponytail:*` skills remain available for existing installs.
