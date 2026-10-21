#!/usr/bin/env python3
"""DIY Toolkits QA suite.

Run from the repo root:
    python3 tests/qa.py            # static checks + browser checks (needs Python Playwright + Chromium)
    python3 tests/qa.py --static   # static checks only (no browser)

What it covers
  Static   JSON validity and cross-references (toolkits.json, data/*.json), every relative href/src
           resolves to a real file, same-page #anchors exist, owner names in open items are canonical,
           JavaScript features that break older Safari, and preview pages that must not leak into
           the public toolkit sequence.
  Browser  Every page loads with no console errors; no horizontal scroll at 390px; every toolkit
           prefills from a saved Business Profile and never overwrites it with example answers;
           "Copy my plan" produces text; Team Review renders every open item and every owner filter
           shows that owner's items; the toolkit bar's Team review link is reachable on mobile;
           keyboard focus is visible on the first interactive control; dark mode renders.

Exit code 0 when every check passes, 1 otherwise. Results print as PASS / FAIL / SKIP lines and a summary.
"""
import glob, html.parser, json, os, re, socket, subprocess, sys, threading, time, functools, http.server, socketserver

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = []  # (status, name, detail)


def rec(ok, name, detail=''):
    RESULTS.append(('PASS' if ok else 'FAIL', name, detail))


def skip(name, detail):
    RESULTS.append(('SKIP', name, detail))


def load(path):
    with open(os.path.join(ROOT, path), encoding='utf-8') as f:
        return json.load(f)


def pages():
    out = ['index.html', 'journey.html']
    for extra in ['review.html', 'roadmap.html']:
        if os.path.exists(os.path.join(ROOT, extra)):
            out.append(extra)
    out += sorted(os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, 'toolkits', '*', '*.html')))
    out += sorted(os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, 'widgets', '*.html')))
    out += sorted(os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, 'mockups', '*.html')))
    return out


# ---------------------------------------------------------------- static checks
CANON_OWNERS = {'Dallas Olsen', 'Scott Smoot', 'Coby Bush', 'Kristina Ainge', 'Erica Pounder', 'Shema Al-Darwish',
                'Whitney Sorensen', 'All owners'}


def check_json():
    data = {}
    for f in ['toolkits.json', 'data/connections.json', 'data/widgets.json', 'data/open-items.json']:
        try:
            data[f] = load(f)
            rec(True, f'JSON parses: {f}')
        except Exception as e:  # noqa
            rec(False, f'JSON parses: {f}', str(e))
    tk = data.get('toolkits.json')
    if tk:
        missing = [t['file'] for s in tk['series'] for t in s['toolkits'] if not os.path.exists(os.path.join(ROOT, t['file']))]
        rec(not missing, 'toolkits.json: every toolkit file exists', ', '.join(missing))
        for s in tk['series']:
            ns = [t['n'] for t in s['toolkits']]
            rec(ns == list(range(1, len(ns) + 1)), f'toolkits.json: {s["id"]} numbered 1..n', str(ns))
        rec(os.path.exists(os.path.join(ROOT, tk['start']['file'])), 'toolkits.json: start file exists')
        prev = tk.get('previews', [])
        pm = [p['file'] for p in prev if not os.path.exists(os.path.join(ROOT, p['file']))]
        rec(not pm, 'toolkits.json: every preview file exists', ', '.join(pm))
        pub = {t['file'] for s in tk['series'] for t in s['toolkits']}
        leak = [p['file'] for p in prev if p['file'] in pub]
        rec(not leak, 'previews are not listed in the public series', ', '.join(leak))
    cn = data.get('data/connections.json')
    if cn and tk:
        by = {s['id']: {t['n'] for t in s['toolkits']} for s in tk['series']}
        prev_ids = {p['id'] for p in tk.get('previews', [])}
        bad = [k for k, (sid, n) in cn['nodes'].items() if not (sid in by and n in by[sid])]
        rec(not bad, 'connections: every node maps to a public toolkit', ', '.join(bad))
        badedge = [e for e in cn['edges'] if e[0] not in cn['nodes'] or e[1] not in cn['nodes']]
        rec(not badedge, 'connections: every edge references known nodes', str(badedge[:3]))
        dup = len(cn['edges']) - len({(e[0], e[1]) for e in cn['edges']})
        rec(dup == 0, 'connections: no duplicate edges', f'{dup} duplicates')
        selfe = [e for e in cn['edges'] if e[0] == e[1]]
        rec(not selfe, 'connections: no self-links', str(selfe))
        empty = [e for e in cn['edges'] if len(e) < 3 or not str(e[2]).strip()]
        rec(not empty, 'connections: every edge explains why', str(empty[:3]))
        pe = cn.get('preview_edges', [])
        bad_pe = [e for e in pe if not ((e[0] in cn['nodes'] or e[0] in prev_ids) and (e[1] in cn['nodes'] or e[1] in prev_ids))]
        rec(not bad_pe, 'connections: preview edges reference known nodes or previews', str(bad_pe[:3]))
    wd = data.get('data/widgets.json')
    if wd:
        miss = [w['file'] for w in wd.get('widgets', []) if not os.path.exists(os.path.join(ROOT, w['file']))]
        miss += [t['file'] for t in wd.get('tiles', []) if not os.path.exists(os.path.join(ROOT, t['file']))]
        rec(not miss, 'widgets.json: every widget and tile file exists', ', '.join(miss))
    oi = data.get('data/open-items.json')
    if oi:
        req = ['title', 'owner', 'type', 'area', 'status', 'detail']
        badf = [i.get('title', '?') for i in oi['items'] if any(k not in i for k in req)]
        rec(not badf, 'open-items: every item has title/owner/type/area/status/detail', ', '.join(badf[:5]))
        owners = {o.strip() for i in oi['items'] for o in str(i['owner']).split(',')}
        odd = sorted(owners - CANON_OWNERS)
        rec(not odd, 'open-items: owner names are canonical full names', ', '.join(odd))
        types = {'Blocker', 'Waiting on', 'Decision', 'Owner review', 'To do', 'Other from the call'}
        badt = sorted({i['type'] for i in oi['items']} - types)
        rec(not badt, 'open-items: every type is a known type', ', '.join(badt))
    return data


