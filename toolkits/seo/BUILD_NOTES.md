# SEO DIY Toolkits: build notes (Draft v1)

Owner: **Shemmah Al-Darweesh** (CTA: "Talk to Shemmah about building it"). Toolkits 1-2 built Oct 19, 2026 from the Agency Brands call. Toolkits 3-5 added Oct 22, 2026.
Files: `01_Can_Google_Find_and_Trust_Your_Site.html`, `02_Is_Your_Business_Ready_for_Local_Search.html`, `03_Does_Google_and_AI_Know_Who_You_Are.html`, `04_How_Exposed_Are_You_to_AI_Overviews.html`, `05_Can_AI_Bots_Actually_Read_Your_Site.html`. Each is a single self-contained file with no external requests. It uses the RevOps v2 shell, the shared Business Profile, and the cross-link map from the build spec.

**Toolkits 3-5 origin.** Shemmah flagged in Slack that the SEO lineup should reflect AI search (entity recognition, AI Overviews, AI crawler access), and suggested swapping the existing two toolkits out for three new ones. The account owner's call was to keep toolkits 1-2 exactly as they are and add the three AI-search toolkits alongside them, so the SEO stepper now runs five steps instead of two. Nothing in toolkits 1-2 was removed or renamed; only the series-wide `SERIES`/`LINKS` metadata, the stepper's "N of 5" CSS, and the "SEO DIY Toolkit X of 5" eyebrow/footer text were updated on those two files.

---

## Toolkit 1: Can Google Find and Trust Your Site?

**What it does.** A foundations gap audit: what a business can set up itself before a first SEO conversation. It checks only what the visitor doesn't already have and hands back **"Your SEO Foundation Fix List"** in build order.

**Questions → what each one feeds**

| # | Question | Feeds |
|---|---|---|
| 1 | Website platform (WordPress / Shopify / Squarespace / Wix / Webflow / HubSpot / Other) + optional domain | The platform note on each fix (menu paths), the sitemap URL, and the domain filled into checks, robots.txt and schema code |
| 2 | Google Search Console: verified + sitemap / verified, no sitemap / none / not sure | "Set up GSC and submit sitemap" fix (or sitemap-only, or access check) |
| 3 | Bing Webmaster Tools yes / no / not sure | Bing fix (import from GSC; note on Copilot / ChatGPT search) |
| 4 | robots.txt: open / blocks some bots / blocks all / haven't looked | **Blocker** (all or some) or a check. Includes a search-bot vs training-bot table and an example robots.txt |
| 5 | `site:` search: main pages there / some missing / few or none / haven't checked | **Blocker** (some or few) or a check. Covers the GSC Pages report, URL Inspection and noindex settings per platform |
| 6 | Already true: HTTPS, Core Web Vitals on mobile, unique titles and descriptions, Organization/LocalBusiness schema, About and contact | One fix per unticked box. The schema fix includes copyable JSON-LD |
| 7 | GA4 yes / no / not sure | GA4 fix + cross-link to Tracking |
| 8 | Page count (<50 / 50–500 / 500+); redesign planned; multi-country; local customers | Number of key pages to title; flags "Where it gets complex"; Organization vs LocalBusiness schema; next toolkit |

**Results order.** Headline (red count of blockers) → Fix List (blockers, then "check this" items, then fixes in build order; the first three are "Do these first"; each has 3–6 how-to steps, a platform note, and a time range) → Already in place → Where it gets complex (flagged "Applies to you") → closing panel.

**Logic and assumptions**
- A **blocker** stops Google or AI search from seeing the site: robots.txt blocks everything, robots.txt blocks named search bots, or important pages are missing from Google. "Haven't looked" answers become checks, not blockers.
- Build order: robots.txt → Search Console + sitemap → indexing → Bing → HTTPS → mobile/CWV → titles → schema → About/contact → GA4.
- Bot guidance: keep **search** bots allowed (Googlebot, Bingbot, OAI-SearchBot, PerplexityBot). Blocking **training** bots (GPTBot, Google-Extended, CCBot) is a business choice and doesn't remove a site from search. This follows the AI-crawler item in the Drive GEO checklist, with OAI-SearchBot and PerplexityBot added.
- Times are first-time rules of thumb in `ASSUMPTIONS` (minutes, low/high). Title time = minutes per page × key pages (6 / 12 / 20 by size). These are shown under "How we calculate this".
- Title (~50–60 characters), description (~140–160) and image size (~200 KB) limits are labelled as rules of thumb.

**Profile mapping.** `ecommerce: shopify` → platform = Shopify. `ga4` → GA4 question. `locations` one/multi or `reach: local` → "local customers" box (LocalBusiness schema). `reach: international` → multi-country box. `website: false` → a note that says to use the list as a launch checklist. `goal`, `crm` and `adBudget` only affect cross-links.

