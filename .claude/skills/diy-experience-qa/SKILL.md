---
name: diy-experience-qa
description: Check the Big Leap DIY Toolkits site end to end before a push or release: run the automated suite, then the manual checks for links, flows, profile reuse, accessibility, mobile and content. Use after any change to toolkits, the hub, the journey map, the roadmap or the shared header.
---

# DIY experience QA

1. Run `python3 tests/qa.py` from the repo root.
   - Fix every FAIL.
   - A KNOWN line is a documented gap. Leave it, unless the change was meant to fix it; if so, remove its entry from `tests/qa.py`.
2. If the suite can't run (no Playwright), run `python3 tests/qa.py --static` and say clearly that the browser checks were not run.
3. Do the manual pass in `docs/QA.md` §2 for whatever changed. At minimum:
   - Each changed result in all its states: example, your answers, from your profile, empty.
   - One phone-width pass.
   - One keyboard-only pass.
4. For changes to `data/connections.json`:
   - Open the hub map and the journey Connect tab.
   - Confirm each changed arrow points from the toolkit that helps to the one it helps.
   - Confirm the reason reads correctly in that direction.
5. Report what was actually run, sorted into: passed, failed, fixed and retested, blocked, and not tested. Never mark a check passed that wasn't run.
