"""Self-audit for references/details.md, and a refresh diff between two builds.

    python audit.py DETAILS.md                 validate: every row has a topic, a rule, an https source URL,
                                               a retrieved date, an expires date; expiry against today; UNVERIFIED count
    python audit.py DETAILS.md --json          same, as one JSON object
    python audit.py --diff OLD.md NEW.md       rows keyed by (section, topic): added / removed / rule changed /
                                               retrieved date changed; exit 0 always for --diff

Exit 0 when every row is valid and none has expired; 1 when any row is invalid or expired (the invalid rows
are listed, one per line, as `INVALID <id> <reason>` / `EXPIRED <id> <expires>`). A row whose rule column
reads UNVERIFIED is valid (it carries its reason) but is counted and listed as `UNVERIFIED <id>`.
Today comes from the clock, or from --today YYYY-MM-DD for a reproducible check.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def split_row(line: str) -> list[str]:
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", body)]


def load(path: Path) -> list[dict]:
    rows, section = [], ""
    for ln in path.read_text(encoding="utf-8").splitlines():
        if ln.startswith("## "):
            m = re.search(r"\{#([\w-]+)\}", ln)
            section = m.group(1) if m else ln[3:].strip()
            continue
        if ln.startswith("|") and not ln.startswith("|---") and not ln.lower().startswith("| id"):
            c = split_row(ln)
            if len(c) >= 8:
                rows.append({"section": section, "id": c[0], "topic": c[1], "rule": c[2], "url": c[3],
                             "retrieved": c[4], "expires": c[5], "quote": c[6], "confidence": c[7]})
            else:
                rows.append({"section": section, "id": c[0] if c else "?", "malformed": True, "ncols": len(c)})
    return rows


def validate(rows: list[dict], today: dt.date) -> dict:
    invalid, expired, unverified = [], [], []
    for r in rows:
        if r.get("malformed"):
            invalid.append((r["id"], f"malformed row, {r['ncols']} columns"))
            continue
        why = []
        if not r["topic"]:
            why.append("no topic")
        if not r["rule"]:
            why.append("no rule")
        if not re.match(r"^https?://", r["url"]) and not r["url"].startswith("github.com/"):
            why.append("no source URL")
        if not DATE.match(r["retrieved"]):
            why.append("no retrieved date")
        if not DATE.match(r["expires"]):
            why.append("no expires date")
        if why:
            invalid.append((r["id"], "; ".join(why)))
            continue
        if dt.date.fromisoformat(r["expires"]) < today:
            expired.append((r["id"], r["expires"]))
        if r["rule"].upper().startswith("UNVERIFIED"):
            unverified.append(r["id"])
    return {"rows": len(rows), "invalid": invalid, "expired": expired, "unverified": unverified,
            "today": today.isoformat(), "valid": not invalid and not expired}


def diff(old: list[dict], new: list[dict]) -> dict:
    key = lambda r: (r["section"], r["topic"])
    o = {key(r): r for r in old if not r.get("malformed")}
    n = {key(r): r for r in new if not r.get("malformed")}
    added = sorted(k for k in n if k not in o)
    removed = sorted(k for k in o if k not in n)
    rule_changed, date_changed = [], []
    for k in sorted(set(o) & set(n)):
        if o[k]["rule"] != n[k]["rule"]:
            rule_changed.append(k)
        if o[k]["retrieved"] != n[k]["retrieved"]:
            date_changed.append(k)
    return {"added": added, "removed": removed, "rule_changed": rule_changed, "retrieved_changed": date_changed,
            "old_rows": len(o), "new_rows": len(n)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("details", nargs="?")
    ap.add_argument("--diff", nargs=2, metavar=("OLD", "NEW"))
    ap.add_argument("--today")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.diff:
        d = diff(load(Path(a.diff[0])), load(Path(a.diff[1])))
        if a.json:
            print(json.dumps(d, ensure_ascii=False, indent=1))
        else:
            print(f"old_rows {d['old_rows']} new_rows {d['new_rows']}")
            for name in ("added", "removed", "rule_changed", "retrieved_changed"):
                print(f"{name} {len(d[name])}")
                for k in d[name]:
                    print(f"  {name.upper()} {k[0]} :: {k[1]}")
        return 0
    if not a.details:
        ap.error("DETAILS.md or --diff OLD NEW")
    today = dt.date.fromisoformat(a.today) if a.today else dt.date.today()
    v = validate(load(Path(a.details)), today)
    if a.json:
        print(json.dumps(v, ensure_ascii=False, indent=1))
    else:
        print(f"rows {v['rows']} invalid {len(v['invalid'])} expired {len(v['expired'])} unverified {len(v['unverified'])} today {v['today']}")
        for rid, why in v["invalid"]:
            print(f"INVALID {rid} {why}")
        for rid, exp in v["expired"]:
            print(f"EXPIRED {rid} {exp}")
        for rid in v["unverified"]:
            print(f"UNVERIFIED {rid}")
        print("RESULT", "PASS" if v["valid"] else "FAIL")
    return 0 if v["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
