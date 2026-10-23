# Changelog

## Local derivative update — 2026-10-23

- Introduced the CodeCraft display identity, an original SVG mark, architecture and development guides, and an explicit upstream attribution statement. Existing Ponytail integration names remain for compatibility.
- Made the correctness benchmark independent of Pandas, moved child execution off shell command strings, used private temporary workspaces, limited inherited environment variables, and guaranteed temporary-file cleanup.
- Made the Hermes gateway parser accept whitespace-delimited arguments and safely ignore empty slash commands.
- Made session import skip transcripts whose escaped working-directory value is malformed.
- Added regression checks for the dependency-free CSV benchmark, temporary cleanup, malformed transcript paths, and Hermes command parsing.
- Added cross-platform process-tree timeout handling for agentic benchmark workers and made benchmark helper tests portable across Windows and Unix.
- Fixed POSIX cleanup to kill the process group by its original ID after the parent has exited, preventing surviving background children.
- Added the dependency-free Python source auditor, structured severity findings, JSON export, a sample project, and unit tests.
- Made unreadable Python directories visible as medium-severity scan findings instead of silently omitting them.
- Guarded the inherited npm publisher so only the canonical upstream repository can use its OIDC publishing job; expanded CI to Ubuntu, macOS, and Windows.
- Documented generic checkout installation, runtime configuration, architecture, limitations, and the missing local Git identity/remote.
