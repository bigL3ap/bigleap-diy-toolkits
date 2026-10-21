# Big Leap DIY Toolkits

Free, self-serve marketing toolkits from Big Leap. *Do the setup yourself. Spend your budget on strategy.*

Live (GitHub Pages, `main` only): https://bigl3ap.github.io/bigleap-diy-toolkits/ (noindex)

## What's here

| Path | What it is |
|---|---|
| `index.html` | The hub: the toolkits by service, plus the widget library (internal) |
| `journey.html` | The buyer-journey map, plus the DIY map of how the toolkits connect ("How it connects" tab) |
| (toolkit bar) | Client-facing pages on the left (Toolkits, Start here, Roadmap); internal pages on the right under "Internal" (Journey map, Sales assets, Widgets, Mockups, Status & review). Set in `tools/site_header.py`. |
| `review.html` | Status & review (internal): a To do tab (decisions, a review card per owner, before-launch to-dos from `data/open-items.json`) and a What's built tab (where everything stands, what changed). Replaces the old Buildout section and Team review page; `index.html#buildout` redirects here. |
| `roadmap.html` | Your Marketing Roadmap: three priorities built from the visitor's answers |
| `toolkits/<series>/` | The 18 public toolkits: RevOps (1–6 live, 7 draft), Paid Media, SEO, Digital PR, Email |
| `toolkits/plan/` | Strategy starters 1–4 (the Strategy series). 3 and 4 await Coby's method review. |
| `roadmap.html` | Your Marketing Roadmap: next priorities from the profile, the starters and toolkit progress. |
| `toolkits.json` | The toolkit catalog. Series drive the hub, the map and Previous and Next. Toolkits with a `review` note, and any `previews`, are listed on `review.html`. |
| `data/` | `connections.json` (map links), `widgets.json`, `open-items.json` (Status & review) |
| `widgets/`, `tiles/` | Embeddable mini-toolkits (three or more per service) and their 16:9 slide tiles. Built with `tools/build_widgets.py` and `tools/build_tiles.py`; listed in `data/widgets.json`, which also holds each owner's title and photo. |
| `mockups/` | Homepage and landing-page mockups |
| `tools/site_header.py` | Adds the shared header, toolkit bar, pager and tracking to every page. Run it after changing `toolkits.json`. |
| `tests/qa.py` | The automated QA suite |
| `docs/` | Authoring guide, data and storage contract, QA guide, build notes |

## Preview locally

```
python3 -m http.server 8000
# open http://localhost:8000/
```

Open pages through the server, not as files. Browsers block the data loads when a page is opened as a file.

## Before you push

```
python3 tools/site_header.py   # only if you changed toolkits.json or the header
python3 tests/qa.py
```

Pushing to `main` publishes the site within about a minute, so do the work on a branch.

## Guides

- `docs/DIY_TOOLKIT_AUTHORING.md`: how to build or change a toolkit so it fits the rest.
- `docs/STATE_AND_STORAGE.md`: what is saved in the browser, and the versioning rules.
- `docs/QA.md`: the automated suite and the manual checks.
