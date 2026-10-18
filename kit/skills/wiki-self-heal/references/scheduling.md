# Scheduling Self-Heal

Three recipes for running `wiki-self-heal` on a schedule. Pick one based on where the vault lives and how you operate.

## Recommended cadence

- **Active vaults** (daily/weekly ingest): **weekly** self-heal
- **Research vaults** (bursts of ingest): **on-demand** after each burst
- **Slow vaults**: **monthly**
- **Team / shared vaults**: weekly + after every batch merge

## Option 1 — macOS launchd (personal, local vault)

Create a launch agent at `~/Library/LaunchAgents/com.user.wiki-self-heal.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.user.wiki-self-heal</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>-lc</string>
    <string>cd /ABSOLUTE/PATH/TO/VAULT && claude "Run wiki-self-heal on this vault" > /tmp/wiki-heal.log 2>&1</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict>
    <key>Weekday</key><integer>0</integer>
    <key>Hour</key><integer>6</integer>
    <key>Minute</key><integer>0</integer>
  </dict>
  <key>StandardOutPath</key>
  <string>/tmp/wiki-heal.out</string>
  <key>StandardErrorPath</key>
  <string>/tmp/wiki-heal.err</string>
</dict>
</plist>
```

Load it:
```bash
launchctl load ~/Library/LaunchAgents/com.user.wiki-self-heal.plist
```

Runs every Sunday at 06:00 local time. Claude Code CLI must be installed and authenticated in the environment where launchd runs it.

### Simpler alternative — cron

```bash
crontab -e
```

Add:
```
0 6 * * 0 cd /ABSOLUTE/PATH/TO/VAULT && claude "Run wiki-self-heal on this vault" > /tmp/wiki-heal.log 2>&1
```

macOS cron works but launchd is the platform-native choice. Either is fine for personal use.

## Option 2 — GitHub Actions (cloud vaults, team wikis, vaults backed by a git remote)

`.github/workflows/self-heal.yml`:

```yaml
name: Wiki Self-Heal

on:
  schedule:
    - cron: '0 6 * * 0'  # Sundays 06:00 UTC
  workflow_dispatch:

permissions:
  contents: write
  pull-requests: write

jobs:
  heal:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Configure git
        run: |
          git config user.name "wiki-self-heal[bot]"
          git config user.email "bot@example.com"

      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Run self-heal
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude "Run wiki-self-heal on this vault. Do not merge. Leave the heal branch for PR review."

      - name: Push heal branch
        run: |
          git push origin "wiki-heal/$(date +%Y-%m-%d)" || true

      - name: Open PR
        run: |
          gh pr create \
            --title "Wiki self-heal — $(date +%Y-%m-%d)" \
            --body "Automated self-heal pass. Review the diff before merging." \
            --base main \
            --head "wiki-heal/$(date +%Y-%m-%d)" || true
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

Set `ANTHROPIC_API_KEY` as a repository secret. The workflow creates a PR for the heal branch — reviewer merges when satisfied.

## Option 3 — Claude Code scheduled triggers

If the user has configured Claude Code's built-in scheduler:

```bash
claude schedule create \
  --name "wiki-heal-weekly" \
  --cron "0 6 * * 0" \
  --prompt "Run wiki-self-heal on /absolute/path/to/vault"
```

Check the user's Claude Code version supports scheduled triggers before recommending this option. If it doesn't, fall back to launchd/cron (Option 1) or GitHub Actions (Option 2).

## First-run rule

**Always run `wiki-self-heal` manually at least once before automating.** Review the resulting heal branch. Merge it if satisfied. Only then set up the schedule.

Never schedule a skill you haven't run manually. This rule prevents silent corruption of the wiki by automation you never verified.

## Monitoring

For scheduled runs, add an alert/review habit:

- **macOS launchd/cron**: check `/tmp/wiki-heal.log` after each run for the first month. Once you trust it, read it less often.
- **GitHub Actions**: subscribe to workflow failure notifications; review the auto-opened PR each week.
- **Claude Code triggers**: review the branch in your editor when you start Monday's work.

The skill will never auto-merge. A stale unmerged heal branch is a signal you need to catch up on reviews.
