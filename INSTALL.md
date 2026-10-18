# INSTALL — instructions for Claude Code

You are Claude Code on the owner's **Windows** machine. The owner pasted a one-line request asking you to install this kit. Do the whole install yourself, end to end. The owner should not need to do anything except approve tool permissions and any Windows admin (UAC) prompt.

Work in Git Bash unless a step says PowerShell. Use `$HOME` (e.g. `/c/Users/<name>`). Keep a running checklist and report at the end.

## Ground rules

- **Back up before overwriting.** Anything that already exists in `~/.claude` (CLAUDE.md, settings.json, an agent or skill with the same name) is copied to `~/.claude/backups/starter-kit-<YYYYMMDD-HHMMSS>/` first.
- **Never delete** the owner's existing files, notes or vault content. Merge, don't replace.
- If a step fails, try one alternative, then mark it SKIPPED with the reason and continue. Do not stop the whole install for an optional step.
- Do not sign the owner up for any service, enter any password, or spend money.

## 0. Get the kit

```bash
KIT="$HOME/.claude-starter-kit"
if [ -d "$KIT/.git" ]; then git -C "$KIT" pull --ff-only; else git clone --depth 1 https://github.com/RoyKriesler/claude-starter-kit.git "$KIT"; fi
```

If `git` is missing, install prerequisites (step 1) first, then come back.

## 1. Prerequisites (winget, PowerShell)

Check each with `--version`; install only what is missing:

```powershell
winget install --id Git.Git -e --accept-source-agreements --accept-package-agreements
winget install --id Python.Python.3.12 -e --accept-source-agreements --accept-package-agreements
winget install --id OpenJS.NodeJS.LTS -e --accept-source-agreements --accept-package-agreements
winget install --id GitHub.cli -e --accept-source-agreements --accept-package-agreements
winget install --id Obsidian.Obsidian -e --accept-source-agreements --accept-package-agreements
```

New PATH entries need a fresh shell; call tools by full path if needed (`$LOCALAPPDATA/Programs/Python/Python312/python.exe`).

Python packages for the agents' render gate and document skills:

```bash
python -m pip install --upgrade pip
python -m pip install python-docx python-pptx openpyxl pymupdf pandas pyarrow playwright pywin32 requests beautifulsoup4
python -m playwright install chromium
```

## 2. Agents, skills, scripts, hooks

```bash
TS=$(date +%Y%m%d-%H%M%S); BK="$HOME/.claude/backups/starter-kit-$TS"; mkdir -p "$BK" ~/.claude/{agents,skills,scripts,hooks}
for kind in agents skills scripts hooks; do
  for src in "$KIT/kit/$kind"/*; do
    dst="$HOME/.claude/$kind/$(basename "$src")"
    [ -e "$dst" ] && { mkdir -p "$BK/$kind"; cp -R "$dst" "$BK/$kind/"; rm -rf "$dst"; }
    cp -R "$src" "$dst"
  done
done
```

Expected: 11 agents, 14 skills, 2 scripts, 1 hook.

## 3. Global CLAUDE.md

- If `~/.claude/CLAUDE.md` does not exist: copy `kit/CLAUDE.md` there.
- If it exists: back it up, then append the kit file under a line `# --- Starter kit (installed <date>) ---`, removing kit sections that duplicate the owner's own rules. The owner's existing rules win on conflict.
- Leave `{{NAME}}` and `{{ROLE}}` for step 9.

## 4. settings.json (deep merge)

Read `kit/settings.fragment.json`. Replace `{{HOME_FORWARD_SLASHES}}` with the home path in forward-slash form (`C:/Users/<name>`). Deep-merge into `~/.claude/settings.json` (create `{}` if missing): append the hook to any existing `UserPromptSubmit` list, add plugins and marketplaces, set `autoMemoryDirectory`. Do not change `permissions`, `model` or any other existing key. Validate the result with `python -m json.tool`.

## 5. Plugins

```bash
claude plugin marketplace add anthropics/skills
claude plugin marketplace add https://github.com/MiniMax-AI/skills.git
claude plugin install document-skills@anthropic-agent-skills
claude plugin install example-skills@anthropic-agent-skills
claude plugin install minimax-skills@minimax-skills
```

If the CLI subcommands are unavailable, the `enabledPlugins` + `extraKnownMarketplaces` entries from step 4 install them on the next Claude Code start; note that in the report.

