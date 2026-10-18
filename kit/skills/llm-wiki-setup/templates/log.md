# Wiki Log

Chronological, append-only. One entry per operation.

Format:
```
## [YYYY-MM-DD] <op> | <title>
```

Operations: `ingest`, `query`, `lint`, `update`, `init`.

Utility: `grep "^## \[" wiki/log.md | tail -5` returns the last 5 operations.

---

## [{{DATE}}] init | wiki created

Wiki initialized with the `llm-wiki-setup` skill. Layout: `{{LAYOUT}}`.

Ready to ingest. Drop a source into `raw/` and ask: "Ingest the new source I just added."
