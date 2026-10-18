# Platform specs — dated evidence table

Built from official platform pages only. Source of every row: `research/2026-09-05-advertising/official-specs.md` (web-researcher, 2026-09-05, fetch log there). A row is usable only while `expires` is in the future; after that it is `EXPIRED` and counts as `UNVERIFIED` until refreshed. A `UNVERIFIED` row is never filled from memory: the report says UNVERIFIED and names the web-researcher route.

Check before use (today from the shell, not from memory):
```
python -c "import datetime;print(datetime.date.today())"
```

## Refresh rule
- Every row expires 90 days after `retrieved`. Retrieved 2026-09-05 → expires 2026-12-04.
- Refresh = a web-researcher run over the source URLs below, official domains only (`support.google.com`, `developers.google.com`, `facebook.com/business`, `linkedin.com/help`, `outbrain.com/help`, Taboola's current help domain), rewriting this table with new `retrieved` and `expires` values and a new quoted sentence per row. Nothing else edits a number here.
- The P7 monthly job owns the refresh. Until it runs, an expired table is still not evidence.

## Text and asset limits

| platform | field | limit or rule (as stated) | source URL | retrieved | expires | confidence |
|---|---|---|---|---|---|---|
| google_rsa | headline | 3 min, 15 max; 30 chars each | https://support.google.com/google-ads/answer/7684791 | 2026-09-05 | 2026-12-04 | high |
| google_rsa | description | 2 min, 4 max; 90 chars each | https://support.google.com/google-ads/answer/7684791 | 2026-09-05 | 2026-12-04 | high |
| google_rsa | display_path | 15 chars each, two paths | https://support.google.com/google-ads/answer/7684791 | 2026-09-05 | 2026-12-04 | high |
| google_rsa | pinning | pin locks text to Headline position 1 or 2 or Description position 1 | https://support.google.com/google-ads/answer/7684791 | 2026-09-05 | 2026-12-04 | high |
| google_pmax | headline | 3–15; 30 chars max; include one of 15 chars or less | https://support.google.com/google-ads/answer/17091269 | 2026-09-05 | 2026-12-04 | high |
| google_pmax | long_headline | 1–5; 90 chars max | https://support.google.com/google-ads/answer/17091269 | 2026-09-05 | 2026-12-04 | high |
| google_pmax | description | 2–5; 90 chars max | https://support.google.com/google-ads/answer/17091269 | 2026-09-05 | 2026-12-04 | high |
| google_pmax | business_name | 25 chars max; matches domain or verified business name | https://support.google.com/google-ads/answer/17091269 | 2026-09-05 | 2026-12-04 | high |
| google_pmax | image | 1.91:1 min 600x314; 1:1 min 300x300; 4:5 min 480x600; up to 20 each; 5120 KB max | https://support.google.com/google-ads/answer/17091269 | 2026-09-05 | 2026-12-04 | high |
| google_pmax | logo | 1:1, 128x128 min, 1 required, up to 5 | https://support.google.com/google-ads/answer/17091269 | 2026-09-05 | 2026-12-04 | high |
| google_pmax | video | 10 seconds or more; up to 15 per orientation; auto-generated when none supplied | https://support.google.com/google-ads/answer/17091269 | 2026-09-05 | 2026-12-04 | high |
| google_demand_gen | headline | UNVERIFIED — the fetched page states image and video ratios only | https://support.google.com/google-ads/answer/13704860 | 2026-09-05 | 2026-12-04 | none |
| google_demand_gen | description | UNVERIFIED — same page, no text limit stated | https://support.google.com/google-ads/answer/13704860 | 2026-09-05 | 2026-12-04 | none |
| google_demand_gen | image | 1:1, 1.91:1, 4:5, 9:16 | https://support.google.com/google-ads/answer/13704860 | 2026-09-05 | 2026-12-04 | high |
| google_display | headline | 1–5; 30 chars or fewer | https://support.google.com/google-ads/answer/7005917 | 2026-09-05 | 2026-12-04 | high |
| google_display | long_headline | 90 chars or fewer | https://support.google.com/google-ads/answer/7005917 | 2026-09-05 | 2026-12-04 | high |
| google_display | description | 1–5 allowed; char cap UNVERIFIED on the fetched page | https://support.google.com/google-ads/answer/7005917 | 2026-09-05 | 2026-12-04 | none |
| meta_feed | primary_text | 50–150 chars recommended (recommendation, not a hard cap) | https://www.facebook.com/business/ads-guide/image/facebook-feed | 2026-09-05 | 2026-12-04 | high |
| meta_feed | headline | 27 chars recommended | https://www.facebook.com/business/ads-guide/image/facebook-feed | 2026-09-05 | 2026-12-04 | high |
| meta_feed | description | UNVERIFIED — not stated on the fetched page | https://www.facebook.com/business/ads-guide/image/facebook-feed | 2026-09-05 | 2026-12-04 | none |
| meta_feed | image | 4:5, 1440x1800 recommended | https://www.facebook.com/business/ads-guide/image/facebook-feed | 2026-09-05 | 2026-12-04 | high |
| meta_feed | video | UNVERIFIED — separate guide page, not fetched | https://www.facebook.com/business/ads-guide | 2026-09-05 | 2026-12-04 | none |
| linkedin_single_image | intro_text | up to 150 chars to avoid truncation; 600 max | https://www.linkedin.com/help/linkedin/answer/a426534 | 2026-09-05 | 2026-12-04 | high |
| linkedin_single_image | headline | up to 70 chars to avoid truncation | https://www.linkedin.com/help/linkedin/answer/a426534 | 2026-09-05 | 2026-12-04 | high |
| linkedin_single_image | description | up to 100 chars to avoid truncation | https://www.linkedin.com/help/linkedin/answer/a426534 | 2026-09-05 | 2026-12-04 | high |
| linkedin_single_image | image | 1.91:1 1200x628 recommended; 1:1 1200x1200; 4:5 720x900 | https://www.linkedin.com/help/linkedin/answer/a426534 | 2026-09-05 | 2026-12-04 | high |
| taboola_native | title | UNVERIFIED — help.taboola.com and taboola.com/help redirect to realize.com/help, off the official-domain list on 2026-09-05 | https://help.taboola.com | 2026-09-05 | 2026-12-04 | none |
| taboola_native | image | UNVERIFIED — same | https://help.taboola.com | 2026-09-05 | 2026-12-04 | none |
| outbrain_native | title | Standard Native 100 chars max, 60 recommended | https://www.outbrain.com/help/ads-specs/ | 2026-09-05 | 2026-12-04 | high |
| outbrain_native | image | Standard Native 1200x800 (3:2); App Install and Carousel 1:1 | https://www.outbrain.com/help/ads-specs/ | 2026-09-05 | 2026-12-04 | high |

Numeric limit per (platform, field), for `variants.json` and the check script. A field not listed here has no verified numeric limit; write `null` and mark the row UNVERIFIED.
```
google_rsa.headline 30 · google_rsa.description 90 · google_rsa.display_path 15
google_pmax.headline 30 · google_pmax.long_headline 90 · google_pmax.description 90 · google_pmax.business_name 25
google_display.headline 30 · google_display.long_headline 90
meta_feed.primary_text 150 (recommended) · meta_feed.headline 27 (recommended)
linkedin_single_image.intro_text 150 (truncation; 600 hard) · linkedin_single_image.headline 70 · linkedin_single_image.description 100
outbrain_native.title 100 (60 recommended)
```

## Measurement and linking (used by campaign-planner)

| topic | rule (as stated) | source URL | retrieved | expires | confidence |
|---|---|---|---|---|---|
| utm | utm_source, utm_medium, utm_campaign required; utm_term, utm_content optional | https://support.google.com/analytics/answer/1033863 | 2026-09-05 | 2026-12-04 | high |
| ga4_ads_link_prereq | admin access on Google Ads (or manager account), Edit on the GA4 property, auto-tagging on | https://support.google.com/google-ads/answer/7519537 | 2026-09-05 | 2026-12-04 | high |
| ga4_ads_link_steps | Google Ads: Tools → Data manager → Connect Product → GA4 & Firebase → select property → Link | https://support.google.com/google-ads/answer/7519537 | 2026-09-05 | 2026-12-04 | high |
| auto_tagging | auto-tagging appends the GCLID parameter to click URLs | https://support.google.com/google-ads/answer/3095550 | 2026-09-05 | 2026-12-04 | high |
| ga4_key_event_import | import GA4 key events into Google Ads from Conversions → Import (or GA4 Advertising → Conversion management); data then shared across both | https://support.google.com/google-ads/answer/10632359 | 2026-09-05 | 2026-12-04 | high |
| ga4_attribution_models | 3 models in GA4 Attribution reports: Data-driven, Paid and organic last click, Google paid channels last click | https://support.google.com/analytics/answer/10596866 | 2026-09-05 | 2026-12-04 | high |
| ads_conversion_action_types | Website, App, Phone call, Offline (import) | https://support.google.com/google-ads/answer/1722022 | 2026-09-05 | 2026-12-04 | high |
| ads_conversion_windows | defaults: click-through 30 days, view-through 1 day, engaged-view 3 days | https://support.google.com/google-ads/answer/3123169 | 2026-09-05 | 2026-12-04 | high |
| consent_mode | signals consent status for ad_storage, analytics_storage, ad_user_data, ad_personalization to Google tags | https://support.google.com/google-ads/answer/10000067 | 2026-09-05 | 2026-12-04 | high |
| consent_mode_v2_eea | ad_user_data and ad_personalization added on top of ad_storage and analytics_storage | https://support.google.com/google-ads/answer/13695607 | 2026-09-05 | 2026-12-04 | high |
| meta_attribution_window | UNVERIFIED — not fetched on 2026-09-05; treat Meta's reported window as whatever the account's column setting says, quoted from the export | — | 2026-09-05 | 2026-12-04 | none |

## Policy

| topic | rule (as stated) | source URL | retrieved | expires | confidence |
|---|---|---|---|---|---|
| google_misrepresentation | ads or destinations that deceive users by excluding relevant product information or providing misleading information are prohibited | https://support.google.com/adspolicy/answer/6020955 | 2026-09-05 | 2026-12-04 | high |
| google_testimonials | testimonials that claim specific results must include a visible disclaimer that there is no guarantee of specific results and that results can vary | https://support.google.com/adspolicy/answer/15936857 | 2026-09-05 | 2026-12-04 | high |
| meta_misleading_claims | UNVERIFIED — policy lives at transparency.meta.com/policies/ad-standards, not fetched; the on-domain help page returned no body | https://www.facebook.com/business/help/757209948405699 | 2026-09-05 | 2026-12-04 | none |
| meta_personal_attributes | UNVERIFIED — same; house rule applies regardless: never assert or imply a personal attribute of the reader (health, finances, religion, age, sexual orientation) | https://www.facebook.com/business/help/757209948405699 | 2026-09-05 | 2026-12-04 | none |
