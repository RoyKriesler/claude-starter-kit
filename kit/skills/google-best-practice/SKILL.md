---
name: google-best-practice
description: Dated reference of Google's own documentation for the analytics and Workspace stack - GA4 event and parameter rules and limits, sessions, data retention, attribution models, Google Ads conversion windows and enhanced conversions, UTM rules, consent mode parameters, Google Tag Manager and the data layer, the GA4 BigQuery export and its daily limit, BigQuery query practice and the eleven Google Cloud anti-patterns, Search Console report definitions, Looker Studio data freshness, Apps Script best practices, quotas and trigger restrictions, Sheets limits and functions, Drive roles and sharing, Calendar and Gmail API rules. Every row carries a source URL, a retrieved date, an expires date and a verbatim quote; a topic with no row is answered "not covered" and routed to the web-researcher agent, never from memory. Two-tier - this file is the map and the governance rules, references/details.md holds the rows; scripts/audit.py validates the rows and diffs two refreshes. Use when someone asks "what does Google say about", "GA4 event name rules", "how long is the conversion window", "which attribution models exist", "consent mode parameters", "BigQuery export limit", "is this a BigQuery anti-pattern", "Apps Script quota", "onEdit restrictions", "Drive roles", "cite the official doc", or Hebrew "מה גוגל אומרים על", "כללי שמות אירועים", "חלון המרה", "מודל ייחוס", "מגבלת", "תצטט את התיעוד הרשמי". Do NOT use to design an event taxonomy or review a query (analytics-engineer agent), to write Apps Script or drive the Google MCPs (google-workspace skill), to plan a campaign (campaign-planner agent), or to fetch a page that is not in the table (web-researcher agent, then refresh). Never states a limit, a window or a quota that has no row, never keeps an expired row as evidence.
---

# google-best-practice

A dated map of what Google's own pages say, for the agents and skills that must cite a platform fact: analytics-engineer, google-workspace, campaign-planner, marketing-analyst, ad-creative. This file is the navigation layer and holds the governance rules; `references/details.md` holds the evidence rows. Read a row, cite its id, URL and `retrieved` date. A fact with no row is not a fact.

Caller is the user, or a main session or another agent working for them. English: terse. Hebrew ask → Hebrew answer in clean prose, the row id, URL, quote and any Latin term on their own lines in a code block, never inside a Hebrew sentence.

# 0. Three laws

**Row or nothing.** A limit, a window, a default, a quota, a reserved name, a role capability: it comes from a row in `references/details.md` whose `expires` date is in the future, cited by id (`ga4-events-11`), URL and `retrieved` date, or the answer is `NOT COVERED` with the route `web-researcher`. Memory is not a source, however confident; the P3 digest found every public collection hallucinating GA4 limits and none citing a page. This file carries no limit value either, not even inside an excuse: a number written here would be quoted as if it were a row.

**Dates are checked, not assumed.** Before citing, run the date from the shell and compare with the row's `expires`; an expired row is `UNVERIFIED` and is reported as such with the refresh route. The audit script does this for the whole file: run it when in doubt, quote its last line.
```
python -c "import datetime;print(datetime.date.today())"
python "$HOME/.claude/skills/google-best-practice/scripts/audit.py" "$HOME/.claude/skills/google-best-practice/references/details.md"
```

**UNVERIFIED rows are pointers.** A row whose rule reads `UNVERIFIED` records that the official page was fetched and did not state the value; it carries the URL to fetch next, not a value. Cite it as the reason the answer is not covered, never as evidence for a number.

# 1. How to answer from the table

1. Find the section by topic in the map below; open `references/details.md` at that anchor; read the rows.
2. Quote the rule as stated, the row id, the URL, `retrieved`, `expires`. One row per fact. Two rows that corroborate (the same fact from two pages) may both be cited.
3. If the rows answer part of the question, answer that part and mark the rest `NOT COVERED` with what page the researcher should fetch (the `Not covered` list at the end of details.md names the pending URLs).
4. Say what the row does not say. A row that gives a default does not give the allowed range; a row that names the models does not give the default model.

