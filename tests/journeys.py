#!/usr/bin/env python3
"""End-to-end visitor journeys for the DIY Toolkits, run in a real browser (Playwright + Chromium).

    python3 tests/journeys.py

Each journey starts with an empty browser profile unless it says otherwise, follows real links and
clicks, and checks what a visitor would see. Prints PASS / FAIL per step and exits non-zero on any FAIL.
"""
import functools, http.server, json, os, socketserver, sys, threading

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = []


def rec(journey, step, ok, detail=''):
    RESULTS.append((ok, journey, step, detail))


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def main():
    from playwright.sync_api import sync_playwright
    httpd = socketserver.ThreadingTCPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=ROOT))
    httpd.daemon_threads = True
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    B = f'http://127.0.0.1:{httpd.server_address[1]}/'
    with sync_playwright() as pw:
        br = pw.chromium.launch()

        def session(width=1280, height=900, storage=None):
            ctx = br.new_context(viewport={'width': width, 'height': height})
            if storage:
                ctx.add_init_script('if(!sessionStorage.getItem("seeded")){sessionStorage.setItem("seeded","1");' + ''.join(
                    f'localStorage.setItem({json.dumps(k)},{json.dumps(json.dumps(v))});' for k, v in storage.items()) + '}')
            pg = ctx.new_page(); errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
            return ctx, pg, errs

        def titles(pg):
            return pg.evaluate("[].map.call(document.querySelectorAll('#priorities > li .st-title'), e => e.textContent)")

        # 1. First-time small-business owner: hub -> Start here -> profile -> roadmap -> first priority
        J = '1 First-time owner'
        ctx, pg, errs = session()
        pg.goto(B + 'index.html'); pg.wait_for_timeout(500)
        pg.click('.blh-tabs a[data-tab="start"]'); pg.wait_for_load_state('load'); pg.wait_for_timeout(300)
        rec(J, '"Start here" opens the Business Profile', 'What_Kind_of_Business' in pg.url, pg.url)
        pg.fill('#name', 'Sunrise Plumbing'); pg.click('label[for=crm-none]'); pg.click('label[for=goal-calls]'); pg.wait_for_timeout(300)
        rec(J, 'profile saved after real answers', 'Sunrise Plumbing' in (pg.evaluate("localStorage.getItem('bl_diy_profile_v1')") or ''))
        pg.goto(B + 'roadmap.html'); pg.wait_for_timeout(500)
        t = titles(pg)
        rec(J, 'roadmap shows three priorities', len(t) == 3, str(t))
        first = pg.query_selector('#priorities > li .kit-link a')
        href = first.get_attribute('href') if first else ''
        if first:
            first.click(); pg.wait_for_load_state('load'); pg.wait_for_timeout(400)
        rec(J, 'first priority opens a toolkit', '/toolkits/' in pg.url, href)
        rec(J, 'no script errors', not errs, '; '.join(errs[:2]))
        ctx.close()

        # 2. Marketer with a specific problem: direct link, no profile, no assessments required
        J = '2 Specific problem, direct link'
        ctx, pg, errs = session()
        pg.goto(B + 'toolkits/email/01_Will_Your_Emails_Reach_the_Inbox.html'); pg.wait_for_timeout(500)
        rec(J, 'toolkit works without a profile or assessments', pg.evaluate("document.getElementById('answer').innerText.length") > 20)
        rid = pg.evaluate("(document.querySelector('#answers input[type=radio]:not(:checked)')||{}).id")
        pg.click(f'label[for="{rid}"]'); pg.wait_for_timeout(300)
        rec(J, 'pill switches to the visitor\'s answers', 'example' not in pg.inner_text('#example-pill').lower(), pg.inner_text('#example-pill'))
        pg.evaluate("window.__c='';navigator.clipboard.writeText=t=>{window.__c=t;return Promise.resolve();}")
        pg.click('#copy-btn'); pg.wait_for_timeout(200)
        plan = pg.evaluate('window.__c') or ''
        rec(J, 'copied plan uses absolute links', 'http://' in plan or 'https://' in plan, plan[:80])
        rec(J, 'no script errors', not errs, '; '.join(errs[:2]))
        ctx.close()

        # 3. Experienced leader: situation -> foundations -> roadmap reflects both
        J = '3 Experienced leader'
        ctx, pg, errs = session()
        pg.goto(B + 'toolkits/plan/01_Are_You_Solving_the_Right_Problem.html'); pg.wait_for_timeout(500)
        for lab in ['comp-many', 'demand-flat', 'spend-costly', 'choose-price', 'discount-often']:
            pg.click(f'label[for="{lab}"]')
        pg.wait_for_timeout(300)
        sit = json.loads(pg.evaluate("localStorage.getItem('bl_diy_assess_v1')") or '{}').get('situation', {}).get('result', {})
        rec(J, 'situation reads generate + differentiation', sit.get('market') == 'generate' and sit.get('limiting') == 'diff', str(sit)[:120])
        pg.goto(B + 'toolkits/plan/02_What_Do_You_Already_Have.html'); pg.wait_for_timeout(500)
        pg.click('label[for="position-missing"]'); pg.click('label[for="analytics-usable"]'); pg.wait_for_timeout(300)
        rec(J, 'foundations ranks positioning first', 'positioning' in pg.inner_text('#out-line').lower(), pg.inner_text('#out-line')[:100])
        pg.goto(B + 'roadmap.html'); pg.wait_for_timeout(500)
        basis = pg.inner_text('#basis').lower()
        rec(J, 'roadmap says it uses both checks', 'situation' in basis and 'foundations' in basis, basis[:120])
        t = titles(pg)
        rec(J, 'positioning is a top priority; usable analytics is not', any('worth choosing' in x for x in t) and not any('see what your marketing does' in x.lower() for x in t), str(t))
        rec(J, 'no script errors', not errs, '; '.join(errs[:2]))
        ctx.close()

        # 4. Returning visitor with saved progress
        J = '4 Returning visitor'
        prof = {'v': 1, 'name': 'Northwind Legal', 'industry': 'Legal services', 'model': 'b2c', 'offer': 'services', 'ecommerce': 'none', 'locations': 'one', 'reach': 'local', 'app': False, 'crm': 'hubspot', 'website': True, 'goal': 'leads', 'adBudget': 4000, 'ga4': 'no', 'gtm': 'no', 'gbp': 'yes'}
        progress = {'v': 1, 'kits': {'revops-07': {'first': '2026-10-01T10:00:00Z', 'last': '2026-10-02T10:00:00Z', 'worked': True, 'headline': '3 of 7 core pieces missing'}}}
        ctx, pg, errs = session(storage={'bl_diy_profile_v1': prof, 'bl_diy_progress_v1': progress})
        pg.goto(B + 'roadmap.html'); pg.wait_for_timeout(500)
        txt = pg.inner_text('#priorities')
        rec(J, 'started toolkit shows "In progress"', 'In progress' in txt, txt[:160])
        rec(J, 'worked toolkit listed with its result', '3 of 7 core pieces missing' in pg.inner_text('#known'))
        before = titles(pg)
        pg.click('#priorities > li:first-child label.opt'); pg.wait_for_timeout(300)
        rec(J, '"I\'ve done this" moves the roadmap on', titles(pg)[0] != before[0] and before[0] in pg.inner_text('#done'), f'{before} -> {titles(pg)}')
        pg.reload(); pg.wait_for_timeout(400)
        rec(J, 'done mark persists after reload', before[0] in pg.inner_text('#done'))
        pg.goto(B + 'toolkits/seo/01_Can_Google_Find_and_Trust_Your_Site.html'); pg.wait_for_timeout(400)
        rec(J, 'profile prefills a later toolkit', 'Northwind Legal' in pg.inner_text('#profile-strip'))
        rec(J, 'no script errors', not errs, '; '.join(errs[:2]))
        ctx.close()

        # 5. Incomplete information: everything "not sure"
        J = '5 Incomplete information'
        ctx, pg, errs = session()
        pg.goto(B + 'toolkits/plan/01_Are_You_Solving_the_Right_Problem.html'); pg.wait_for_timeout(500)
        for k in ['comp', 'demand', 'share', 'unserved', 'unprompted', 'choose', 'discount', 'referral']:
            pg.click(f'label[for="{k}-unsure"]')
        pg.click('label[for="spend-untried"]'); pg.click('label[for="cac-unknown"]'); pg.click('label[for="worth-unknown"]'); pg.wait_for_timeout(300)
        out = pg.inner_text('#answer')
        rec(J, 'situation says it is not clear yet, without guessing', 'Not clear' in out, out[:100])
        rec(J, 'every unknown gets a "how to find out"', pg.evaluate("document.querySelectorAll('#unknowns li').length") >= 8)
        pg.goto(B + 'toolkits/plan/02_What_Do_You_Already_Have.html'); pg.wait_for_timeout(400)
        for a in pg.evaluate("[].map.call(document.querySelectorAll('#areas input[value=unknown]'), i => i.id)"):
            pg.click(f'label[for="{a}"]')
        pg.wait_for_timeout(300)
        rec(J, 'all-unknown foundations still give a useful next step', 'check' in pg.inner_text('#out-line').lower() or pg.evaluate("document.querySelectorAll('#first > li').length") > 0, pg.inner_text('#out-line')[:100])
        rec(J, 'no script errors', not errs, '; '.join(errs[:2]))
        ctx.close()

        # 6. Declines the optional assessments: everything still works, nothing gated
        J = '6 Skips optional assessments'
        ctx, pg, errs = session(storage={'bl_diy_profile_v1': prof})
        pg.goto(B + 'roadmap.html'); pg.wait_for_timeout(400)
        rec(J, 'roadmap works from the profile alone', len(titles(pg)) == 3)
        rec(J, 'assessments offered as optional', 'Optional' in pg.inner_text('#sharpen'))
        tk = json.load(open(os.path.join(ROOT, 'toolkits.json')))
        gated = []
        for s in tk['series']:
            for t in s['toolkits']:
                pg.goto(B + t['file']); pg.wait_for_timeout(150)
                if pg.evaluate("document.getElementById('answer') ? document.getElementById('answer').innerText.length : 0") < 20:
                    gated.append(t['file'])
        rec(J, 'every public toolkit gives a result with no prerequisite', not gated, ', '.join(gated[:4]))
        rec(J, 'no script errors', not errs, '; '.join(errs[:2]))
        ctx.close()

        # 7. Mobile visitor (390 x 844)
        J = '7 Mobile visitor'
        ctx, pg, errs = session(width=390, height=844)
        over = []
        for u in ['index.html', 'toolkits/paid/01_What_Kind_of_Business_Are_You.html', 'toolkits/plan/01_Are_You_Solving_the_Right_Problem.html', 'toolkits/plan/02_What_Do_You_Already_Have.html', 'toolkits/plan/03_What_Makes_You_Worth_Choosing.html', 'toolkits/plan/04_Would_Your_Customers_Recommend_You.html', 'roadmap.html', 'review.html', 'journey.html']:
            pg.goto(B + u); pg.wait_for_timeout(300)
            if pg.evaluate('document.documentElement.scrollWidth - innerWidth') > 2:
                over.append(u)
        rec(J, 'no sideways scrolling on key pages', not over, ', '.join(over))
        pg.goto(B + 'toolkits/paid/01_What_Kind_of_Business_Are_You.html'); pg.wait_for_timeout(300)
        small = pg.evaluate("[].filter.call(document.querySelectorAll('#answers .seg label'), l => { const r = l.getBoundingClientRect(); return r.width && r.height < 40; }).length")
        rec(J, 'answer buttons are large enough to tap (40px+)', small == 0, f'{small} small targets')
        rec(J, 'no script errors', not errs, '; '.join(errs[:2]))
        ctx.close()

        # 8. Keyboard-only visitor on the roadmap
        J = '8 Keyboard only'
        ctx, pg, errs = session(storage={'bl_diy_profile_v1': prof})
        pg.goto(B + 'roadmap.html'); pg.wait_for_timeout(400)
        reached = False
        for _ in range(80):
            pg.keyboard.press('Tab')
            if pg.evaluate("document.activeElement && document.activeElement.name === 'goal'"):
                reached = True; break
        rec(J, 'Tab reaches the goal choice', reached)
        if reached:
            pg.keyboard.press('ArrowRight'); pg.wait_for_timeout(300)
            rec(J, 'arrow keys change the goal and save it', 'goal' in (pg.evaluate("localStorage.getItem('bl_diy_assess_v1')") or ''))
        got = False
        for _ in range(80):
            pg.keyboard.press('Tab')
            if pg.evaluate("document.activeElement && !!document.activeElement.getAttribute('data-done')"):
                got = True; break
        if got:
            before = titles(pg)[0]
            pg.keyboard.press('Space'); pg.wait_for_timeout(300)
        rec(J, 'Tab and Space mark a priority done', got and before in pg.inner_text('#done'))
        rec(J, 'no script errors', not errs, '; '.join(errs[:2]))
        ctx.close()
        br.close()
    httpd.shutdown()
    for ok, j, s, d in RESULTS:
        print(('PASS' if ok else 'FAIL') + f'  [{j}] {s}' + ('' if ok or not d else f'  ->  {d}'))
    f = sum(1 for r in RESULTS if not r[0])
    print(f'\n{len(RESULTS) - f} passed, {f} failed')
    sys.exit(1 if f else 0)


if __name__ == '__main__':
    main()
