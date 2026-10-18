---
name: python-data
description: General-purpose Python for data analysis, scripting, and feature engineering — pandas, numpy, polars, pathlib, requests, sqlalchemy. Use when the user wants to load, clean, transform, aggregate, join, or analyze tabular data in Python; build a one-off script; or wire Python into a Cursor / VS Code workflow. Distinct from `web-scraper` (HTTP/HTML extraction) and `firecrawl-*` (web search/scrape via API). Triggers on "pandas", "dataframe", "numpy", "polars", "Jupyter", "merge these CSVs", "clean this data", "feature engineering", "Python script", "Cursor".
---

# Python — Data & Scripting

General-purpose Python for the kind of work the user does outside scraping: tabular analysis, feature engineering for fraud patterns, and quick scripts that glue tools together.

## When to use

- Loading CSV / parquet / xlsx into a dataframe and answering a question about it.
- Cleaning, deduping, joining, or pivoting data.
- Feature engineering for fraud patterns (velocity windows, entity linking, rolling aggregations).
- One-off scripts (rename files, batch-convert formats, hit an API in a loop).
- Wiring Python into a Cursor workflow — `.py` modules imported across a project.

## When NOT to use

- Web scraping → `firecrawl-scrape` or `firecrawl-search`.
- Statistical modeling in R → use Desktop's `r-statistics` skill.
- Heavy ML training → out of scope; defer to a notebook-focused workflow.

## Defaults

### Stack

| Need | Library |
|---|---|
| Tabular small/medium (< 5M rows) | `pandas` |
| Tabular large (5M–500M rows, single machine) | `polars` |
| Arrays / vectorized math | `numpy` |
| Reading parquet | `pyarrow` (via pandas/polars) |
| Reading xlsx | `openpyxl` (read) or `xlsxwriter` (write) |
| HTTP | `httpx` (sync or async) over `requests` for new code |
| SQL | `sqlalchemy` 2.x with `pandas.read_sql` or `polars.read_database` |
| CLI args | `argparse` for simple, `typer` for ergonomics |
| Env / paths | `pathlib.Path` (never raw strings) |
| Config | `pydantic-settings` or plain `os.getenv` for one-offs |

### Style

- Python 3.11+. Use match-case, type hints, and the walrus where they read clearly.
- `from __future__ import annotations` at the top of multi-class files.
- Type hints on function signatures; not on every local var.
- f-strings always. No `%` or `.format()`.
- `pathlib.Path` for any path. No string concatenation with `/` or `os.path.join` in new code.

### File layout

For a one-off script:

```
script.py
```

For a small project in Cursor:

```
project/
├── pyproject.toml         # uv, ruff, mypy config
├── src/
│   └── pkg/
│       ├── __init__.py
│       ├── io.py          # loaders
│       ├── features.py    # transformations
│       └── pipeline.py    # main entry point
├── tests/
└── data/                  # gitignored
```

Use `uv` for dependency management — `uv add pandas`, `uv run python pipeline.py`.

## Pandas idioms the user should use

### Read with explicit dtypes

```python
import pandas as pd

dtypes = {
    "order_id": "string",
    "customer_id": "string",
    "amount_usd": "float64",
    "merchant_id": "category",
}
df = pd.read_csv("orders.csv", dtype=dtypes, parse_dates=["created_at"])
```

Explicit dtypes prevent surprises later. `category` for low-cardinality string columns saves memory.

### Chain, don't reassign

```python
result = (
    df
    .loc[df["amount_usd"] > 100]
    .assign(amount_log=lambda d: np.log1p(d["amount_usd"]))
    .groupby("merchant_id", observed=True)
    .agg(n=("order_id", "size"), avg=("amount_usd", "mean"))
    .reset_index()
    .sort_values("n", ascending=False)
)
```

Readable, immutable, easy to comment-out steps.

### Velocity windows for fraud patterns

```python
df = df.sort_values(["customer_id", "created_at"])
df["orders_last_1h"] = (
    df.groupby("customer_id")["created_at"]
      .transform(lambda s: s.rolling("1h", on=s).count())
)
```

For large data, switch to polars — `polars` rolling on groups is ~10× faster.

### Entity linking via shared fields

```python
# orders linked by any shared field: ship_addr, device_id, email_normalized
import networkx as nx

G = nx.Graph()
for col in ["ship_addr", "device_id", "email_normalized"]:
    for val, group in df.groupby(col):
        for a, b in zip(group["order_id"], group["order_id"].iloc[1:]):
            G.add_edge(a, b, via=col)

clusters = list(nx.connected_components(G))
df["cluster_id"] = df["order_id"].map(
    {o: i for i, c in enumerate(clusters) for o in c}
)
```

## Anti-patterns

- `iterrows()` on dataframes > 10k rows. Vectorize or use `apply` over `numpy`/`polars`.
- `df[df["x"] == y]` chained when `df.query("x == @y")` reads better.
- Mutating in place (`df["new"] = ...`) inside a function that takes `df` as input — return a new frame or document the side effect.
- Wide `try / except Exception:` blocks. Catch the specific error.
- `print()` for logging. Use `logging` with a configured handler.

## Cursor / VS Code workflow

- Install the Python and Ruff extensions.
- Configure `ruff` in `pyproject.toml`:

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "SIM"]
```

- Use `# %%` cell markers in `.py` files to run inline in Cursor (Python: Jupyter integration).
- Type-check with `mypy --strict` or `pyright` on shipped code.

## References

- pandas docs: `pandas.pydata.org/docs`
- polars user guide: `pola.rs/posts` and `docs.pola.rs`
- McKinney's *Python for Data Analysis*, 3rd ed. — canonical for pandas.
- VanderPlas's *Python Data Science Handbook* — free online.
