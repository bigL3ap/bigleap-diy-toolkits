# Paid Media DIY Toolkits: build notes (Draft v1)

Owner: **Scott Smoot** (CTA "Talk to Scott about building it"). Built Oct 19, 2026 from the Agency Brands Bi-Weekly call.
Three single-file HTML tools, no external requests, matching the RevOps series shell (`toolkits/revops/01_Is_Every_Lead_Reaching_Your_CRM.html`).

| # | File | Title | Deliverable |
|---|---|---|---|
| 1 | `01_What_Kind_of_Business_Are_You.html` | What Kind of Business Are You? | Business Profile card + `BL1.` code + campaign-type fit + "Your DIY path" across all series |
| 2 | `02_Is_Your_Google_Ads_Account_Ready.html` | Is Your Google Ads Account Ready? | Your Launch Readiness List (OK/gap in build order, steps, time) |
| 3 | `03_Which_Campaigns_Should_You_Run_First.html` | Which Campaigns Should You Run First? | Your Campaign Starter Plan (campaigns, budget split, structure, negatives, 30 days, what not to turn on) |

## What each tool does

**01 Business Profile Builder (the shared start for every series).** This is Dallas's "drag and drop your deliverable from toolkit one" idea. Eight questions cover every field in the shared schema. The tool saves the profile to `localStorage` (`bl_diy_profile_v1`) once the answers stop being the example answers. Example answers are not saved unless the visitor clicks "Save to this browser". It also prints a copyable `BL1.` code for other devices. On the results side it shows:
- **Campaign types**: one line each, marked Fits, Maybe or Not yet. The types are Search, Performance Max / Shopping, Local and location assets, App, and Demand Gen / YouTube.
- **Your DIY path**: an ordered, reasoned list of toolkits across paid, tracking, seo, pr and revops, built from the LINKS map. The first three are marked "Do first".
- **Special-rule callout**: a "talk to Scott, special rules apply" panel for auto dealers, legal, healthcare/pharma, finance, and housing/employment/credit. These are matched against the industry text.

**02 Readiness / gap check.** This is Coby's "gap audit": what they have vs. what paid needs before spending a dollar. The checks run in build order:
- Account, admin access and billing owned by you, not an agency
- Tag Manager, GA4, a conversion action that fires, GA4 linked, auto-tagging
- Google Business Profile, if they have locations
- Merchant Center plus the Shopify Google & YouTube app, if they sell products online
- The landing page has one clear action and is fast on mobile
- CRM, or a CRM-to-Google Ads import for B2B or lead-gen businesses
- An app SDK, if they have an app
- Budget sanity

The headline counts the **gaps that would waste spend**. Account and Merchant Center gaps are listed as launch blockers and are not counted in the red number.

**03 Campaign starter plan.** This turns the profile into:
- The first one or two campaigns
- A budget split shown as ranges, monthly and daily
- A "start tight, then open up" structure: exact/phrase match only, up to 3 ad groups with one landing page each, tight geo, no Display or search partners, and Maximize clicks until conversions record
- Negative keyword starter categories
- Weekly checks for the first 30 days
- What NOT to turn on yet: broad match / AI Max, Display and partners, auto-applied recommendations, targets from day one, PMax URL expansion, Dynamic Search Ads and optimized targeting

## Questions → what they feed

