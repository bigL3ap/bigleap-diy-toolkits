# Big Leap DIY Toolkits

Free, self-serve marketing toolkits from Big Leap. *Do the setup yourself. Spend your budget on strategy.*

Live (GitHub Pages, `main` only): https://bigl3ap.github.io/bigleap-diy-toolkits/ (noindex)

## What's here

| Path | What it is |
|---|---|
| `index.html` | **Start here**, the landing page and the site's front door: what the toolkits are, who wrote them, how they work, the toolkit map, each service with a live widget, where DIY stops, FAQs. Old hub hashes (`#toolkits`, `#seo`, `#widgets`, `#buildout`…) redirect to their new pages. |
| `toolkits.html` | **All toolkits**: the catalog by service, with search and service filters (`#revops`, `#paid`, … select a service). |
| `my-profile.html`, `your-journey.html`, `roadmap.html`, `progress.html` | **My Profile** and its sub-tabs: Profile & answers, Journey, Roadmap, Progress. |
| `journey.html` | Customer journey (internal): segments, the campaign flow, how the toolkits connect, measurement, service-team buy-in. |
| `sales.html`, `widgets.html`, `mockups/homepage.html` | **Assets** (internal) and its sub-tabs: Sales deck & talk tracks, Widgets & tiles, Page mockups. `mockups/toolkits-landing.html` now redirects to `index.html`. |
| (toolkit bar) | Client side on the left (Start here, All toolkits menu, My Profile); internal pages on the right under "Internal" (Customer journey, Assets, Status & review). Sub-tabs for My Profile and Assets are set in `GROUPS` in `tools/site_header.py`. |
| `review.html` | Status & review (internal): a To do tab and a What's built tab. |
| `toolkits/<series>/` | The 18 public toolkits: RevOps (1–6 live, 7 draft), Paid Media, SEO, Digital PR, Email |
| `toolkits/plan/` | Strategy starters 1–4 (the Strategy series). 3 and 4 await Coby's method review. |
| `toolkits.json` | The toolkit catalog. Series drive the hub, the map and Previous and Next. Toolkits with a `review` note, and any `previews`, are listed on `review.html`. |
| `data/` | `connections.json` (map links), `widgets.json`, `open-items.json` (Status & review) |
| `widgets/`, `tiles/` | Embeddable mini-toolkits (three or more per service) and their 16:9 slide tiles. Built with `tools/build_widgets.py` and `tools/build_tiles.py`; listed in `data/widgets.json`, which also holds each owner's title and photo. |
| `mockups/` | The bigleap.com homepage mockup (the landing-page mockup became `index.html`) |
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
