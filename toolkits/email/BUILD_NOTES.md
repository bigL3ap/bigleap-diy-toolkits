# Email Marketing DIY Toolkits: build notes (Draft 1)

Owner: **Erica Pounder** (CTA: "Talk to Erica about building it"). Built Oct 19, 2026 from the Agency Brands call.
Files: `01_Will_Your_Emails_Reach_the_Inbox.html`, `02_Which_Emails_Should_Send_Themselves.html`, `03_Is_Your_Email_Program_Working.html`. Each is one self-contained file with no external requests. They use the RevOps v2 shell as carried into the SEO series (draft banner, Business Profile strip, stepper, live results, "Copy my plan", closing panel), the shared Business Profile helper, and the shared cross-link map. The site header and pager are injected afterwards by `tools/site_header.py`; none of it is in these files.

Series stepper: 1 Inbox → 2 Automate → 3 Measure, with "Start here: Build your Business Profile" (Paid 01).
Brand line: "Ready for the big leap? Talk to Erica about building it." appears once per page, in "Where it gets complex".

---

## Toolkit 1: Will Your Emails Reach the Inbox?

**What it does.** A deliverability and compliance gap audit. It hands back **"Your Inbox Readiness List"** in fix order, with platform-specific menu paths, a copyable DMARC record, and a plain table of the email laws for the visitor's regions.

**Questions → what each one feeds**

| # | Question | Feeds |
|---|---|---|
| 1 | Platform: Mailchimp / Klaviyo / HubSpot / Constant Contact / Other | Menu paths on authentication, unsubscribe, address, double opt-in and report items |
| 2 | From address: own domain / free mailbox / not sure (+ optional domain) | "Send from your own domain" **risk** or check; domain merged into steps and the DMARC record |
| 3 | SPF, DKIM, DMARC: yes / no / not sure each | SPF+DKIM item (**risk** if either is no, check if unsure); DMARC item (**risk** or check) with record snippet |
| 4 | Every email has: unsubscribe link, postal address | One **risk** per missing box (CAN-SPAM, CASL, Gmail/Yahoo one-click rule) |
| 5 | List sources: signed up / bought from us / imported / bought-rented-scraped; double opt-in yes/no | Bought list **risk**; imported-contacts item (**risk** if UK/EU); double opt-in fix |
| 6 | List size; last send: 30 days / 1–6 months / 6–12 months / over a year | Stale list **risk** (6+ months), "ease back in" fix (1–6 months); bulk-sender note at 5,000+ |
| 7 | Bounce and complaint rates: fine / high or warned / don't know | **Risk** (high) or check, with Google Postmaster Tools and a link to Toolkit 3 |
| 8 | Subscribers in US / Canada / UK or EU | Consent-records fix (CA or UK/EU) and the rules table |
| 9 | Coming up: platform move, new domain, several brands | "Where it gets complex" flags |

**Results order.** Headline (red count of issues that could send mail to spam or break the rules) → Inbox Readiness List (risks first, then checks, then fixes; SPF/DKIM is always kept just before DMARC; first three "Do these first"; each with steps, platform note, time) → Already in place → Rules table for their regions → Where it gets complex → closing panel.

**Logic and assumptions**
- Inbox risk = free-mailbox sender, SPF or DKIM missing, DMARC missing, bought list, list not mailed 6+ months, no unsubscribe, no address, rates known to be high, imported UK/EU contacts. "Not sure" answers become checks, never risks.
- Gmail/Yahoo bulk-sender rules (Feb 2024; Microsoft Outlook.com similar in 2025) are flagged from 5,000 contacts (`ASSUMPTIONS.bulkList`) as a proxy for 5,000 emails a day.
- DMARC starts at `p=none` with a report address; the steps say to wait 2–4 weeks before `p=quarantine` and to get help before `p=reject`.
- Times are first-time rules of thumb in `ASSUMPTIONS` (minutes), shown under "How we calculate this". DNS waits are extra.
- The laws table is general information, labelled "not legal advice".

**Profile mapping.** `crm: hubspot` → platform HubSpot. `reach: international` → ticks UK/EU. `ecommerce` shopify/other → ticks "they bought from us". `name` → plan text. `goal` and `locations` only affect cross-links.

**Where it sends people next.** Next: Toolkit 2 (flows). Cross-links when relevant: leadCapture (no CRM or imported contacts), tracking (UTMs on email links, always), speedToLead (leads/calls goal), local (has locations), emailHealth.

---

## Toolkit 2: Which Emails Should Send Themselves?

**What it does.** An automated flow planner. It produces **"Your Automated Email Plan"**: the recommended flows for the visitor's kind of business, ranked, each with trigger, timing, number of emails, goal, three or four subject lines merged with their business name, and build steps for their platform. Below it, **"Your first email, ready to edit"** for the top missing flow, with a copy button.

**Questions → what each one feeds**

