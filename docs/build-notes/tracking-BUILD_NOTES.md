> **Update Oct 19, 2026:** there is no separate Tracking series any more. Toolkit 1 (tracking stack) is now **RevOps Toolkit 7** (`toolkits/revops/07_Can_You_See_What_Your_Marketing_Does.html`, owner Dallas Olsen) and Toolkit 2 (conversions) is now **Paid Media Toolkit 3** (`toolkits/paid/03_Which_Conversions_Should_You_Track.html`, owner Scott Smoot). The notes below are kept as written for the original build.

# Tracking & Measurement DIY Toolkits — Build Notes (Draft v1, Oct 19, 2026)

**Owner:** Scott Smoot (CTA: "Talk to Scott about building it")
**Co-owner:** TBD. Alex was suggested on the Oct 19 call ("maybe we can leverage like Alex or somebody else… maybe it's a collaborative thing").
**Status:** Draft v1 for internal review. Every page carries the draft banner.

Two single-file HTML toolkits, built on the same shell as the RevOps series (CSS tokens, light/dark, stepper, questions left / results right, live results, Copy my plan, closing panel). No external requests. Both read the shared Business Profile (`bl_diy_profile_v1` in localStorage, or a pasted `BL1.` code) built by Paid 01.

| # | File | Deliverable |
|---|---|---|
| 1 | `01_Can_You_See_What_Your_Marketing_Does.html` | Your Tracking Build List (install order + test checklist) |
| 2 | `02_Which_Conversions_Should_You_Track.html` | Your Conversion Event Plan (event table + build order + UTM starter) |

---

## Toolkit 1 — Can You See What Your Marketing Does?