**Where it sends people next.** Next: Local (if there are locations or a local area), otherwise Tracking (no GA4), otherwise Conversions. Cross-links shown only when relevant: tracking (RevOps 7) or conversions (Paid 3), local, leadCapture (leads/calls goal or CRM), prReady (no About/trust basics), adsReady (ad budget > 0). The next toolkit is never listed again under cross-links.

---

## Toolkit 2: Is Your Business Ready for Local Search?

**What it does.** A readiness check for businesses with a location or service area. It produces **"Your Local Search Checklist"**, scaled to the number of locations, plus copyable review request (text and email) and review reply templates (good and bad).

**Skip state.** If the visitor picks "online only", or the profile says `locations: none` without a local reach (or `gbp: na`), the questions and checklist are hidden. The page shows "You can skip this one" with a link to seoBasics and an "I do have a location or service area" undo button.

**Questions → what each one feeds**

| # | Question | Feeds |
|---|---|---|
| 1 | How customers reach you: storefront / service area / both / online only | Skip state; service-area vs storefront setup steps; wording of other items |
| 2 | Number of locations (+ optional business name) | Per-location time multipliers; business-group item (2+); bulk verification (10+); name in templates |
| 3 | GBP: verified / exists but not ours / none / not sure | **Blocker** (claim, create or verify) or an access check |
| 4 | Profile filled in: categories, hours, photos, services/description, address/service area | Setup, categories and "fill in" items |
| 5 | NAP consistent: yes / some differ / haven't checked + directories claimed (Apple Business Connect, Bing Places, Yelp, Facebook, industry directory) | NAP item; directory item lists only the missing ones |
| 6 | Reviews: ask every / sometimes / never; reply every / only bad / rarely | Review request and review reply items (rules on incentives and filtering who you ask) |
| 7 | Location pages: one per location / one contact page / not really | Location page item (unique content, embedded map, LocalBusiness schema, GBP website link) + link to seoBasics |
| 8 | Duplicates; similar names; running Google Ads | Duplicates / similar names **blocker**; Google Ads location asset item + link to adsReady |

**Results order.** Headline ("N of 8 local basics are missing", red) → Checklist (blockers first, then build order; time ranges already multiplied per location) → Already in place → Review request and reply templates (an optional review-link field fills them in) → Where it gets complex → closing panel.

**Logic and assumptions**
- The eight basics: verified profile; no competing profiles; complete profile; matching NAP; Apple and Bing claimed plus most directories; asking every customer; replying to every review; location pages.
- Time totals leave out the ongoing weekly review replies, which are called out separately.
- Location count is clamped to 1–999. Blank or invalid input counts as 1.

**Profile mapping.** `locations` none/one/multi → mode and count (multi defaults to 3, which the visitor can edit). `gbp` yes/no → GBP question. `name` → business name. `adBudget > 0` → ticks "We run Google Ads".

**Where it sends people next.** Next: adsReady if they run Google Ads, otherwise seoBasics. Cross-links: seoBasics, adsReady or campaigns, tracking or conversions, speedToLead (calls/leads goal or CRM).

---

## Toolkit 3: Does Google and AI Know Who You Are?

**What it does.** A brand entity health check: whether Google and AI tools can resolve the business to one clear, consistent subject. Produces **"N of 6 entity signals"** plus a ranked fix list, foundational/DIY-able signals (schema, consistency) ranked ahead of signals that can't be built on demand (Knowledge Panel, press mentions).

**Questions → what each one feeds**

| # | Question | Feeds |
|---|---|---|
| 1 | Website platform + optional business name/domain | Platform note on the schema fix; prefills the copyable Organization JSON-LD |
| 2 | Knowledge Panel shows for the business name: yes/no/unsure | Panel item (flagged as "takes time," not a one-time fix) |
| 3 | NAP (name, address, phone) consistent across profiles: yes/some differ/unsure | NAP consistency item |
| 4 | Organization schema on homepage: yes/no/unsure | Schema item with the copyable JSON-LD snippet |
| 5 | Press/partner/directory mentions: yes/no/unsure | Mentions item (flagged "takes time") |
| 6 | One clear About page: yes/no/unsure | About page item |
| 7 | Social profiles cross-linked to the site: yes/no/unsure | Cross-link item |

**Results order.** Headline ("N of 6 entity signals") → Fix list, schema and consistency ranked ahead of "takes time" items (new `earn` severity chip, styled like the existing `.chip.manual` pattern) → Already in place → Where it gets complex → closing panel.