| # | Question | Feeds |
|---|---|---|
| 1 | Business type: online store / B2B / local services / bookings / software | Which flows are recommended and their rank, per-type names, triggers and goals |
| 2 | Business name | Merged into subject lines and the first email (special characters are safe) |
| 3 | Platform | Build steps per flow and the "connect your tool" step |
| 4 | Store, booking tool or CRM connected? | "Connect first" step and "Needs a connection" chips on cart, browse, after-purchase, reminder, win-back, onboarding |
| 5 | Flows already running (8 boxes) | Running flows ticked off; missing count |
| 6 | List size and average order/customer value (optional) | Rule-of-thumb estimate in the headline and per flow |
| 7 | Who follows up with a new lead | "Marketing email, not sales follow-up" note + link to speedToLead |

**Ranking by type**
- Online store: welcome → abandoned cart → after-purchase/review → browse abandonment → win-back → sunset
- B2B: welcome → lead nurture → re-engage cold leads → sunset
- Local services: welcome → thank-you/review request → appointment reminders → service-due win-back → sunset
- Bookings: appointment reminders → welcome → after-visit/rebook → win-back → sunset
- Software: trial/onboarding → welcome → re-engagement → sunset

**Headline.** Red count of missing recommended flows, then "Start with your [top missing flow]", then an estimate labelled as a rule of thumb: for each missing flow, list size × % entering a month × % taking the goal action (× average value if given). The shares per flow are editable on the page under "How we calculate this" (with reset). Sunset is never counted; it protects inbox placement.

**Guardrails in the copy.** Review requests: no incentives and no filtering who is asked (Google policy and US rules). Reminders: use the booking tool's own reminders if it has them. Sunset: suppress, don't delete. HubSpot: multi-step email workflows may need a higher Marketing Hub plan.

**Profile mapping.** `ecommerce` shopify/other → online store; else `app` or `goal: installs` → software; else `model: b2b` → B2B; else `locations` one/multi or `reach: local` → local services. `name` → business name. `crm: hubspot` → platform HubSpot. `crm` also sets who follows up.

**Where it sends people next.** Next: Toolkit 3. Cross-links: speedToLead (a person follows up, or B2B), leadCapture (no CRM), local (local or bookings: review flow pairs with Google reviews), tracking (UTMs on flow links), conversions (online store), inbox.

---

## Toolkit 3: Is Your Email Program Working?

**What it does.** A health scorecard. **"Your Email Health Scorecard"** grades nine measures good / watch / fix, then **"The 3 fixes to do first"**, each with steps and where to find the number in their platform.

**Questions → what each one feeds**

| # | Question | Feeds |
|---|---|---|
| 1 | Mostly email consumers / businesses | Which range set (B2C or B2B) is used |
| 2 | Platform | "Where to look" note and UTM setting in the tracking fix |
| 3 | Contacts today and 3 months ago | List growth (%) |
| 4 | Campaigns a month | Sending rhythm (fix under 1, watch over 12) |
| 5 | Click, unsubscribe, spam complaint, bounce rates (90 days) | One scored row each. Open rate is deliberately not asked; the helper explains Apple Mail Privacy Protection |
| 6 | Revenue / leads / not tracked + amount per send | "Results per send" row; not tracked = fix |
| 7 | Segmentation: none / one or two / several | Segmentation row |
| 8 | Sunset policy: yes / no / not sure | Sunset row |

**Ranges (editable on the page, with reset)**

| Measure | B2C good / fix | B2B good / fix |
|---|---|---|
| Click rate | 2%+ / under 1% | 2.5%+ / under 1% |
| Unsubscribe rate | under 0.5% / 1%+ | under 0.3% / 0.8%+ |
| Spam complaint rate | under 0.1% / 0.3%+ | under 0.1% / 0.3%+ |
| Bounce rate | under 1% / 2%+ | under 2% / 3%+ |
| List growth (3 months) | 3%+ / shrinking | 3%+ / shrinking |
| Campaigns a month | 2+ / under 1 (watch over 12) | same |

Click, unsubscribe, spam and bounce ranges follow the benchmark table in Big Leap's Klaviyo audit standard (which cites the Email Marketing Training Manual §8–9 and Gmail/Yahoo sender rules). The B2B bounce "fix at 3%" and the unsubscribe "fix" lines are my additions to create a watch band; Erica should confirm.

**Fix order.** Spam → bounce → sunset → click → unsubscribe → tracking → segmentation → growth → rhythm; fix before watch; top three shown. Blank answers show "Not entered" and never count as a problem.

**Profile mapping.** `model` b2b/b2c → audience. `crm: hubspot` → platform. `goal: sales` → revenue; `leads`/`calls` → leads.

**Where it sends people next.** Next: inbox (spam or bounce at fix), else tracking (not tracked), else flows. Cross-links: inbox, tracking, conversions (revenue not tracked), leadCapture + pipelineDash (leads), flows (no sunset or no segments).

---