Answer skeleton (English; Hebrew mirrors it with the Latin lines fenced):
```
Answer: <one sentence, the rule as stated>
Rows: <id> · <URL> · retrieved <date> · expires <date> · "<quote>"
Not covered: <topic> → web-researcher (<URL to fetch>)   (only if any)
```
When the answer is the audit script's output, the Rows line cites the script and its invocation (the output is not a row) and the UNVERIFIED ids go under Not covered.

# 2. Map of the sections in references/details.md

| anchor | covers | typical question |
|---|---|---|
| `#ga4-events` | event-name rules (start with a letter, letters numbers underscores, case sensitive, 40 chars), reserved prefixes and names, per-event and per-property limits, recommended vs automatically collected vs enhanced-measurement events, key events, session definition and 30-minute default, data retention 2 / 14 months | "can I call an event `Sign-Up`", "how many parameters per event", "what starts a session" |
| `#attribution` | GA4 attribution models available, DDA reattribution window, Google Ads models today (last click, data-driven) and the retired rule-based ones, click-through window default 30 days and its ranges, view-through default 1 day, engaged-view, enhanced conversions hashing, auto-tagging and GCLID, UTM required set and case sensitivity | "why do Ads and GA4 disagree", "what is the default conversion window", "which UTMs are required" |
| `#consent` | the four consent parameters, granted / denied values, basic vs advanced mode, the EEA obligation | "what does consent mode v2 require" |
| `#gtm` | container, tags, triggers, variables, preview and publish, Google tag vs GTM, data layer definition and the push pattern | "how do I pass a value to a tag", "is preview live" |
| `#bq-export` | daily vs streaming export, the 1 million events per day limit for standard properties and what happens above it, schema fields (event_params, event_date, user_pseudo_id) | "why did my export stop", "where are the parameters in BigQuery" |
| `#bigquery` | the eleven Google Cloud anti-patterns (SELECT *, semi-join without aggregation, CTE referenced more than twice, ORDER BY without LIMIT, REGEXP_CONTAINS over LIKE, ROW_NUMBER for latest record, dynamic predicates, WHERE order, join order, TEMP tables), performance and cost rules (projection, self-joins, ORDER BY placement, LIMIT does not cut bytes billed, preview instead of SELECT *, maximum bytes billed) | "is this query bad", "will LIMIT save money" |
| `#search-console` | performance report metric definitions, page-indexing report categories | "what is average position" |
| `#looker` | data-freshness defaults per connector (GA, BigQuery, Sheets); blends and connector quotas are pending | "how stale is the dashboard" |
| `#apps-script` | batch reads and writes, minimise service calls, Cache service, quotas (6 minutes per execution, trigger runtime per day, email recipients, URL fetches), simple-trigger restrictions (no authorised services, 30 seconds, not in read-only), installable triggers | "why does onEdit not send mail", "how long can a script run" |
| `#sheets` | 10 million cells and 18,278 columns, Docs and Slides size limits, QUERY, ARRAYFORMULA, IMPORTRANGE access grant and recalculation | "is the sheet too big", "why does IMPORTRANGE ask for access" |
| `#drive` | roles (owner, organizer, fileOrganizer, writer, commenter, reader) and their capabilities, Restricted vs Anyone with the link | "which role for read-only", "what does commenter allow" |
| `#calendar-gmail` | RFC3339 dateTime and the timeZone field, all-day `date`, attendees, reminders, one time zone for recurring events, a draft is not sent until `drafts.send`, `messages.send` RFC 2822 raw | "how do I set the time zone", "does creating a draft send it" |
| `#not-covered` | pending topics with the URL to fetch: custom-dimension limits, key-event counting method, lookback windows, Ads-vs-GA4 import mechanics, channel-group mapping, GTM versions / folders / limits, server-side tagging, Looker blends and GA4 Data API quotas, Search Console retention and Core Web Vitals thresholds, Drive default access for a new file | anything here → web-researcher |

# 3. Metric governance (this skill's rules, derived from the rows named)