**Logic and assumptions.** The Organization JSON-LD snippet prefills from `loadProfile()` (business name, domain) with bracketed placeholders (`[Your Business Name]`) when profile data is missing — a deliberate departure from Toolkit 1's ALL-CAPS placeholder convention, per the build spec. The profile is never written, only read.

**Where it sends people next.** Next: Local (`seo2`) if NAP/locations are unresolved, otherwise AI Overviews (`seo4`). Cross-links: `seoBasics`, `local`, `seoExposure`, `prReady` (press mentions missing).

---

## Toolkit 4: How Exposed Are You to AI Overviews?

**What it does.** Checks whether content is shaped the way AI Overviews and answer engines tend to lift an answer: answer-first structure, FAQ-style headers, FAQPage/HowTo schema, page-1 ranking (an authority proxy) and refresh cadence. Produces an exposure level (Low / Building / Ready for AI Overviews) and a ranked fix list with a before/after plain-text example of rewriting a paragraph answer-first. No invented statistics about AI Overview click-through or traffic impact anywhere on the page — mechanism and plausible reasoning only.

**Questions → what each one feeds**

| # | Question | Feeds |
|---|---|---|
| 1 | Website platform | Platform note on the FAQPage/HowTo schema fix |
| 2 | Key pages answer the question in the first sentence or two: yes/no/unsure | Answer-first item, with the before/after example attached |
| 3 | FAQ-style, question-phrased headers: yes/no/unsure | FAQ headers item |
| 4 | FAQPage or HowTo schema present: yes/no/unsure | Schema item |
| 5 | Page-1 ranking for a core keyword: yes/no/unsure | Authority item (flagged "takes time," links to `seoBasics`) |
| 6 | Content refresh cadence (within 3mo / 3-12mo / over 1yr / never) | Refresh-calendar item |

**Results order.** Headline ("N of 5 exposure signals") → Fix list (formatting fixes first, then checks, then the authority item) → Already in place → Where it gets complex → closing panel.

**Logic and assumptions.** Formatting (answer-first, FAQ headers, schema) is treated as DIY-able with time ranges; ranking/authority is treated as earned over time, not scheduled, and carries no time estimate.

**Where it sends people next.** Next: `seoBasics` if not yet ranking page 1 for any core keyword (AI Overviews mostly pull from pages that already rank), otherwise `seoCrawler`. Cross-links: `seoCrawler`, `seoEntity`, `seoBasics`.

---

## Toolkit 5: Can AI Bots Actually Read Your Site?

**What it does.** A technical readiness grader for the named AI crawlers (GPTBot, Google-Extended, PerplexityBot, ClaudeBot, CCBot, OAI-SearchBot): robots.txt blocking, llms.txt presence, JS-rendering vs. static HTML, XML sitemap submission, homepage load speed, login/paywall gating. Produces a grade (Blocked / Partially ready / Ready) and a ranked technical fix list, with a copyable robots.txt allow-list snippet for the six named bots.

**Questions → what each one feeds**

| # | Question | Feeds |
|---|---|---|
| 1 | Website platform | Platform note on the llms.txt fix |
| 2 | robots.txt blocks any named AI crawler: no/yes/haven't checked | **Blocker** (yes) or a check; carries the bot table and the copyable allow-list snippet |
| 3 | llms.txt present at site root: yes/no/unsure | llms.txt item |
| 4 | Key content visible without JavaScript: yes/no/unsure | **Blocker** (needs JS) or a check; flagged as usually needing a developer, no DIY time estimate |
| 5 | XML sitemap submitted to Search Console: yes/no/unsure | Sitemap item |
| 6 | Homepage load speed (fast / moderate / slow / untested) | Speed item, scaled to severity |
| 7 | Core content gated behind login/paywall: no/yes/unsure | **Blocker** (yes); framed as a business decision, not a one-time fix |

**Results order.** Headline (grade + "N of 6 technical signals clear") → Fix list, hard blockers ranked first (new `block` severity chip), then fixes, then checks → Already in place → Where it gets complex (server-side rendering, real speed fixes, gating as a business call, confirming crawler visits needs server logs) → closing panel.

**Logic and assumptions.** Any one of: robots.txt blocking a named bot, content gated, or content requiring JavaScript, sets the grade to "Blocked" regardless of the other five signals, because none of them matter until that one is cleared.

**Where it sends people next.** Next: always `seoExposure` — formatting for AI Overviews only pays off once AI crawlers can reach the content, so the "why" text changes depending on whether a blocker is present. Cross-links: `seoBasics`, `seoEntity`, `seoExposure`.

---