| Toolkit | Question | Feeds |
|---|---|---|
| 01 | Name (optional), industry (list + free text) | Card; special-vertical callout (regex in `SPECIAL_VERTICALS`) |
| 01 | Sells to (B2B/B2C/both) | Path (leadCapture, pipelineDash), complex flags (mixed, offline) |
| 01 | Products/services → online checkout (Shopify/other/none) | PMax/Shopping fit, feed complexity |
| 01 | Visit in person (none/one/multi) → reach | Local fit, `local` toolkit, multi-location complexity, intl complexity |
| 01 | CRM (HubSpot/other/none) | leadCapture, offline-import complexity, pipelineDash |
| 01 | Main goal | Every fit line; path order (conversions, speedToLead, prReady/mediaKit) |
| 01 | Monthly ad budget | Demand Gen fit threshold; carried to 02/03 |
| 01 | Quick checks: website, app, GA4, GTM, Google Business Profile | Search fit, App fit, `tracking` link, path order |
| 02 | Business rows (prefilled from profile) | Which checks appear (GBP, Merchant Center, CRM import, SDK) |
| 02 | Account ownership | Item 1 (launch blocker) |
| 02 | GTM / GA4 / GA4 link / auto-tagging | Items 2, 3, 5, 6 |
| 02 | Conversion action fires | Item 4 (wastes spend) |
| 02 | Landing page action + mobile speed | Items 9, 10 (waste spend) |
| 02 | Conditional: GBP, Merchant Center, CRM import, SDK | Items 7, 8, 11, 12 |
| 02 | Budget | Item 13 (wastes spend under $1,000/mo) |
| 03 | Business rows, goal, reach, budget (prefilled) | Campaign choice, split, targeting text |
| 03 | Lines to advertise | Ad group count (max 3) |
| 03 | People search your name? | Whether a brand campaign is the second campaign |
| 03 | Conversion tracking tested? | Bidding advice, "fix tracking first" warning, next link |

## Results order (all three)
Headline (one sentence, at most one red number) → named deliverable → Where it gets complex (sorted, "Applies to you" chips) → closing panel. The closing panel has Copy my plan, the Talk to Scott CTA, Next toolkit, and cross-links filtered by the answers. 02 and 03 also have "How we calculate this" listing every rule of thumb.

## Logic and assumptions (all in `ASSUMPTIONS` at the top of each script)
- 01: `videoMinBudget` $3,000/mo before Demand Gen moves from "not yet" to "maybe" (non-B2B). `smallBudget` $1,000.
- 02: `minBudget` $1,000/mo counts as "ready" for one Search campaign. Daily budget ≥ 10× expected CPC. 14–30 days before judging. "Not sure" counts as a gap.
- 03: one campaign under $1,500/mo. Main/secondary split 70–85% / 15–30%. Brand campaign 10–20%. Standard Shopping instead of PMax under $1,500. Up to 3 ad groups, 5–15 keywords each. About 30 conversions in 30 days before a tCPA/tROAS target. Raise budget 15–20% in week 4 if efficient.
- Campaign choice (03): installs+app → App. Sales+store → PMax (or Standard Shopping when small). Visits+location → Search with location assets (+ PMax for store goals at $3k+). Calls → Search with call assets. Awareness → Demand Gen. Otherwise → Search (+ location assets if they have locations). The second campaign is brand Search unless they said nobody searches the name.
- Every number is labeled a rule of thumb. No invented statistics. The only external benchmark cited is Google's own ~2.5s LCP guidance.

## Where it sends people next
- 01 → 02 (always next).
- 02 → 03.
- 03 → 02 if conversions are not confirmed, else tracking 01.

Cross-links follow spec §5:
- No/unsure GA4 or GTM → `tracking`
- Conversion not tested, or CRM import missing → `conversions` (+ `leadCapture`)
- Locations → `local`
- Slow page → `seoBasics`
- Lead or call goals → `speedToLead`
- B2B → `pipelineDash`
- Awareness → `prReady` / `mediaKit`

Footer links `hub` (`../../index.html`). All links are relative and open in the same tab. The CTA alone opens in a new tab (external site).

## Shared Business Profile
The helper is inlined verbatim (`encodeProfile`, `decodeProfile`, `loadProfile`, `saveProfile`, `clearProfile`, key `bl_diy_profile_v1`).
- **02/03 profile strip**: shows "Using your Business Profile: <name or industry> · <model> · <reach>" with Change/Clear, or the build link plus a collapsed "Paste a profile code" field. Prefilled answers get a "From your profile" tag that disappears when the visitor changes that answer.
- **01 strip**: says when a saved profile was loaded ("Start fresh" clears it), or offers to paste a code.
- `LABELS`, `SPECIAL_VERTICALS` and `detectSpecial()` sit in the common script block. Other series can copy them if they want the same wording.

## Settings to edit before launch
- `CTA_URL` in all three files: swap for Scott's scheduler link.
- `OWNER` if a co-owner is added.
- `ASSUMPTIONS` values once Scott confirms them (see open questions).
- `SPECIAL_VERTICALS` regex list (01, and copied into 02/03) if Scott wants more or fewer flagged industries.
- Sources are kept in the scratchpad (`paid-src/`: `build.py`, `p1–p3.py/.js`, `common.js`, `header.js`, `base.css`, `extra.css`). Editing the HTML directly is fine too, because each page is self-contained.

