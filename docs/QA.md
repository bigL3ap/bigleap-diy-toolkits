# QA: how to check the DIY Toolkits

## 1. Automated suite (run before every push)

```
python3 tests/qa.py            # static and browser checks
python3 tests/qa.py --static   # static checks only, no browser needed
```

It needs Python 3 and, for the browser checks, Playwright with Chromium (`pip install playwright && python3 -m playwright install chromium`). It serves the repo on a local port by itself.

It reports PASS, FAIL, SKIP or KNOWN for each check, and exits non-zero on any FAIL. KNOWN is a documented gap waiting on an owner decision; it is listed in `tests/qa.py` and doesn't fail the run.

What it covers:
- **Data:** JSON validity and cross-references between `toolkits.json`, `data/connections.json`, `data/widgets.json` and `data/open-items.json`. Owner names are checked to be canonical.
- **Links:** every relative link and asset path resolves to a file.
- **Safari:** no JavaScript features that throw in older Safari.
- **Preview isolation:** draft previews stay out of the public list and out of Previous and Next.
- **Every page:** no console errors at 1280px and 390px, and no horizontal scroll at 390px.
- **Business Profile:** every toolkit shows a saved profile and never overwrites it. The builder never saves example answers, and the `BL1.` code round-trips with non-English characters.
- **Copy my plan:** produces a plan on every toolkit.
- **Team Review:** every open item renders, every owner filter works, every agenda button works, a load failure shows an error message, and the tab is reachable on a phone.
- **Keyboard:** Tab reaches each toolkit's form, and focus is visible.
- **Dark mode:** the hub renders in dark mode.
- **Roadmap:** shows a useful empty state, and gives three priorities from a profile alone.

## 2. Manual pass (before a release or after a big change)

Do these by hand; the suite can't judge them.

1. **Real Safari and Firefox:** open the hub, one toolkit from each series, a strategy starter and the roadmap. WebKit could not be installed in the build environment, so Safari has only been checked by the static scan.
2. **Phone:** do one toolkit end to end with your thumb. Check that the bottom "Your result so far" bar doesn't cover the button you need.
3. **Screen reader (VoiceOver or NVDA):** do one toolkit. Check that questions are announced with their options, and that result changes are announced (the result panel uses `aria-live` where it updates).
4. **Content:**
   - Read each changed result in all its states: example, your answers, from your profile, empty.
   - Every number needs a reason and every claim needs a source or a "rule of thumb" label.
5. **Journeys:** walk each one.
   - A first-time owner: hub, then Business Profile, then the roadmap, then the first priority.
   - A marketer with one problem: a direct link to a toolkit, without a profile.
   - A returning visitor: profile saved, then the roadmap shows their progress.
   - Keyboard only: one toolkit end to end.

## 3. After editing shared pieces

- Changed `tools/site_header.py`? Run it. Check `git diff` touches only what you meant, then run the suite.
- Changed `toolkits.json`? Run `tools/site_header.py` (the sequence comes from it), then the suite.
- Changed `data/connections.json`? Open the hub map and the journey "How each toolkit connects" tab. Click three nodes and check each arrow's reason reads correctly in its direction.