## Settings to edit before launch (top of each file's script)
- `CTA_URL`: currently `https://www.bigleap.com/contact-us/?utm_source=diy-toolkits&utm_medium=talk-to-owner&utm_campaign=email-0N`. Swap for Erica's scheduler link, keeping the UTMs.
- `OWNER`, `SERIES`, `LINKS`: identical in all three files.
- `EXAMPLE`: first-visit answers. `ASSUMPTIONS`: times (01), flow shares (02), ranges (03).
- The pages are generated from `scratchpad/email-src/build.py` (+ `p1.py`, `p2.py`, `p3.py`, the shared `base.css` and `common.js` taken from SEO 01). Editing the HTML directly is fine too; just don't mix the two.

## Source material used
- **Fathom: "Agency Brands Bi-Weekly SEO/Content/PPC/RevOps Call - October 19"**: Coby Bush ~9:00–12:40 and ~38:00–41:00 (get clients set up so Big Leap time goes to strategy; "what has to be done before we can have a conversation"; don't redo what already exists → the gap-audit shape and the "Already in place" lists); Dallas Olsen ~7:00 (cross-link the toolkits); Dallas ~0:24 (Big Leap moved its own email marketing from HubSpot to Mailchimp → open question below); Dallas ~13:52 / Scott ~14:23 ("how'd it go?" check-in after someone gets a deliverable → open question below).
- **Big Leap Klaviyo audit standard** (`revops-klaviyo-audit` skill: format spec, intake checklist, analyzer): the benchmark table used for Toolkit 3; the core flow list (welcome, abandoned checkout/cart, browse, post-purchase, win-back, sunset) used for Toolkit 2; "lead with clicks, not opens (Apple MPP)"; branded sending domain + DMARC and single vs. double opt-in as intake items used in Toolkit 1.
- **Google Drive** (generalized; no client names or content reproduced):
  - Client email workflow build specs (Welcome / First order / Reactivation at 60–75–90 days, each with an exit goal) → the trigger + timing + exit structure in Toolkit 2.
  - A Klaviyo + Shopify requirements doc (cart, browse and replenishment emails showing generic blocks until store data flows) → "Product feeds and dynamic content" in Where it gets complex, and the "Needs a connection" logic.
  - A brand's contact accounting for a Mailchimp import (purchased and out-of-policy contacts held out per Mailchimp's acceptable use policy; unsubscribes loaded first as suppressions) → the bought-list risk and "suppress, don't delete" guidance.
  - A HubSpot workflow export including an "inactive subscriber sunset and win-back" workflow (90+ days without engagement, 3 steps) → sunset flow timing.
  - Drip email stats sheets and a Q4 email marketing planner → click-rate framing and the sending-rhythm measure.
  - I did not find an email document authored by Erica, nor the "Email Marketing Training Manual" the audit standard cites. Searches run: Klaviyo, Mailchimp, deliverability, welcome series, email flow, "Erica Pounder", owner = erica@bigleap.com, Training Manual titles.

## Open questions for Erica
1. Which platforms should we support first? Pages cover Mailchimp, Klaviyo, HubSpot and Constant Contact; should any be dropped, or Brevo/ActiveCampaign added?
2. Should Mailchimp steps lead (default example on Toolkit 1), given Big Leap's own move from HubSpot email to Mailchimp?
3. Are the Toolkit 3 ranges the ones you use? Especially the B2B bounce fix line (3%) and the unsubscribe fix lines (1% B2C, 0.8% B2B).
4. Is the Email Marketing Training Manual (cited by the audit standard) the source of truth for benchmarks, and where does it live?
5. Are the Toolkit 2 rule-of-thumb shares (e.g. 4% of list entering cart flow, 5% recovering) acceptable to show, or should the dollar estimate be removed?
6. Please check the menu paths per platform (Mailchimp Domains, Klaviyo branded sending domain, HubSpot email sending domain, Constant Contact self-authentication).
7. Is 5,000 contacts the right threshold to flag Gmail/Yahoo bulk-sender rules, given the rule is 5,000 emails a day?
8. Do you want the consent/laws table in Toolkit 1 reviewed by legal before launch?
9. Your meeting scheduler link for `CTA_URL`?
10. Add a 4th toolkit for sign-up forms and lead magnets (list growth), or fold it into Toolkit 2?
11. Should SMS appear anywhere, or stay in "Where it gets complex" only?
12. Dallas's "how'd it go?" idea: should a completed plan trigger a check-in email from you 2–4 weeks later (needs a form or capture step these pages don't have yet)?

## Known limits (Draft 1)
- Nothing is sent or stored except the shared Business Profile in `localStorage`. The domain and business name fields stay on the page.
- QA: 320 light, 390 dark, 768 light, 1280 light, 1920 dark: no horizontal overflow, no console errors, no NaN/undefined on default, blank, extreme (999,999,999,999), negative and zeroed-assumption inputs; profile load, copy plan, and keyboard order checked in Chromium only (no Firefox/WebKit here; code grepped for Safari-unsafe features).
- The bundled screenshot tool repeats the page top in full-page captures taller than ~8,000px. This is a capture artifact; the page height checks out.