Optional third-party skill: `ui-ux-pro-max` from https://github.com/nextlevelbuilder/ui-ux-pro-max-skill — follow its README to put the skill folder at `~/.claude/skills/ui-ux-pro-max/`. SKIP on any failure.

## 6. Obsidian vault

Target: `$HOME/ObsidianVault`.

- If it does not exist: `cp -R "$KIT/vault" "$HOME/ObsidianVault"` and delete the `.gitkeep` files.
- If it exists: copy only files and folders that are missing; never overwrite. If the existing vault has its own `CLAUDE.md`, save the kit one as `CLAUDE.kit.md` and mention it in the report.

Obsidian settings (create `.obsidian/` inside the vault if missing; merge if the files exist):

- `.obsidian/daily-notes.json` → `{"folder":"04_Notes_Daily","template":"00_Index/Templates/daily-note","format":"YYYY-MM-DD"}`
- `.obsidian/templates.json` → `{"folder":"00_Index/Templates"}`
- `.obsidian/core-plugins.json` → make sure `daily-notes`, `templates`, `backlink`, `graph`, `outline`, `file-explorer`, `global-search` are enabled.

Community plugins — for each id below, look up its GitHub repo in `https://raw.githubusercontent.com/obsidianmd/obsidian-releases/master/community-plugins.json`, download `main.js`, `manifest.json` and `styles.css` (if present) from the repo's latest release into `.obsidian/plugins/<id>/`, then write all installed ids to `.obsidian/community-plugins.json`:

```
dataview
templater-obsidian
calendar
periodic-notes
obsidian-tasks-plugin
omnisearch
obsidian-rtl
obsidian-git
```

Register the vault so Obsidian opens it directly: if Obsidian is not running, add an entry to `%APPDATA%/obsidian/obsidian.json` under `vaults` with a random 16-hex id, `"path"` = the vault's Windows path with escaped backslashes, `"ts"` = now in ms, `"open": true` (create the file if missing, keep existing vaults).

Do not register the recurring Task Scheduler jobs; mention them as optional in the report (they spend Claude usage every day).

## 7. Memory

```bash
MEM="$HOME/ObsidianVault/05_Resources/Claude Code/memory"; mkdir -p "$MEM"
for f in "$KIT"/kit/memory/*.md; do b=$(basename "$f"); [ "$b" = MEMORY.md ] && [ -e "$MEM/$b" ] && continue; [ -e "$MEM/$b" ] || cp "$f" "$MEM/"; done
```

Merge `kit/memory/MEMORY.md`: create it if missing, else append only the lines whose file is not already listed.

## 8. Verify (quote the outputs in the report)

```bash
ls ~/.claude/agents | wc -l          # >= 11
ls ~/.claude/skills | wc -l          # >= 14
python -m json.tool ~/.claude/settings.json > /dev/null && echo settings OK
echo '{"prompt":"שלום"}' | powershell -NoProfile -ExecutionPolicy Bypass -File "$(cygpath -w ~/.claude/hooks/hebrew-language-rule.ps1)"   # prints HEBREW DETECTED
python ~/.claude/scripts/render_check.py --help | head -3
ls "$HOME/ObsidianVault/00_Index" && ls "$HOME/ObsidianVault/05_Resources/Claude Code/memory" | wc -l
```

## 9. Profile and report

1. Ask the owner, in one AskUserQuestion call (Hebrew if they wrote in Hebrew): their name, and what they do (job or studies). Fill `{{NAME}}` and `{{ROLE}}` in `~/.claude/CLAUDE.md`. If they skip, leave the placeholders — never invent.
2. Write a vault note `04_Notes_Daily/<today>.md` (from the daily-note template) and one line in `00_Index/log.md`: `## [<today>] init | Starter kit installed`.
3. Final report to the owner, in the language they used, following the Hebrew rules if Hebrew: what was installed, what was SKIPPED and why, where backups are.
4. Tell them the two things only they can do:
   - Restart Claude Code so the new agents, hook and memory path load.
   - Open Obsidian once; if it asks "Trust author and enable plugins?", click Trust.
5. Optional next steps to offer: register the daily / nightly / weekly vault jobs (`00_Index/Scripts/run-job.ps1`), install Firecrawl, connect Gmail / Drive / Calendar connectors in claude.ai settings.
