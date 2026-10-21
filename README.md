# Big Leap DIY Toolkits

Free, self-serve marketing toolkits from Big Leap. *Do the setup yourself. Spend your budget on strategy.*

Live (GitHub Pages, `main` only): https://bigl3ap.github.io/bigleap-diy-toolkits/ (noindex)

## What's here

| Path | What it is |
|---|---|
| `index.html` | The hub: the DIY map, the toolkits by service, widgets |
| `journey.html` | The buyer-journey map (internal strategy content) |
| `review.html` | Team review: agenda, drafts to review, open items. Internal, and not linked from toolkit content. |
| `roadmap.html` | Your Marketing Roadmap (internal draft): three priorities built from the visitor's answers |
| `toolkits/<series>/` | The 18 public toolkits: RevOps (1–6 live, 7 draft), Paid Media, SEO, Digital PR, Email |
| `toolkits/plan/` | Strategy starters 1–4, internal drafts. Listed under `previews` in `toolkits.json`. |
| `toolkits.json` | The toolkit catalog. Series drive the hub and Previous and Next; previews drive the review page. |
| `data/` | `connections.json` (map links), `widgets.json`, `open-items.json` (Team review) |
| `widgets/`, `tiles/` | Embeddable widgets and slide tiles |
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