Two valid definitions of the same word are common in this stack. Never put two on one surface without labelling both; never add figures measured under different rules. Derived from rows in `#attribution` (windows, models, retired models) and `#ga4-events` (session definition); the labels are this skill's convention, marked `house`.

| word | valid definitions | label each as | never |
|---|---|---|---|
| conversion rate | key events ÷ sessions (GA4, session-scoped); key events ÷ users (GA4, user-scoped); conversions ÷ clicks (Google Ads, click-through window, Ads model) | `session CVR (GA4)`, `user CVR (GA4)`, `click CVR (Ads, N-day click)` | one bare "conversion rate" when two are on the page |
| conversions | Google Ads conversions (Ads window and model, platform-reported); GA4 key events (GA4 attribution setting); orders in the system of record | `Ads conversions (30-day click, DDA)`, `GA4 key events (DDA)`, `orders (billing)` | summing across sources; comparing Ads to GA4 as one scale |
| ROAS | platform ROAS (platform conversions value ÷ platform spend); GA4 ROAS (GA4 purchase revenue by channel ÷ spend); blended ROAS (system-of-record revenue ÷ total spend) | `platform ROAS (window, model)`, `GA4 ROAS (model)`, `blended ROAS` | "channel X is 2× better than blended" across scopes |
| session | GA4 session (30-minute inactivity default, `session_start`) | `GA4 session` | equating with an Ads click or a CRM visit |
| attribution model | GA4: data-driven, paid and organic last click, Google paid channels last click; Ads: last click, data-driven; first click, linear, time decay, position-based retired in Ads | name the model beside every attributed figure | a rule-based Ads model that no longer exists |

Source of truth per question, this skill's convention: "how many" → the system of record; "which channel" → the source whose channel split is internally consistent (GA4 or CRM) with its coverage gap stated; platform figures are context, labelled platform-reported.

# 4. Naming conventions (house, not Google's)

Google states the event-name syntax (`#ga4-events` rows on characters, case, length, reserved prefixes) and nothing about style. The house convention, marked `house` when cited: GA4 custom events and parameters in `snake_case`, a verb-object name (`compare_products`, `save_search`), a recommended event used whenever one exists for the action, parameters named for what they hold (`product_id`, not `id`). GTM: `<type> - <platform> - <what>` for tags (`GA4 Event - Web - compare_products`), `<event or condition> - <where>` for triggers (`CE - compare_products - all pages`), `DLV - <key>` / `JS - <what>` / `CONST - <what>` for variables. A caller's convention overrides the house one; a name that breaks Google's syntax is rejected with the row cited.

# 5. Refresh (the P7 monthly job)

1. web-researcher run over the source URLs and the `Not covered` list, official domains only, WebFetch and `gh`, 0 firecrawl, the two-table shape in `research/<date>-analytics/official-docs*.md`.
2. Rebuild: `python scripts/build_details.py --out references/details.md --retrieved <date> <tables>`.
3. Diff against the previous build and record the changed rows in the refresh log: `python scripts/audit.py --diff OLD.md references/details.md`. The diff names the changed rows by section and topic, not the before and after text; grep both files for the row id to quote the two rules.
4. Validate: `python scripts/audit.py references/details.md` → `RESULT PASS`, 0 invalid, 0 expired.
5. Copy to the repo (`scripts/sync-from-claude.ps1`), commit with the row counts and the diff summary in the body.

Nothing else edits a value in `references/details.md`. A hand edit to a rule is a fabrication.

# 6. Rationalisations, pre-answered

| Excuse | Reality |
|---|---|
| "Everyone knows GA4 allows N event-scoped custom dimensions" | No row. `NOT COVERED`, route web-researcher with the pending URL. |
| "The row expired last week, the number will not have changed" | Expired is UNVERIFIED. Refresh, then cite. |
| "The Ads number and the GA4 number are close enough to add" | Different windows and models. Side by side, labelled, never summed. |
| "The page moved, I remember what it said" | Fetch the new page through web-researcher; a memory is not a row. |
| "Snake case is Google's rule" | Google states the syntax; the style is `house`. Cite both, marked. |
