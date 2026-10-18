---
name: obsidian-cli
description: Interact with Obsidian vaults using the Obsidian CLI to read, create, search, and manage notes, tasks, properties, and more. Also supports plugin and theme development with commands to reload plugins, run JavaScript, capture errors, take screenshots, and inspect the DOM. Use when the user asks to interact with their Obsidian vault, manage notes, search vault content, perform vault operations from the command line, or develop and debug Obsidian plugins and themes. Detects whether the `obsidian` CLI is actually on PATH before issuing any command, and falls back to direct vault file edits plus `qmd query` search if it is absent.
---

# Obsidian CLI

## Step 0 — detect the CLI

Before running any `obsidian` command, confirm the CLI is actually present. Do not assume it exists just because Obsidian is installed.

**PowerShell:**
```powershell
Get-Command obsidian -ErrorAction SilentlyContinue
```

**Other shells:**
```bash
where.exe obsidian
```

If the command is absent, stop. Do not fabricate `obsidian` command output or pretend a call succeeded. Print this pointer:

> Obsidian CLI not found on PATH. Requires Obsidian desktop ≥ 1.8 with the CLI enabled: Settings → General → Command line interface, then restart the shell for PATH to pick it up.

Then fall back to:
- Direct file edits in the vault at `$HOME/ObsidianVault`. New notes go in `00_Raw/` unless the user names a folder; frontmatter dates are ISO `YYYY-MM-DD`; write UTF-8.
- `qmd query` for searching vault content

If the two detection commands disagree, trust `Get-Command`: it resolves the same PATH the session will use.

### Rule: never touch `.obsidian/`

Never edit files under `.obsidian/` (plugin and config state, e.g. `community-plugins.json`, `app.json`, theme CSS snippets) through this skill — neither via the CLI nor via direct file edit. Refuse and point the user to the Obsidian settings UI instead.

## Command reference (requires the CLI, see Step 0)

Use the `obsidian` CLI to interact with a running Obsidian instance. Requires Obsidian to be open.

## Command reference

Run `obsidian help` to see all available commands. This is always up to date. Full docs: https://help.obsidian.md/cli

## Syntax

**Parameters** take a value with `=`. Quote values with spaces:

```bash
obsidian create name="My Note" content="Hello world"
```

**Flags** are boolean switches with no value:

```bash
obsidian create name="My Note" silent overwrite
```

For multiline content use `\n` for newline and `\t` for tab. Frontmatter can be embedded inline in `content=` as a leading `---` block; if the CLI rejects it, create the note first and set each property with `property:set`.

## File targeting

Many commands accept `file` or `path` to target a file. Without either, the active file is used.

- `file=<name>` — resolves like a wikilink (name only, no path or extension needed)
- `path=<path>` — exact path from vault root, e.g. `folder/note.md`

## Vault targeting

Commands target the most recently focused vault by default. Use `vault=<name>` as the first parameter to target a specific vault:

```bash
obsidian vault="My Vault" search query="test"
```

## Common patterns

```bash
obsidian read file="My Note"
obsidian create name="New Note" content="# Hello" template="Template" silent
obsidian append file="My Note" content="New line"
obsidian search query="search term" limit=10
obsidian daily:read
obsidian daily:append content="- [ ] New task"
obsidian property:set name="status" value="done" file="My Note"
obsidian tasks daily todo
obsidian tags sort=count counts
obsidian backlinks file="My Note"
```

Use `--copy` on any command to copy output to clipboard. Use `silent` to prevent files from opening. Use `total` on list commands to get a count.

## Plugin development

### Develop/test cycle

After making code changes to a plugin or theme, follow this workflow:

1. **Reload** the plugin to pick up changes:
   ```bash
   obsidian plugin:reload id=my-plugin
   ```
2. **Check for errors** — if errors appear, fix and repeat from step 1:
   ```bash
   obsidian dev:errors
   ```
3. **Verify visually** with a screenshot or DOM inspection:
   ```bash
   obsidian dev:screenshot path=screenshot.png
   obsidian dev:dom selector=".workspace-leaf" text
   ```
4. **Check console output** for warnings or unexpected logs:
   ```bash
   obsidian dev:console level=error
   ```

### Additional developer commands

Run JavaScript in the app context:

```bash
obsidian eval code="app.vault.getFiles().length"
```

Inspect CSS values:

```bash
obsidian dev:css selector=".workspace-leaf" prop=background-color
```

Toggle mobile emulation:

```bash
obsidian dev:mobile on
```

Run `obsidian help` to see additional developer commands including CDP and debugger controls.
