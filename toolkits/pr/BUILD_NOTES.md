# Digital PR DIY Toolkits: build notes (Draft v1)

Owner: **Kristina Ainge** (CTA "Talk to Kristina about building it"). Built Oct 19, 2026 from the Agency Brands call. Two single-file HTML toolkits, same shell as the RevOps series. No external requests.

The line we held: Kristina said on the call that the proprietary systems (Muck Rack workflows, the internal HARO agent) can't be given away. These toolkits only cover **readiness**, meaning "a toolkit to be pitched": spokesperson, topics, bios, headshots, a press page, podcast readiness. Media lists, opportunity sourcing and pitching are only named under "Where it gets complex", and they hand off to Kristina.

## 01 · Are You Ready to Be Pitched? (`01_Are_You_Ready_to_Be_Pitched.html`)

**What it does:** a PR readiness gap audit. Nine answers produce a Pitch-Ready Checklist (gaps first, in fix order) and a 90-day prep plan.

**Questions → what each feeds**
| Question | Feeds checklist item | Counts as ready when |
|---|---|---|
| Company name (optional, prefilled from profile `name`) | Title of the copied plan | — |
| Who will talk to reporters? | Name a willing spokesperson | "One named person who has said yes" |
| Reply and interview speed | Commit to replying within 24–48 hours | "Within 24–48 hours" |
| Who approves a quote? | Set a same-day approvals path | "One person, same day" |
| 2–3 expertise topics written down? | Write down 2–3 expertise topics | "Yes" |
| News in the next 90 days (multi) | Find one newsworthy hook | Any box ticked |
| Where a reporter lands (profile `website:false` → "Neither") | Give reporters a page to land on | "About page and a press page" |
| Ready to send today (multi) | Short + long bio · Headshot · Past coverage | Both bios / headshot / coverage ticked |
| Expectations for the first 90 days | Agree on realistic expectations | "Groundwork, then a few early wins" |

**Results order:** headline (red count of month-one stall gaps, or "Ready") → Your Pitch-Ready Checklist (at-a-glance strip, then 10 items with "Do first" on the first three gaps, 3–5 how-to steps and a time range each) → Your 90-day prep plan (Phase 1 Prep, days 1–30 · Phase 2 Launch assets, days 31–60 · Phase 3 Sustain, days 61–90; gaps are bold inside their phase) → closing panel.

**Logic and assumptions**
- Headline = the number of open items flagged `stall: true`. 9 of the 10 items can stall month one; past coverage is polish only. It shows in the list but is not counted. Explained under "How we count gaps".
- In-between answers (someone in mind, within a week, a few people, ideas only, About page only, pages out of date, steady placements expected) count as gaps, each with a tailored "why".
- Profile `reach` local/regional adds a local and trade outlet tip to the news-hook item.
- Phase mapping mirrors the source PR plan: Phase 1 = spokesperson, speed, approvals, topics, bios, headshot, expectations · Phase 2 = news hook, press page, past coverage, press kit, byline · Phase 3 = announce, podcast applications, awards and speaking deadlines, monthly referral check, 90-day review.
- The "24–48 hours" and "groundwork in the first 30–60 days" figures are labeled rules of thumb. No statistics are cited.

**Where it gets complex** (sends to Kristina): media lists and relationships · reactive and expert-source pitching at scale · turning news into a story · crisis and reputation · measuring share of voice and sentiment (start with referral traffic, links to Tracking).

**Where it sends people next:** Next = Media Kit (02). Cross-links shown only when relevant: `mediaKit` (bios, topics or headshot missing) · `seoBasics` (no full press page) · `tracking` (always: measure coverage referrals) · `local` (profile has locations or is local) · `leadCapture` (profile goal is leads or calls) · `profile` (no profile loaded). The footer links `hub`.

## 02 · Build Your Media Kit (`02_Build_Your_Media_Kit.html`)

**What it does:** a spokesperson and media kit builder. It drafts seven pieces from short prompts using fixed templates. No AI, nothing sent anywhere. Each piece sits in an editable textarea with its own Copy button, an Edited tag and a Reset button. "Copy all", "Copy my plan" and "Download as .txt" are included. The download uses a Blob with `<a download>`, falls back to `msSaveOrOpenBlob`, then falls back to copying with a selectable box.

**Inputs:** name, job title, pronoun for third-person bios, company (from profile `name`), industry (from profile `industry`), what the company does, based in (optional), years of experience, 2–3 topics, one notable achievement, an origin or personal detail, audience, website, LinkedIn (optional), media contact email (optional).

