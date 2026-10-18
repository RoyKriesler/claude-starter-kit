"""Build references/details.md from one or more web-researcher evidence tables.

    python build_details.py --out ../references/details.md --retrieved 2026-09-06 TABLE.md [TABLE.md ...]

Each input is a Markdown file holding one table with the columns
`area | topic | rule or value (as stated) | source URL | retrieved | quoted sentence | confidence`
(the shape the web-researcher writes) and optionally a `## Not found` list. Rows are regrouped into the
skill's fixed sections, an `expires` column (retrieved + 90 days) is added, and the Not-found items are
collected under "Not covered". Nothing here edits a value: a rule, a URL, a quote and a date are copied
as the researcher wrote them. Re-run by the P7 monthly refresh with the new tables and date.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path

SECTIONS = [
    ("ga4-events", "A. GA4 events, parameters, sessions, retention"),
    ("attribution", "B. Attribution, Google Ads conversion measurement, UTM"),
    ("consent", "C. Consent mode"),
    ("gtm", "D. Google Tag Manager and the data layer"),
    ("bq-export", "E. GA4 BigQuery export"),
    ("bigquery", "F. BigQuery query practice and anti-patterns"),
    ("search-console", "G. Search Console"),
    ("looker", "H. Looker Studio"),
    ("apps-script", "I. Apps Script"),
    ("sheets", "J. Sheets, Docs, Slides limits and functions"),
    ("drive", "K. Drive roles and sharing"),
    ("calendar-gmail", "L. Calendar and Gmail APIs"),
]

AREA_MAP = [
    (r"^GA4 events", "ga4-events"),
    (r"^GA4 attribution|^Google Ads attribution|^Google Ads measurement|^UTM", "attribution"),
    (r"^Consent", "consent"),
    (r"^GTM", "gtm"),
    (r"^GA4 BigQuery export", "bq-export"),
    (r"^BigQuery|^H6", "bigquery"),
    (r"^Search Console", "search-console"),
    (r"^Looker|^H5", "looker"),
    (r"^Apps Script|^H1", "apps-script"),
    (r"^H2", "sheets"),
    (r"^H3", "drive"),
    (r"^H4", "calendar-gmail"),
]


def split_row(line: str) -> list[str]:
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    cells = re.split(r"(?<!\\)\|", body)
    return [c.strip() for c in cells]


def parse(path: Path) -> tuple[list[list[str]], list[str]]:
    rows, notfound = [], []
    section = None
    for ln in path.read_text(encoding="utf-8").splitlines():
        if ln.startswith("## "):
            section = ln[3:].strip().lower()
            continue
        if section and section.startswith("not found"):
            if ln.strip().startswith("- "):
                notfound.append(ln.strip()[2:])
            continue
        if ln.startswith("|") and not ln.startswith("|---") and not ln.lower().startswith("| area"):
            cells = split_row(ln)
            if len(cells) == 7:
                rows.append(cells)
    return rows, notfound


def section_of(area: str) -> str:
    for pat, key in AREA_MAP:
        if re.search(pat, area):
            return key
    return "ga4-events"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("tables", nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--retrieved", required=True, help="YYYY-MM-DD of the research run")
    ap.add_argument("--sources", default="", help="comma-separated provenance paths to cite in the header")
    ap.add_argument("--drop-notfound", default="", help="'||'-separated substrings; a Not-found line containing one is dropped (covered by a later table)")
    a = ap.parse_args()
    ret = dt.date.fromisoformat(a.retrieved)
    exp = ret + dt.timedelta(days=90)

    grouped: dict[str, list[list[str]]] = {k: [] for k, _ in SECTIONS}
    notfound: list[str] = []
    for t in a.tables:
        rows, nf = parse(Path(t))
        for r in rows:
            grouped[section_of(r[0])].append(r)
        notfound.extend(nf)
    drops = [s for s in a.drop_notfound.split("||") if s]
    notfound = [x for x in notfound if not any(d in x for d in drops)]

    out = []
    out.append("# google-best-practice — details (dated evidence)")
    out.append("")
    out.append(f"Built {dt.date.today().isoformat()} from web-researcher tables retrieved {ret.isoformat()} "
               f"(official Google domains only). Every row expires {exp.isoformat()} (retrieved + 90 days); "
               "after that it counts as UNVERIFIED until the P7 monthly refresh rebuilds this file. "
               "A row whose rule reads UNVERIFIED was not stated on the fetched page: it is a pointer, not evidence.")
    if a.sources:
        out.append("")
        out.append("Provenance: " + ", ".join(f"`{s.strip()}`" for s in a.sources.split(",")))
    out.append("")
    out.append("Check today's date from the shell before using a row, never from memory:")
    out.append("```")
    out.append('python -c "import datetime;print(datetime.date.today())"')
    out.append("```")
    total = 0
    for key, title in SECTIONS:
        rows = grouped[key]
        out.append("")
        out.append(f"## {title} {{#{key}}}")
        out.append("")
        if not rows:
            out.append("_No rows yet. Route the question to web-researcher and add rows at the next refresh._")
            continue
        out.append("| id | topic | rule or value (as stated) | source URL | retrieved | expires | quoted sentence | confidence |")
        out.append("|---|---|---|---|---|---|---|---|")
        for i, r in enumerate(rows, 1):
            area, topic, rule, url, retrieved, quote, conf = r
            rid = f"{key}-{i:02d}"
            out.append(f"| {rid} | {topic} | {rule} | {url} | {retrieved} | {exp.isoformat()} | {quote} | {conf} |")
            total += 1
    out.append("")
    out.append("## Not covered (route to web-researcher, never answer from memory) {#not-covered}")
    out.append("")
    for nf in notfound:
        out.append(f"- {nf}")
    out.append("")
    out.append(f"Row count: {total}. Rebuild: `python scripts/build_details.py --out references/details.md --retrieved <date> <tables>`; "
               "validate: `python scripts/audit.py references/details.md`.")
    Path(a.out).write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"rows {total} notfound {len(notfound)} expires {exp.isoformat()} -> {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