class Links(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.ids = [], set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            self.ids.add(a['id'])
        for k in ('href', 'src'):
            v = a.get(k)
            if v and tag in ('a', 'link', 'img', 'script', 'iframe', 'source'):
                self.refs.append((tag, v))


def check_links():
    broken, anchors = [], []
    for page in pages():
        p = Links()
        with open(os.path.join(ROOT, page), encoding='utf-8') as f:
            p.feed(f.read())
        for tag, v in p.refs:
            if re.match(r'^(https?:|mailto:|tel:|data:|javascript:)', v) or v.startswith('//'):
                continue
            target, _, frag = v.partition('#')
            target = target.split('?')[0]
            if not target:
                if frag and not frag.startswith('connect:') and frag not in p.ids and not re.match(r'^[a-z-]+$', frag):
                    anchors.append(f'{page} -> #{frag}')
                continue
            full = os.path.normpath(os.path.join(ROOT, os.path.dirname(page), target))
            if not os.path.exists(full):
                broken.append(f'{page} -> {v}')
    rec(not broken, 'every relative href/src resolves to a file', '; '.join(broken[:10]) + (f' (+{len(broken)-10} more)' if len(broken) > 10 else ''))
    rec(not anchors, 'same-page anchors exist', '; '.join(anchors[:10]))


SAFARI_RISK = [
    (re.compile(r'\(\?<[=!]'), 'regex lookbehind (Safari < 16.4 throws at parse time)'),
    (re.compile(r'\.at\(\s*-?\d'), 'Array/String .at() (Safari < 15.4)'),
    (re.compile(r'structuredClone\('), 'structuredClone (Safari < 15.4)'),
    (re.compile(r'\.findLast(Index)?\('), 'findLast (Safari < 15.4)'),
    (re.compile(r'Object\.hasOwn\('), 'Object.hasOwn (Safari < 15.4)'),
]


def check_safari_js():
    hits = []
    for page in pages():
        with open(os.path.join(ROOT, page), encoding='utf-8') as f:
            s = f.read()
        for block in re.findall(r'<script[^>]*>(.*?)</script>', s, re.S):
            for rx, why in SAFARI_RISK:
                if rx.search(block):
                    hits.append(f'{page}: {why}')
    rec(not hits, 'no JavaScript features that break older Safari', '; '.join(sorted(set(hits))[:8]))


def check_preview_isolation(data):
    tk = data.get('toolkits.json') or {}
    prev = [p['file'] for p in tk.get('previews', [])]
    if not prev:
        skip('preview pages stay out of the public sequence', 'no previews defined')
        return
    leaks = []
    public = ['index.html', 'journey.html'] + [t['file'] for s in tk['series'] for t in s['toolkits']]
    for page in public:
        with open(os.path.join(ROOT, page), encoding='utf-8') as f:
            s = f.read()
        m = re.search(r'var SEQ = (\[.*?\]);', s)
        if m and any(pf in m.group(1) for pf in prev):
            leaks.append(page + ' (pager sequence)')
        for pf in prev:
            if os.path.basename(pf) in s and page in ('index.html', 'journey.html') and 'data-preview' not in s:
                leaks.append(f'{page} links {os.path.basename(pf)}')
    rec(not leaks, 'preview pages stay out of the public sequence and hub', '; '.join(leaks[:6]))


# ---------------------------------------------------------------- browser checks
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def serve():
    s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
    handler = functools.partial(Quiet, directory=ROOT)
    httpd = socketserver.ThreadingTCPServer(('127.0.0.1', port), handler)
    httpd.daemon_threads = True
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, f'http://127.0.0.1:{port}/'


PROFILE = {'v': 1, 'name': 'QA Test Co', 'industry': 'Manufacturing or industrial', 'model': 'b2b', 'offer': 'products',
           'ecommerce': 'none', 'locations': 'multi', 'reach': 'national', 'app': False, 'crm': 'other', 'website': True,
           'goal': 'leads', 'adBudget': 7500, 'ga4': 'yes', 'gtm': 'no', 'gbp': 'yes'}


def browser_checks(data):
    try:
        from playwright.sync_api import sync_playwright
    except Exception:
        skip('browser checks', 'Python Playwright is not installed')
        return
    httpd, base = serve()
    tk = data.get('toolkits.json') or {'series': []}
    kits = [t['file'] for s in tk['series'] for t in s['toolkits']] + [p['file'] for p in tk.get('previews', [])]
    with sync_playwright() as pw:
        b = pw.chromium.launch()

        def new(width=1280, height=900, storage=None, dark=False):
            ctx = b.new_context(viewport={'width': width, 'height': height}, color_scheme='dark' if dark else 'light')
            if storage is not None:
                ctx.add_init_script('try{localStorage.clear();' + ''.join(
                    f'localStorage.setItem({json.dumps(k)},{json.dumps(json.dumps(v))});' for k, v in storage.items()) + '}catch(e){}')
            pg = ctx.new_page()
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
            return ctx, pg, errs

        # 1. every page loads cleanly, desktop and 390px
        for width in (1280, 390):
            bad, wide = [], []
            ctx, pg, errs = new(width=width, storage={})
            for page in pages():
                errs.clear()
                pg.goto(base + page, wait_until='load'); pg.wait_for_timeout(350)
                if errs:
                    bad.append(f'{page}: {errs[0][:120]}')
                over = pg.evaluate('document.documentElement.scrollWidth - innerWidth')
                if over > 2:
                    wide.append(f'{page} (+{over}px)')
            ctx.close()
            rec(not bad, f'no console errors on any page at {width}px', '; '.join(bad[:6]))
            rec(not wide, f'no horizontal page scroll at {width}px', '; '.join(wide[:8]))

        # 2. profile prefill and protection, for every toolkit except the builder
        ctx, pg, errs = new(storage={'bl_diy_profile_v1': PROFILE})
        noprefill, overwrote = [], []
        for f in kits:
            if f.endswith('paid/01_What_Kind_of_Business_Are_You.html'):
                continue
            with open(os.path.join(ROOT, f), encoding='utf-8') as fh:
                if 'profile-strip' not in fh.read():
                    noprefill.append(f + ' (does not read the profile)')
                    continue
            pg.goto(base + f, wait_until='load'); pg.wait_for_timeout(300)
            strip = pg.evaluate("(document.getElementById('profile-strip')||{}).textContent||''")
            if 'QA Test Co' not in strip:
                noprefill.append(f)
            saved = pg.evaluate("localStorage.getItem('bl_diy_profile_v1')")
            if json.loads(saved or 'null') != PROFILE:
                overwrote.append(f)
        ctx.close()
        rec(not noprefill, 'every toolkit shows the saved Business Profile', '; '.join(noprefill[:6]))
        rec(not overwrote, 'no toolkit overwrites the saved Business Profile on load', '; '.join(overwrote[:6]))

        # 3. the builder never saves example answers over nothing, and saves real answers
        ctx, pg, errs = new(storage={})
        pg.goto(base + 'toolkits/paid/01_What_Kind_of_Business_Are_You.html'); pg.wait_for_timeout(300)
        rec(pg.evaluate("localStorage.getItem('bl_diy_profile_v1')") is None, 'Business Profile builder does not save example answers automatically')
        pg.fill('#name', 'Ñandú Café & Co'); pg.wait_for_timeout(200)
        saved = json.loads(pg.evaluate("localStorage.getItem('bl_diy_profile_v1')") or 'null')
        rec(bool(saved) and saved.get('name') == 'Ñandú Café & Co', 'Business Profile builder saves the visitor\'s own answers (non-ASCII safe)')
        code = pg.input_value('#code-out')
        ok = pg.evaluate("(c)=>{try{var b=c.slice(4);var p=JSON.parse(decodeURIComponent(escape(atob(b+'==='.slice((b.length+3)%4)))));return p.name}catch(e){return null}}", code)
        rec(ok == 'Ñandú Café & Co', 'BL1 profile code round-trips', str(ok))
        ctx.close()

        # 4. copy my plan works on every toolkit (clipboard may be blocked; fallback textarea counts)
        ctx, pg, errs = new(storage={})
        nocopy = []
        for f in kits:
            pg.goto(base + f, wait_until='load'); pg.wait_for_timeout(250)
            if not pg.query_selector('#copy-btn'):
                continue
            pg.evaluate("window.__copied='';try{navigator.clipboard.writeText=function(t){window.__copied=t;return Promise.resolve();}}catch(e){}")
            pg.click('#copy-btn'); pg.wait_for_timeout(200)
            txt = pg.evaluate("window.__copied || ((document.querySelector('#copy-host textarea')||{}).value||'')")
            if len(txt or '') < 80:
                nocopy.append(f)
        ctx.close()
        rec(not nocopy, '"Copy my plan" produces a plan on every toolkit', '; '.join(nocopy[:6]))

        # 5. Team Review: data, filters, mobile reach, failure state
        oi = data.get('data/open-items.json') or {'items': []}
        review_page = 'review.html' if os.path.exists(os.path.join(ROOT, 'review.html')) else 'index.html#review'
        ctx, pg, errs = new(storage={})
        pg.goto(base + review_page); pg.wait_for_timeout(700)
        n = pg.evaluate("document.querySelectorAll('#groups .item').length")
        rec(n == len(oi['items']), 'Team Review renders every open item', f'{n} of {len(oi["items"])}')
        owners = sorted({o.strip() for i in oi['items'] for o in str(i['owner']).split(',')} - {'All owners'})
        short = []
        for o in owners:
            pg.select_option('#owner-sel', o); pg.wait_for_timeout(80)
            got = pg.evaluate("document.querySelectorAll('#groups .item').length")
            want = len([i for i in oi['items'] if o in [x.strip() for x in str(i['owner']).split(',')] or str(i['owner']).strip() == 'All owners'])
            if got != want:
                short.append(f'{o}: {got}/{want}')
        rec(not short, 'Team Review owner filter shows each owner\'s items plus team-wide items', '; '.join(short))
        btns = pg.evaluate("[].map.call(document.querySelectorAll('button.link[data-owner]'),function(b){return b.getAttribute('data-owner')})")
        badb = []
        for o in btns:
            pg.click(f'button.link[data-owner="{o}"]'); pg.wait_for_timeout(80)
            if pg.evaluate("document.querySelectorAll('#groups .item').length") == 0:
                badb.append(o)
        rec(not badb, 'every agenda owner button shows items', ', '.join(badb))
        ctx.close()
        ctx, pg, errs = new(storage={})
        pg.route('**/data/open-items.json', lambda r: r.abort())
        pg.goto(base + review_page); pg.wait_for_timeout(700)
        msg = pg.evaluate("(document.getElementById('groups')||{}).textContent||''")
        rec('could not load' in msg.lower(), 'Team Review explains when open items fail to load', msg[:80])
        ctx.close()
        ctx, pg, errs = new(width=390, height=844, storage={})
        pg.goto(base + 'index.html'); pg.wait_for_timeout(500)
        a = pg.query_selector('.blh-tabs a[data-tab="review"]')
        reach = False
        if a:
            a.focus(); pg.wait_for_timeout(200)
            r = pg.evaluate("(()=>{var a=document.querySelector('.blh-tabs a[data-tab=review]').getBoundingClientRect();return [a.left,a.right,innerWidth]})()")
            reach = r[0] >= 0 and r[1] <= r[2] + 1
        rec(reach, 'Team review link scrolls into view when focused on a phone')
        ctx.close()

        # 6. keyboard focus visible on the first control of each toolkit
        ctx, pg, errs = new(storage={})
        nofocus = []
        for f in kits[:6] + kits[-4:]:
            pg.goto(base + f); pg.wait_for_timeout(200)
            # Tab from the top of the page until focus lands inside the question form, like a keyboard user.
            inside = False
            for _ in range(120):
                pg.keyboard.press('Tab')
                if pg.evaluate("!!(document.activeElement && document.activeElement.closest && document.activeElement.closest('#answers'))"):
                    inside = True
                    break
            if not inside:
                nofocus.append(f + ' (form not reachable by Tab)')
                continue
            vis = pg.evaluate("""(()=>{var e=document.activeElement;if(!e||e===document.body)return false;
              var c=[e,e.nextElementSibling,e.parentElement,e.parentElement&&e.parentElement.parentElement].filter(Boolean);
              return c.some(function(x){var s=getComputedStyle(x);return (s.outlineStyle!=='none'&&parseFloat(s.outlineWidth)>0)||(s.boxShadow&&s.boxShadow!=='none');});})()""")
            if not vis:
                nofocus.append(f)
        ctx.close()
        rec(not nofocus, 'first form control shows a visible keyboard focus', '; '.join(nofocus[:5]))

        # 7. dark mode renders the hub without errors
        ctx, pg, errs = new(storage={}, dark=True)
        pg.goto(base + 'index.html'); pg.wait_for_timeout(500)
        rec(not errs and pg.evaluate("document.querySelectorAll('#map .stop').length") >= 18, 'hub renders in dark mode with the full map', '; '.join(errs[:2]))
        ctx.close()

        # 8. roadmap (when present): empty state and personalized state
        if os.path.exists(os.path.join(ROOT, 'roadmap.html')):
            ctx, pg, errs = new(storage={})
            pg.goto(base + 'roadmap.html'); pg.wait_for_timeout(400)
            t = pg.evaluate("document.body.innerText")
            rec('Business Profile' in t and not errs, 'roadmap: useful empty state with no saved data', '; '.join(errs[:2]))
            ctx.close()
            ctx, pg, errs = new(storage={'bl_diy_profile_v1': PROFILE})
            pg.goto(base + 'roadmap.html'); pg.wait_for_timeout(400)
            pri = pg.evaluate("document.querySelectorAll('#priorities > li').length")
            rec(pri == 3 and not errs, 'roadmap: three priorities from a profile alone', f'{pri} priorities; ' + '; '.join(errs[:2]))
            ctx.close()
        b.close()
    httpd.shutdown()


def main():
    data = check_json()
    check_links()
    check_safari_js()
    check_preview_isolation(data)
    if '--static' not in sys.argv:
        browser_checks(data)
    w = max(len(r[1]) for r in RESULTS)
    for s, n, d in RESULTS:
        print(f'{s:4}  {n}' + (f'  ->  {d}' if d and s != 'PASS' else ''))
    c = {k: sum(1 for r in RESULTS if r[0] == k) for k in ('PASS', 'FAIL', 'SKIP')}
    print(f"\n{c['PASS']} passed, {c['FAIL']} failed, {c['SKIP']} skipped")
    sys.exit(1 if c['FAIL'] else 0)


if __name__ == '__main__':
    main()