## Source material used
- Fathom: "Agency Brands Bi-Weekly SEO/Content/PPC/RevOps Call - October 19" (0:00–14:00). Scott's variables:
  - product vs. lead gen vs. service
  - locations and Google Business Profile
  - lead form and funnel
  - conversion tracking and GTM
  - B2B CRM sending MQL/SQL/closed-won back to Google Ads
  - Shopify integration
  - app install campaigns with Kochava/AppsFlyer
  - car dealerships as a special case
  
  Also from the call: Dallas's profile-builder idea, Coby's gap audit, and Scott's "link to tracking, don't digress".
- Scott's other Fathom calls (generalized, no client names): "start tight, then open up" with exact match, high-intent keywords and one landing page per ad group; launch blocked until the conversion was wired in GTM and the HubSpot ↔ Google Ads integration re-authorized; PMax tiers by margin via a Shopify supplemental feed, pausing DSA / broad AI Max at first; app-install tracking via Firebase/AppsFlyer and event taxonomy.
- Template: RevOps toolkits 01 and 05 (Dallas Olsen).

## Open questions for Scott
1. What minimum monthly ad budget should the toolkits call "ready"? (Draft: $1,000 for one Search campaign; $1,500 for a second.)
2. Is the default split right? (Draft: 70–85% main campaign, brand Search 10–20%.)
3. Which verticals should be hard-routed to "talk to Scott" instead of getting a plan? (Draft flags auto, legal, healthcare/pharma, finance, housing/employment/credit, but still shows the plan.)
4. Should auto dealers get their own path (vehicle ads / inventory feeds) in v2, or stay "talk to an expert" only?
5. Do Meta Ads and Microsoft Ads belong in v2 (a "Which platform first?" step), or stay Google-only?
6. Is Standard Shopping under $1,500/mo the right call vs. starting PMax for everyone with a feed?
7. Should a brand Search campaign be a default second campaign, or only when brand search volume is proven?
8. What is your meeting scheduler link for `CTA_URL`?
9. Should "Not sure" on a check count as a gap that wastes spend (current draft), or a separate "verify" state?
10. Which CRM-to-Google Ads stages do you want us to recommend by default (MQL, SQL, closed-won), and with what values?
11. Is ~30 conversions in 30 days the threshold you use before setting tCPA/tROAS?
12. Should Performance Max for leads ever be a "fits" for service businesses in v1, or always "not yet"?
13. Who co-owns the tracking links these tools send people to (Alex suggested)? It affects the expert name shown on the path.
14. Should the profile also capture creative assets (logo, images, video) and ICP, per Coby's gap-audit list, for a v2 readiness check?
15. Dallas's follow-up idea: should submitting a profile trigger a "how did it go?" check-in from you? It would need a form/HubSpot hook. These pages send nothing today.

## QA run (Oct 19, 2026)
- Bundled Chromium at 320 light, 390 dark, 768 light, 1024 light, 1280 light and 1920 dark: no horizontal overflow and no console errors on all three. Screenshots are in `scratchpad/qa/paid-0N-*.png`.
- Edge inputs tested: blank budget, negative, 99,999,999,999, HTML in the business name (escaped), every goal in 03, profile save → prefill in 02/03 → Clear → paste code → reload. No NaN/undefined/null text on screen or in copied plans.
- Copy my plan: plain text mirrors the screen sections, including the absolute URLs of the linked toolkits. The fallback chain is Clipboard API → `execCommand` → selectable textarea.
- Safari: no regex lookbehind, `structuredClone`, top-level await or `dvh`. The base shell's `:has()` rules are cosmetic only; selected options use `.is-checked` and focus uses `input:focus-visible + label`. `localStorage` is wrapped in try/catch.
- Tap targets are ≥ 44px, inputs are 16px, and number fields use `inputmode="numeric"`. Sticky positioning is off under 880px, safe-area padding is applied, motion is reduced when requested, and the print view shows the deliverable only.
- Not tested: real Firefox, WebKit or Samsung Internet (no binaries here).
- Cross-links to tracking/seo/pr pages will 404 until those series land.