**Outputs:** short bio (target about 50 words, live word count with a "trim" hint above 120% of target) · long bio (about 150) · one-line podcast intro · 5 host questions per topic (from a 9-question bank, no repeats within a topic) · "About <company>" boilerplate with media contact · headshot spec checklist (recency, 2000px or more, JPG plus web copy, under 5 MB, 4:5 / 16:9 or 3:2 / 1:1 crops, background and light, file naming, photo credit and permission) · press kit and newsroom page outline (9 sections).

**Logic:** blank fields render as `[bracketed placeholders]`. The headline counts missing details, or shows "7 of 7" when complete. Profile loaded → the kit starts blank with only company and industry filled (the solar example would not fit their business). No profile → the full example. Years are clamped from 0 to 80. All user text is escaped before it is inserted into HTML. Question prompts are generalized from Big Leap's thought-leadership bio questionnaire (shaping experience, three words, mission, misconceptions, industry change, origin story). No client content was reproduced.

**Where it gets complex:** finding your angle and voice · pitching the kit · paid podcast-guest and speaker placements · press releases · measuring what coverage does.

**Next:** PR 01. Cross-links: `prReady`, `seoBasics` (press page plus Organization and Person schema), `tracking`, `local` (profile has locations), `profile` (none loaded).

## Settings to edit before launch
- `CTA_URL` in both files (top of the script): swap `https://www.bigleap.com/contact-us/` for Kristina's scheduler link.
- `OWNER` if a co-owner is added.
- Remove the `draft-banner` div and the "Draft v1" footer note when approved.
- The Paid, SEO and Tracking files these pages link to are being built in parallel. Relative links will 404 until those land.

## Device and browser notes
- QA at 320, 390, 768, 1024, 1280 and 1920 (light and dark) in bundled Chromium: no overflow, no console errors. Firefox and WebKit binaries aren't available here, so the code was grepped for Safari-unsafe features (none: no lookbehind, `structuredClone`, `?.`, `??`, top-level await or `dvh`).
- The shell's `:has()` rules are kept for modern browsers, with class-based fallbacks (`.opt.is-checked`, `.seg input:focus-visible + label`) so older Safari still shows selected and focus states.
- Inputs use 16px text and tap targets are 44px or more. Sticky columns turn off under 880px. Print styles hide controls and open "Where it gets complex".

## Source material used
- Fathom: Agency Brands Bi-Weekly, Oct 19, 2026. Kristina 15:00–16:46 (readiness questionnaires, bios, spokesperson, topics, podcast readiness, headshots; proprietary-tools constraint) and Coby 32:42–37:26 (PR is qualitative, narrative and relationships; find the limits of a DIY tool).
- Drive: "Digital PR SWOT and Start/Keep/Stop" (Kristina). Used for the measurability emphasis (links, traffic, search visibility) and for setting clear expectations before onboarding.
- Drive: "Commercial Loan | Bio Questions". The question set was generalized into the bio prompts and the hi-res headshot ask.
- Drive: "PR Inbox Agent HARO requests". Read for context only. Its method is **not** exposed; it only informed the "reactive pitching at scale" complexity bullet.
- Source notes on a past PR plan (Phase 1/2/3 structure and metrics) and a PR post-mortem (willing spokesperson, fast replies, realistic expectations). Generalized, no client names.

## Open questions for Kristina
- Your "doc I started" for the PR toolkit wasn't found in Drive. Can you share it so v1 can be checked against it?
- Where exactly does the proprietary line sit? Is naming "reporter request services" (as a generic category) OK, or should even that stay out?
- Do paid podcast-guest lists or services belong in a v2 (for example a 90-day jumpstart option), or only as a "talk to Kristina" item?
- What is your meeting scheduler link for `CTA_URL`?
- Is "reply within 24–48 hours" the right bar for DIY clients, or do you prefer the "within ~5 business days for interviews" commitment used in past engagements?
- Should past coverage count toward the month-one stall headline, or stay polish only (current choice)?
- Are 50 / 150-word bios and the headshot spec (2000px or more, 4:5 / 16:9 / 1:1 crops) the formats your team actually asks clients for?
- Should 02 include more bio-questionnaire prompts (three words, mission, misconception, industry change) as optional fields, or keep it short?
- Do you want the copied plan to feed a follow-up from you (Dallas's "how'd it go?" idea), and if so, which address should it go to?
