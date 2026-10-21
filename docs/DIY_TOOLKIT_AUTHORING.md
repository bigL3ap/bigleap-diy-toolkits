# Authoring a DIY toolkit

How to add or change a toolkit so it looks, behaves and connects like every other one. Read `docs/STATE_AND_STORAGE.md` first.

## The shape of every toolkit

Each toolkit is one self-contained HTML file in `toolkits/<series>/NN_Title_With_Underscores.html`. There is no build step: the toolkit's styles and scripts live in the file. The fastest correct start is to copy the most similar existing toolkit and replace its questions and logic.

Every toolkit has the same parts, with the same ids, because the shared header script and the tests rely on them:

| Part | id or class | Notes |
|---|---|---|
| Draft strip | `.draft-banner` | Drafts only: "Draft 1 · for internal review · Owner: …" |
| Masthead | `.masthead` | Wordmark, eyebrow ("<Series> DIY Toolkit n of m"), `h1` question title, one-sentence `.lede` promise |
| Business Profile strip | `#profile-strip` | `renderProfileStrip()`; mark prefilled answers with `.pf-tag` "From your profile" |
| Series stepper | `#stepper-list` | `renderStepper(n)` |
| Question form | `#col-q > form#answers` | One `.q` per question. Label first, then the control, then `.q-help`. The header script lays these out in two columns. |
| Example state | `#example-pill`, `#example-text`, `#restore-example` | Every page opens with realistic example answers. The pill says "Example answers" until the visitor changes something. |
| Result | `#answer` with `.hero-fig` and `.answer-line` | One number or word, one plain sentence. The progress recorder reads these. |
| Deliverables | `.panel.deliv` sections | What to do, in order, with the free toolkit for each step |
| Closing | `.closing` | `#copy-btn` "Copy my plan", optional print, `#cta-link` "Talk to <owner>" |
| Next and related | `#next`, `#xlinks` | `renderNext(key, why)` and `renderXlinks([...])` using the shared `LINKS` map |

## Content rules

- **Every toolkit must answer five questions:** what we learned, why it matters, what to do, how to do it, and what's next.
- **Never withhold the plan.** The whole plan is on the page and in "Copy my plan". "Talk to <owner>" is optional and never required.
- **Plain English.** Explain any acronym the first time. One idea per sentence.
- **Explain every recommendation.** Show the reason next to it. Mark rules of thumb as rules of thumb. No invented statistics, no ROI promises, no guarantees.
- **No commitments nobody approved.** Avoid "exactly what we'd build" or "the scope of any campaign we run". Use "a good place to start", "what we'd look at first".
- **"Not sure" is a valid answer.** Turn it into "how to find out", not a fail.
- **Copied plans use absolute links.** Use `absUrl()` / `linkPlain()`, so a pasted plan still works.

## Data rules

- **Read the profile; don't rewrite it.** Use `loadProfile()`; write it only when a visitor pastes a code.
- **Example answers are never saved and never presented as the visitor's.** Track `touched` and switch state only on real input. When a profile loads, fields it doesn't supply stay marked as examples, or start blank.
- **New shared data needs a design first.** Agree a versioned key or section in `docs/STATE_AND_STORAGE.md` before adding it.

## Accessibility and layout

- Radio groups: `role="radiogroup"` with `aria-labelledby`. Use the `.seg` pattern, or `.opts` for long options and checkboxes.
- Every input has a label. Focus stays visible (the shared CSS handles it; don't remove outlines).
- Don't carry meaning by color alone: pair it with a word or an icon (✓, !, ✕, ?).
- Check at 390px wide: no horizontal page scroll. Wide tables go in `.table-wrap`.
- Respect `prefers-reduced-motion` for any scrolling or animation.

## Wiring a new toolkit in

1. Add it to `toolkits.json`.
   - A public toolkit goes into its series.
   - A draft that should not be public yet goes under `"previews"`. Previews show on `review.html` and are never added to the public list, the map or Previous and Next.
   - A **new series** also needs: a colour, node prefix and id in `index.html` (`COLORS`, `DARK_COLORS`, `PFX`, `SERVICE_IDS`); a tab and its place in `ORDER` in `tools/site_header.py`; and its toolkits in `journey.html` (`K`, `SERIES`, `SERIES_ORDER`, `CAMPAIGN`, and a `--c-<series>` colour). The Strategy series is the worked example.
2. Add its key to the `LINKS` map in the pages that should link to it.
3. If it has real relationships with other toolkits, add them to `data/connections.json`. Each needs a reason, and the arrow must point from the toolkit that helps to the one it helps. Don't add links just to fill the map.
4. Run `python3 tools/site_header.py` to add the shared header, toolkit bar, pager and tracking.
5. Run `python3 tests/qa.py` and fix anything it reports.
6. Add the toolkit's owner questions to `toolkits/<series>/BUILD_NOTES.md` and any open items to `data/open-items.json`.

## Tracking (already wired by the shared script)

The shared script sends `diy_*` events to `window.dataLayer` from every page: view, start, copy, download, next, CTA and cross-link clicks. Don't add personal data to events. Don't rename events; reports depend on them. GA4 and HubSpot stay off until `GTM_ID` / `HUBSPOT_ID` are set in `tools/site_header.py`. Read the consent note there first.

## The strategy starters

`toolkits/plan/01–04` and `roadmap.html` follow the same structure. They share one extra block (assessment storage, the three motions and their depths) and a few extra styles. These are marked "Strategy starters" in the CSS and the script. To change all four, change each file.