## Settings to edit before launch (top of each file's script)
- `CTA_URL`: currently `https://www.bigleap.com/contact-us/`. Swap for Shemmah's meeting scheduler link.
- `OWNER`: name and first name used on the CTA and in "Where it gets complex".
- `EXAMPLE`, `ASSUMPTIONS`: example answers and time ranges.
- `LINKS`: the shared cross-link map. Paid, Tracking and PR targets must exist at the same relative paths. Neither page was checked against those series' final files.
- Toolkits 3-5 add `seoEntity`, `seoExposure` and `seoCrawler` to the `LINKS` map in all five SEO files plus the 15 other toolkit/roadmap files that carry their own copy of this map (Paid, Plan, PR, Email, RevOps 07, `roadmap.html`), so any toolkit can cross-link to them. The three keys were not added to `data/widgets.json`'s wording or any file outside this `LINKS` map search.

## Source material used
- Fathom: "Agency Brands Bi-Weekly SEO/Content/PPC/RevOps Call - October 19" (Scott Smoot ~9:10 on locations, GBP and Google Ads, and "for SEO, GA4 plus a couple of conversion events is enough"; Coby Bush ~9:15–12:40 on "hold a brush vs. Starry Night" and doing setup in order from beginning to end; Coby ~38:00–41:00 on "what has to be done before we can have a conversation" and "you wouldn't set up GA4 again if it already exists").
- Google Drive: "Site Migration/Redesign - SEO Checklist - Template" (HTTPS, robots.txt, XML sitemap, GSC + Bing submission, canonicals, schema carry-over, mobile/PageSpeed, custom 404, redirects → "Where it gets complex").
- Google Drive: the client-specific "Website SEO / GEO Checklist" (AI crawler access review, Organization/FAQ schema for AI understanding, entity clarity, LLM-friendly content → content strategy and AI visibility in "Where it gets complex"). Generalized; no client named.
- Source notes: AI search tracking needs prompts, URLs, competitors and personas, and has no history before setup; location pages + GBP; competing GBP profiles with similar names; simple local landing pages (hero, H1, details, map).

## Open questions for Shemmah
1. Confirm you are the owner and CTA name for both SEO toolkits, or name a co-owner (Alex and Mark also run SEO/GEO).
2. Provide your meeting scheduler link to replace `CTA_URL`.
3. Which AI-search checks should stay in the foundations kit (OAI-SearchBot, PerplexityBot, Bing for Copilot/ChatGPT)? Add llms.txt, or leave it out?
4. Is the "search bots vs training bots" advice (allow search bots; blocking training bots is the client's choice) Big Leap's official position?
5. Do you want a third "Content and keyword starter" toolkit (topics, question-based pages, one primary intent per page), or should that stay expert-only?
6. Should AI visibility tracking setup (prompts, competitors, personas) become a DIY step, or stay in "Where it gets complex"?
7. Should the blocker definition include "no Search Console", or only things that actually hide the site (robots.txt, indexing)?
8. Are the time ranges in `ASSUMPTIONS` realistic for a first-time SMB owner? Adjust any that feel off.
9. Is a "check your redirects" mini-step wanted for visitors planning a redesign, or should migrations stay fully expert-led (currently expert-only)?
10. Local: should we name a listing-sync tool for multi-location (for example BrightLocal), or stay vendor-neutral (currently neutral)?
11. Local: which industry directories should we name per vertical? (Current examples: Healthgrades, Avvo, Houzz, Angi, TripAdvisor.)
12. Local: is "about two hours' drive" the service-area guidance you want to cite, or should that line go?
13. Should LeadGenix (local SMB clients) get a variant of Toolkit 2 with LeadGenix branding or a different CTA?

## QA (run Oct 19, 2026)
- Headless Chromium at 320 light, 390 dark, 768 light, 1280 light, 1920 dark for both files: no horizontal overflow, no console errors. Screenshots in `scratchpad/qa/seo-<n>-*.png` (plus `seo-2-390-dark-skip.png` and `seo-1-print.png`).
- Behaviour tests: blank or extreme location counts (blank, -5, 0, 99999, 2.7, "e") show no NaN, undefined or null. A junk domain is escaped. Profile paste, prefill, "From your profile" tags and Clear all work. Toolkit 2 shows the skip state from a `locations: none` profile. "Copy my plan" text includes every item title on screen and the templates. Clipboard fallback chain: `navigator.clipboard` → hidden-textarea `execCommand` → visible selected textarea.
- Keyboard: every control is reachable in order. Segmented buttons get a visible focus ring through a class (no `:has()`). Arrow keys move within radio groups.
- Safari safety: no `:has()`, regex lookbehind, `structuredClone`, optional chaining or top-level await. `localStorage` is wrapped in try/catch. `100dvh` has a `100vh` fallback. Reduced motion is respected. Print stylesheet hides the controls.
- Not testable here: real Firefox, WebKit/Safari and Samsung Internet (binaries unavailable). Paid, Tracking and PR cross-link targets did not exist yet at build time.
