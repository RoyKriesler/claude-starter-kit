#!/usr/bin/env python
"""Validation gate for scraped datasets. Used by the web-scraper agent before it may report success.

Usage:
  python validate_dataset.py FILE [--key col1,col2] [--expect-rows N] [--tolerance 0.05]
                                  [--date-cols a,b] [--numeric-cols c,d] [--allow-constant e,f]
                                  [--hebrew-cols g] [--dedup-out FILE] [--json]

Checks, all mandatory unless the flag says otherwise:
  1. File readable (parquet / csv / json / jsonl), UTF-8.
  2. Row count > 0, and within tolerance of --expect-rows when given.
  3. No column entirely null.
  4. No column with a single distinct value, unless listed in --allow-constant.
  5. Duplicates on --key: counted, removed, rewritten to --dedup-out (or in place) when given.
  6. --date-cols parse as ISO 8601 (YYYY-MM-DD or full timestamp) for every non-null value.
  7. --numeric-cols are numeric dtype, not object/string.
  8. Hebrew round-trip: for --hebrew-cols (or auto-detected columns containing Hebrew letters),
     write the file back to a temp path, read it again, compare values exactly.
Exit code 0 = PASS, 1 = FAIL. Prints a JSON report with --json, otherwise a short text report.
"""
import argparse
import json
import os
import re
import sys
import tempfile

import pandas as pd

HEBREW = re.compile(r"[֐-׿]")
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}([T ]\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:?\d{2})?)?$")


def read_any(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".parquet":
        return pd.read_parquet(path)
    if ext == ".csv":
        return pd.read_csv(path, encoding="utf-8")
    if ext == ".jsonl":
        return pd.read_json(path, lines=True, encoding="utf-8")
    if ext == ".json":
        return pd.read_json(path, encoding="utf-8")
    raise ValueError(f"unsupported extension {ext}")


def write_any(df, path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".parquet":
        df.to_parquet(path, index=False)
    elif ext == ".csv":
        df.to_csv(path, index=False, encoding="utf-8")
    elif ext == ".jsonl":
        df.to_json(path, orient="records", lines=True, force_ascii=False)
    elif ext == ".json":
        df.to_json(path, orient="records", force_ascii=False)
    else:
        raise ValueError(f"unsupported extension {ext}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--key", default="")
    ap.add_argument("--expect-rows", type=int, default=None)
    ap.add_argument("--tolerance", type=float, default=0.05)
    ap.add_argument("--date-cols", default="")
    ap.add_argument("--numeric-cols", default="")
    ap.add_argument("--allow-constant", default="")
    ap.add_argument("--hebrew-cols", default="")
    ap.add_argument("--dedup-out", default="")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    split = lambda s: [c.strip() for c in s.split(",") if c.strip()]
    key, date_cols, num_cols = split(a.key), split(a.date_cols), split(a.numeric_cols)
    allow_const, heb_cols = set(split(a.allow_constant)), split(a.hebrew_cols)

    report = {"file": a.file, "checks": [], "status": "PASS"}

    def check(name, ok, detail=""):
        report["checks"].append({"check": name, "ok": bool(ok), "detail": detail})
        if not ok:
            report["status"] = "FAIL"

    try:
        df = read_any(a.file)
        check("readable", True, f"{len(df)} rows x {len(df.columns)} cols")
    except Exception as e:
        check("readable", False, f"{type(e).__name__}: {e}")
        return finish(report, a.json)

    n = len(df)
    check("rows_nonzero", n > 0, f"{n}")

    # list / dict / array cells are unhashable; compare them by their string form
    def hashable(col):
        return col.map(lambda v: str(v) if isinstance(v, (list, dict, tuple)) or hasattr(v, "__array__") else v)

    all_null = [c for c in df.columns if df[c].isna().all()]
    check("no_all_null_columns", not all_null, ", ".join(all_null) or "none")

    const = [c for c in df.columns if c not in allow_const and hashable(df[c]).nunique(dropna=True) <= 1 and n > 1]
    check("no_constant_columns", not const, ", ".join(const) or "none")

    if key:
        missing = [k for k in key if k not in df.columns]
        if missing:
            check("dedup_key_exists", False, f"missing key columns {missing}")
        else:
            before = n
            keyframe = df[key].apply(hashable)
            dupmask = keyframe.duplicated()
            dups = int(dupmask.sum())
            df = df[~dupmask]
            check("dedup", True, f"{dups} duplicates removed on {key}, {before} -> {len(df)}")
            if a.dedup_out:
                write_any(df, a.dedup_out)
            elif dups:
                write_any(df, a.file)
    else:
        check("dedup_key_declared", False, "no --key given; declare a dedup key")

    # row expectation is judged after dedup, on what will actually be delivered
    if a.expect_rows is not None:
        n2 = len(df)
        lo, hi = a.expect_rows * (1 - a.tolerance), a.expect_rows * (1 + a.tolerance)
        check("rows_vs_expected", lo <= n2 <= hi, f"got {n2} after dedup, expected {a.expect_rows} ±{a.tolerance:.0%}")

    for c in date_cols:
        if c not in df.columns:
            check(f"date_iso:{c}", False, "column missing")
            continue
        vals = df[c].dropna().astype(str)
        bad = vals[~vals.str.match(ISO_DATE)]
        check(f"date_iso:{c}", bad.empty, f"{len(bad)} non-ISO values, e.g. {bad.head(3).tolist()}" if not bad.empty else "all ISO 8601")

    for c in num_cols:
        if c not in df.columns:
            check(f"numeric:{c}", False, "column missing")
            continue
        check(f"numeric:{c}", pd.api.types.is_numeric_dtype(df[c]), str(df[c].dtype))

    if not heb_cols:
        heb_cols = [c for c in df.columns if df[c].dtype == object and df[c].dropna().astype(str).str.contains(HEBREW).any()]
    if heb_cols:
        ext = os.path.splitext(a.file)[1]
        tmp = os.path.join(tempfile.gettempdir(), f"roundtrip_{os.getpid()}{ext}")
        try:
            write_any(df, tmp)
            back = read_any(tmp)
            same = all(df[c].fillna("").astype(str).tolist() == back[c].fillna("").astype(str).tolist() for c in heb_cols)
            check("hebrew_roundtrip", same, f"cols {heb_cols}")
        except Exception as e:
            check("hebrew_roundtrip", False, f"{type(e).__name__}: {e}")
        finally:
            try:
                os.remove(tmp)
            except OSError:
                pass
    else:
        check("hebrew_roundtrip", True, "no Hebrew columns detected, skipped")

    report["rows"] = int(len(df))
    report["schema"] = {c: str(t) for c, t in df.dtypes.items()}
    report["sample"] = json.loads(df.head(5).to_json(orient="records", force_ascii=False, date_format="iso"))
    return finish(report, a.json)


def finish(report, as_json):
    if as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"{report['status']}  {report['file']}")
        for c in report["checks"]:
            print(f"  [{'ok' if c['ok'] else 'XX'}] {c['check']}: {c['detail']}")
        if "schema" in report:
            print("  schema:", report["schema"])
    sys.exit(0 if report["status"] == "PASS" else 1)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