**What it does:** a gap audit of the tracking stack (Coby's "what they have vs. what they need"). It never tells someone to set up something they already have. It gives an install-order build list with platform-specific steps, time ranges and a "test it" checklist.

### Questions → what each feeds
| Question | Feeds |
|---|---|
| Website platform (WordPress / Shopify / Squarespace / Wix / Webflow / HubSpot CMS / custom / not sure) | GTM install steps per platform; Shopify swaps GTM for the native Google & YouTube + Facebook & Instagram apps; consent tool suggestion; sitemap URL; Meta pixel install path |
| Google Tag Manager installed? | Item 1 (gap / check / ok) |
| GA4 installed? + how it was added (GTM / plugin-site / both-unsure) | Item 3. "Both" or "plugin + GTM present" raises the **double-tagging** check |
| Search Console verified? | Item 4 + cross-link to SEO 01 |
| EU/UK/EEA visitors? + consent banner (Consent Mode / basic / none) | Item 2 (core when EU = yes or unsure). If no EU but ads run, an optional US state privacy note |
| Ad platforms run or planned (Google Ads / Meta / LinkedIn) + tags present (all / some-unsure / none) | One item per platform: Google Ads tag + Conversion Linker + GA4 link + auto-tagging; Meta pixel **+ Conversions API** with event-ID dedupe; LinkedIn Insight Tag |
| How much phone calls matter | Call tracking item (core if "a lot", optional if "some") |
| Where leads end up (CRM with source / CRM without source / inbox) | CRM item → links to RevOps 01 (`leadCapture`) instead of repeating the HubSpot tracking code + UTM steps |

### Results order
1. Headline: **"N of M core pieces missing"** (red number), plus how many to check and a total time range.
2. Your Tracking Build List: at-a-glance strip, then items in install order: **Tag Manager → Consent → GA4 → Search Console → ad tags → call tracking → CRM source → test**. Each item has OK / Gap / Check / Optional, "Do first" on the first three open items, 3–6 how-to steps with menu paths, and a time range.
3. Test it checklist (Tag Assistant, GA4 DebugView + Realtime with a test UTM, Search Console, Google Ads status, Meta Test events, LinkedIn tag status, tap-to-call, CRM test lead), filtered to the answers.
4. Where it gets complex (6 bullets, "Applies to you" on the relevant ones).
5. Closing panel: Copy my plan, CTA, Next = Toolkit 2, cross-links.

### Logic and assumptions
- Core pieces = tag management (GTM; not core on Shopify), GA4, Search Console, CRM with source; plus Consent Mode when EU = yes/unsure; plus one per ad platform chosen; plus call tracking when calls matter "a lot". Range is 4–8.
- Missing = answered No. Check = Not sure or Some (it may already exist, so the step is to find it first).
- Time ranges are first-timer rules of thumb in `ASSUMPTIONS` (minutes, low/high), summed over open items only.
- Profile mapping: `ecommerce:'shopify'` → platform Shopify; `gtm`, `ga4` → those questions; `reach:'international'` → EU yes, any other reach → EU no; `adBudget > 0` → Google Ads ticked if none ticked; `goal:'calls'` → calls "a lot", locations → "some"; `crm` → lead destination. Tagged "From your profile" and still editable.

---

## Toolkit 2 — Which Conversions Should You Track?

**What it does:** turns how the business makes money into a named GA4 event plan, which events are key events, which go into Google Ads as Primary or Secondary, what value to pass, plus a UTM naming starter, the B2B offline-conversion path and the app SDK event chain.

### Questions → what each feeds
| Question | Feeds |
|---|---|
| Wins (form leads / calls / purchases / bookings / sign-ups / app installs) | Rows: `generate_lead`, `click_to_call` (+ Google Ads "Calls from ads"), `book_appointment`, `purchase` / `begin_checkout` / `add_to_cart`, `sign_up`, `first_open` → `subscribe` / in-app `purchase` |
| B2B / B2C / both | B2B or both + CRM + lead-type wins → offline path (`qualify_lead`, `close_convert_lead`) |
| CRM (HubSpot / other / none) | HubSpot ad conversion events vs. Google Ads CRM/file import |
| Ad platforms | Google Ads column, Primary/Secondary, Meta event mapping step, LinkedIn conversion step, UTM rows |
| After a form submit (thank-you page / inline message / embed or not sure) *(shown for leads/bookings)* | Trigger wording and GTM steps; "thank-you page reloads" and "button click vs. success" mistakes; embedded-form complexity flag |
| Store (Shopify / WooCommerce / other) *(shown for purchases)* | Where purchase events are set up; duplicate-purchase warning |
| App SDK (Firebase / AppsFlyer-Kochava-Adjust / none) + app money model *(shown for installs)* | App chain build step and table rows |
| Average first sale + leads out of 10 that buy *(optional)* | Lead value = sale × rate ÷ 10, passed as `value` on lead rows |
| Conversions tracked today (trust / some / none) | Adds the "check what you already count" audit step |

### Results order
1. Headline: **N conversions should steer your ad bids** (or N key events to mark in GA4 when no ads), plus total actions, lead value and time.
2. Your Conversion Event Plan: table (event, counts when, set up in, key event, Google Ads Primary/Secondary, value), then the build order (confirm stack → audit → GTM events → mark key events → Google Ads import + enhanced conversions → Meta mapping → LinkedIn → offline CRM path → app chain → test).
3. UTM naming starter (5 rules + example rows per channel used).
4. The classic mistakes (page views as conversions, duplicate purchases, thank-you reloads, everything primary, button click vs. success), "Applies to you" where relevant.
5. Where it gets complex, closing panel (Next = Paid 03 if ads, else RevOps 01 or SEO 01).

### Logic and assumptions
- Primary only for actions close to money: `generate_lead`, `book_appointment`, `purchase`, `sign_up` (secondary if purchases exist), "Calls from ads", `first_open` (at launch). `click_to_call` is always secondary (a tap is not a call). CRM imports start secondary and move to primary once volume is steady. The method note says Google's bidding learns best with "a few dozen conversions a month", and labels it a rule of thumb.
- `book_appointment` and `subscribe` are custom names in GA4 recommended-event style; the table note says so.
- Profile mapping: `goal` and `ecommerce` and `app` → wins; `model`, `crm` → those questions; `ecommerce` → store; `adBudget > 0` → Google Ads ticked.

---

## Where they send people next
- T1 → T2 always (Next). Cross-links: `leadCapture` (CRM without source or inbox), `seoBasics` (Search Console not yes), `adsReady` (Google Ads), `campaigns` (any ads), `local` (profile has locations), `pipelineDash` (CRM with source).
- T2 → `tracking` always; `leadCapture` (leads/bookings); `pipelineDash` (B2B + CRM); `campaigns` (any ads); `local` (calls + locations). In-step links to `adsReady` and `leadCapture`.
- Footer on both: `hub` (`../../index.html`). All toolkit links are relative and open in the same tab.

## Settings to edit before launch
- `CTA_URL` in both files: swap for Scott's meeting scheduler link.
- `OWNER`: add the co-owner if one is named and the CTA should change.
- `ASSUMPTIONS`: time ranges (minutes) if Scott or Alex want different estimates.
- `EXAMPLE`: the prefilled answers.
- Menu paths (GA4, GTM, Google Ads, Meta Events Manager, LinkedIn Campaign Manager, HubSpot, Shopify, Wix, Squarespace, Webflow) were written from current knowledge in Oct 2026. Have Scott or Alex click through them once before launch.

## Source material
- Fathom: "Agency Brands Bi-Weekly SEO/Content/PPC/RevOps Call - October 19" (3:30–14:00): Scott on GTM, conversion tracking, CRM → Google Ads (MQL/SQL/closed-won), Shopify integration, app SDKs (Kochava, AppsFlyer); Coby on GA4/GTM/pixels in the first two weeks "in order from beginning to finish" and the gap audit; Scott: tracking should be its own DIY section, linked from paid; Alex suggested as collaborator.
- `SOURCE_NOTES.md` tracking + paid sections (Sales AI: one trackable conversion per landing page, launch blocked on GTM conversion + HubSpot ↔ Google Ads re-auth; NCHRG app event chain install / first open / subscribe; Tax Lien Code: Search Console AI Overview reporting).
- RevOps Toolkit 01 (`Is Every Lead Reaching Your CRM?`). It owns the HubSpot tracking code + UTM capture, so these toolkits link to it instead of repeating it.

## Open questions for Scott/Alex
1. Who is the co-owner of this series: Alex, or someone else? Should the CTA name both?
2. Scott's meeting scheduler URL for `CTA_URL`.
3. On Shopify, do we recommend the native Google & YouTube app only, or GTM via Customer Events for clients who'll run paid?
4. Should a client import GA4 key events into Google Ads, or use Google Ads tags via GTM? (T2 currently says either, but not both.)
5. Is "click_to_call = secondary, Calls from ads ≥ 60s = primary" the default you want?
6. What conversion volume should a client wait for before making qualify_lead primary? (The draft says "steady weekly volume".)
7. Which call tracking vendor do we prefer to name first (CallRail, CTM, WhatConverts)?
8. Which consent platforms do we recommend (Cookiebot, CookieYes, Usercentrics, OneTrust, Complianz), and should we name any?
9. Should T1 cover Microsoft Ads UET and TikTok pixels, or leave them for v2?
10. For apps, should we recommend Firebase only to start, or an attribution partner (AppsFlyer, Kochava) when Meta/Apple Ads run too?
11. Should the "free GA4 dashboard for AI/LLM referral traffic" (Tax Lien Code) be a step in T1 or its own toolkit?
12. Should server-side tagging stay only in "Where it gets complex", or count as a core piece for e-commerce?
13. Should a filled-in plan trigger the automated "how'd it go?" follow-up Dallas proposed (needs form capture, which these pages don't have)?
14. Who verifies the menu paths before launch, and how often should they be rechecked?

## QA run (Oct 19, 2026)
- Bundled Chromium at 320 light, 390 dark, 768 light, 1280 light, 1920 dark: no horizontal overflow, no console errors (screenshots in `scratchpad/qa/tracking-{1,2}-*.png`).
- Blank inputs (all unchecked, numbers cleared) and extreme inputs (all checked, 999,999,999,999): no NaN, undefined or null on screen. Profile paste, prefill tags and Clear all work. The copy text holds the headline and every build step.
- Grep: no `:has()`, regex lookbehind, `structuredClone` or top-level await. `100dvh` has a `100vh` fallback. Clipboard falls back to textarea + `execCommand`. localStorage is wrapped in try/catch.
- Not testable here: real Safari/Firefox/Samsung Internet (no binaries), and a physical print preview (`@media print` rules are in place).
