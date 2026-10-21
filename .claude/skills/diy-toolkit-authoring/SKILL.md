---
name: diy-toolkit-authoring
description: Build or change a Big Leap DIY toolkit so it matches the existing toolkits (structure, Business Profile, storage, content rules, accessibility, wiring). Use when adding a toolkit, a strategy starter or a widget, or when editing a toolkit's questions, logic or results.
---

# DIY toolkit authoring

1. Read `docs/DIY_TOOLKIT_AUTHORING.md` and `docs/STATE_AND_STORAGE.md` before writing anything.
2. Start from the closest existing toolkit file: copy it, then replace the questions and logic. Keep every id the guide lists (`#answers`, `#example-pill`, `#answer`, `#copy-btn`, `#next`, `#xlinks`, `#profile-strip`).
3. Keep the design: reuse the toolkit's CSS classes (`.q`, `.seg`, `.opts`, `.panel.deliv`, `.steps`, `.chip`). Don't add new visual patterns unless the change is approved.
4. Data:
   - Read the Business Profile with `loadProfile()`; never write it.
   - Never save example answers, and never present them as the visitor's.
   - New shared data needs a versioned key or section, documented in `docs/STATE_AND_STORAGE.md`.
5. Content: answer what we learned, why it matters, what to do, how, and what's next.
   - Explain every recommendation; label rules of thumb.
   - No withheld value, no invented numbers, no unapproved commitments.
   - Copied plans use absolute links.
6. Never edit inside the generated blocks (`<!-- bl-header -->`, `bl-pager`, `bl-header-css`, `bl-header-js`, `bl-track-js`). Run `python3 tools/site_header.py` instead.
7. Wire it in:
   - Add it to `toolkits.json`: its series if public, `previews` if it's a draft.
   - Add it to the `LINKS` maps.
   - Add only genuine edges to `data/connections.json`.
8. Run `python3 tests/qa.py`. Then use the `diy-experience-qa` skill for the manual checks before you call it done.
9. Work on a branch. Pushing to `main` publishes the site.
