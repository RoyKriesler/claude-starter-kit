# claude-starter-kit — maintainer notes

Public, sanitized export of Roy's Claude Code setup for family/friends. Windows-first.

## Hard rules
- PUBLIC repo. No personal data: no names, IDs, emails, employer names, merchant names, internal schemas, personal paths. Run the scan below before every push.
- Source of truth for agents/skills is `~/.claude` + `~/Projects/claude-config`; this repo is a derived copy. Re-export, then re-sanitize; never hand-edit here only.

## Pre-push scan
```bash
grep -rniE "roy|kriesler|roykr|global-e|globale|reichman|213099815|okta|clover|skims|harrods|@gmail|onedrive/" kit vault INSTALL.md README.md
```
Only allowed hit: the GitHub clone URL.
