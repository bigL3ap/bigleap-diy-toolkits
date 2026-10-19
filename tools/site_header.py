#!/usr/bin/env python3
"""Big Leap site header for every DIY Toolkits page.

Tier 1 copies the bigleap.com header (logo, Services / Who We Serve / Case Studies / Resources / About menus,
"Get Your Custom Strategy"), with links to the live site, so the toolkits read as part of bigleap.com.
Tier 2 is the toolkit bar: Dashboard · Journey map · Team review, plus Previous / Next on toolkit pages.

Run from the repo root after any change to toolkits.json or the menu below:  python3 tools/site_header.py
It is idempotent: it replaces everything between <!-- bl-header --> and <!-- /bl-header -->.
Menu links were taken from bigleap.com on Oct 19, 2026.
"""
import html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BL = 'https://www.bigleap.com'
UTM = '?utm_source=diy-toolkits&utm_medium=site-header'

MENU = [
    ('Services', BL + '/services/', [
        ('SEO', [('SEO Marketing', '/services/seo-marketing/'), ('AI SEO', '/services/ai-seo/'), ('Local SEO', '/services/local-seo/'), ('Technical SEO', '/services/technical-seo/'), ('Site Migrations', '/services/seo-site-migrations/')]),
        ('Paid Advertising', [('Paid Advertising', '/services/paid-advertising/'), ('Paid Search Ads', '/services/paid-search/'), ('Google Ads Agency', '/services/paid-search/google-ads-agency/'), ('Paid Social Ads', '/services/paid-social/'), ('Retargeting Ads', '/services/retargeting/')]),
        ('More services', [('RevOps', '/services/revops-agency/'), ('Content Marketing', '/services/content-marketing/'), ('Digital PR', '/services/digital-pr/'), ('Reputation Management', '/services/reputation-management/'), ('Conversion Rate Optimization', '/services/cro-marketing/')]),
    ]),
    ('Who We Serve', None, [
        ('By business type', [('Enterprise', '/who-we-serve/enterprise/'), ('Multi-Location & Franchise', '/who-we-serve/multi-location/'), ('Ecommerce & DTC', '/who-we-serve/ecommerce/'), ('B2B', '/who-we-serve/b2b/'), ('SaaS', '/who-we-serve/saas/'), ('Private Equity & Investors', '/who-we-serve/investors/')]),
        ('By industry', [('Automotive', '/who-we-serve/automotive/'), ('Contractor / HVAC', '/who-we-serve/home-contractor-and-hvac/'), ('Finance', '/who-we-serve/finance/'), ('Food & Beverage', '/who-we-serve/food-and-beverage/'), ('Higher Education', '/who-we-serve/higher-education/'), ('Information Technology', '/who-we-serve/information-technology/'), ('Insurance', '/who-we-serve/insurance/'), ('Legal', '/who-we-serve/legal/')]),
        ('', [('Manufacturing', '/who-we-serve/manufacturing/'), ('Medical Practices', '/who-we-serve/medical-practices/'), ('Mental Health', '/who-we-serve/mental-health/'), ('Nonprofit', '/who-we-serve/nonprofit/'), ('Optometrists', '/who-we-serve/optometrists/'), ('Retail', '/who-we-serve/retail/'), ('Roofers', '/who-we-serve/roofing/')]),
    ]),
    ('Case Studies', BL + '/digital-marketing-seo-case-studies/', [
        ('By business type', [('B2B Case Studies', '/b2b-case-studies/'), ('Enterprise Case Studies', '/enterprise-case-studies/'), ('Local & Multi-Location', '/local-and-multilocation-case-studies/'), ('Ecommerce Case Studies', '/ecommerce-case-studies/'), ('View All Case Studies', '/digital-marketing-seo-case-studies/')]),
    ]),
    ('Resources', BL + '/blog/digital-marketing-free-resource-roundup/', [
        ('Blog', [('Content Marketing', '/blog/category/content-marketing/'), ('Conversion Rate Optimization', '/blog/category/conversion-optimization/'), ('Paid Advertising', '/blog/category/paid-advertising/'), ('SEO', '/blog/category/seo/'), ('View All Blog Posts', '/blog/')]),
        ('Tools', [('Free DIY Toolkits', 'HUB'), ('Digital Marketing Budget Calculator', '/digital-marketing-budget-calculator/'), ('Digital Marketing Tool Kit', '/blog/your-free-digital-marketing-tool-kit/'), ('Partnership Pulse Check', '/blog/your-client-agency-partnership-pulse-check/'), ('Site Health Checklist', '/blog/your-16-point-site-health-checklist/')]),
        ('Podcast', [('Sweet Takes Podcast', '/podcasts/')]),
    ]),
    ('About', BL + '/about-us/', [
        ('', [('About Us', '/about-us/'), ('Our Team', '/about-us/#our-leadership-team'), ('Careers', '/careers/'), ('Contact Us', '/contact-us/')]),
    ]),
]

CSS = r"""<style id="bl-header-css">
/* Big Leap site header (tools/site_header.py). Always light, like bigleap.com. */
.blh, .blh * { box-sizing: border-box; }
.blh { position: relative; z-index: 60; font-family: "Open Sans", "Segoe UI", Arial, sans-serif; color: #143D55; -webkit-text-size-adjust: 100%; }
.blh a { color: inherit; }
.blh :focus-visible { outline: 3px solid #3187B5; outline-offset: 2px; border-radius: 6px; }
.blh-bar { background: #fff; border-bottom: 1px solid #D4DADF; }
.blh-in { max-width: 1240px; margin: 0 auto; padding: 0 max(20px, env(safe-area-inset-left)) 0 max(20px, env(safe-area-inset-right)); }
.blh-bar .blh-in { display: flex; align-items: center; justify-content: space-between; gap: 18px; min-height: 76px; }
.blh-logo { display: block; flex: 0 0 auto; }
.blh-logo img { display: block; height: 40px; width: auto; }
.blh-nav { display: flex; align-items: center; gap: 4px; }
.blh-nav > ul { list-style: none; margin: 0; padding: 0; display: flex; align-items: center; gap: 2px; }
.blh-nav > ul > li { position: relative; }
.blh-top { display: inline-flex; align-items: center; gap: 7px; min-height: 44px; padding: 8px 11px; border: 0; background: none; color: #143D55; font: 700 15px "Raleway", "Segoe UI", Arial, sans-serif; letter-spacing: -0.2px; text-decoration: none; cursor: pointer; white-space: nowrap; border-radius: 8px; }
.blh-top:hover { color: #3187B5; }
.blh-top .car { width: 7px; height: 7px; border-right: 2px solid currentColor; border-bottom: 2px solid currentColor; transform: rotate(45deg); margin-top: -4px; transition: transform .15s ease; }
.blh-li.open > .blh-top .car { transform: rotate(-135deg); margin-top: 3px; }
.blh-top.is-here { box-shadow: inset 0 -3px 0 #EA4335; border-radius: 0; }
.blh-new { display: inline-block; padding: 1px 7px; border-radius: 999px; background: #EA4335; color: #fff; font: 700 10.5px/1.5 "Open Sans", Arial, sans-serif; letter-spacing: 0; }
.blh-dd { display: none; position: absolute; top: calc(100% + 6px); left: 50%; transform: translateX(-50%); background: #fff; border: 1px solid #D4DADF; border-radius: 12px; box-shadow: 0 18px 40px rgba(20,61,85,.16); padding: 18px 20px; gap: 6px 28px; grid-auto-flow: column; grid-auto-columns: minmax(170px, auto); }
.blh-li:last-child .blh-dd, .blh-li.r .blh-dd { left: auto; right: 0; transform: none; }
.blh-li.open > .blh-dd { display: grid; }
@media (hover: hover) and (min-width: 1081px) { .blh-li:hover > .blh-dd { display: grid; } .blh-li:hover > .blh-top .car { transform: rotate(-135deg); margin-top: 3px; } }
.blh-dd::before { content: ""; position: absolute; left: 0; right: 0; top: -10px; height: 10px; }
.blh-col h6 { margin: 0 0 6px; font: 700 12px "Open Sans", Arial, sans-serif; color: #5F6E79; min-height: 16px; }
.blh-col ul { list-style: none; margin: 0; padding: 0; display: grid; gap: 2px; }
.blh-col a { display: flex; align-items: center; gap: 8px; min-height: 34px; padding: 4px 6px; margin: 0 -6px; border-radius: 6px; font: 600 14.5px/1.3 "Open Sans", Arial, sans-serif; color: #143D55; text-decoration: none; white-space: nowrap; }
.blh-col a:hover { background: #EEF3F8; color: #246D96; }
.blh-cta { display: inline-flex; align-items: center; min-height: 44px; margin-left: 8px; padding: 10px 18px; border-radius: 25px; background: #143D55; color: #fff !important; font: 700 14px "Raleway", "Segoe UI", Arial, sans-serif; text-decoration: none; white-space: nowrap; }
.blh-cta:hover { background: #1D4D69; }
.blh-burger { display: none; align-items: center; justify-content: center; gap: 8px; min-height: 44px; min-width: 44px; padding: 8px 14px; border: 1px solid #D4DADF; border-radius: 10px; background: #fff; color: #143D55; font: 700 14px "Open Sans", Arial, sans-serif; cursor: pointer; }
.blh-burger i { position: relative; width: 18px; height: 2px; background: currentColor; display: inline-block; }
.blh-burger i::before, .blh-burger i::after { content: ""; position: absolute; left: 0; width: 18px; height: 2px; background: currentColor; }
.blh-burger i::before { top: -6px; } .blh-burger i::after { top: 6px; }
/* Tier 2: toolkit bar */
.blh-sub { background: #EEF3F8; border-bottom: 1px solid #D4DADF; }
.blh-sub .blh-in { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 4px 16px; min-height: 52px; padding-top: 4px; padding-bottom: 4px; }
.blh-crumb { display: flex; flex-wrap: wrap; align-items: center; gap: 2px 4px; }
.blh-crumb .home { font: 800 15px "Raleway", "Segoe UI", Arial, sans-serif; color: #143D55; text-decoration: none; margin-right: 10px; }
.blh-tabs { display: flex; flex-wrap: wrap; gap: 2px; }
.blh-tabs a { display: inline-flex; align-items: center; min-height: 40px; padding: 6px 12px; border-radius: 999px; font: 600 14px "Open Sans", Arial, sans-serif; color: #143D55; text-decoration: none; }
.blh-tabs a:hover { background: #DAE9F2; }
.blh-tabs a[aria-current="page"] { background: #143D55; color: #fff; }
.blh-right { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; }
.blh-where { font-size: 13px; color: #5F6E79; }
.blh-pn { display: flex; gap: 8px; }
.blh-pn a { display: inline-flex; align-items: center; gap: 6px; min-height: 40px; max-width: 300px; padding: 6px 14px; border: 1px solid #D4DADF; border-radius: 999px; background: #fff; color: #143D55; font: 600 13.5px "Open Sans", Arial, sans-serif; text-decoration: none; }
.blh-pn a:hover { border-color: #3187B5; }
.blh-pn a b { flex: 0 0 auto; }
.blh-pn a span { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.blh-theme { min-height: 40px; min-width: 40px; border: 1px solid #D4DADF; border-radius: 999px; background: #fff; color: #143D55; cursor: pointer; font-size: 16px; }
@media (max-width: 1080px) {
  .blh-burger { display: inline-flex; }
  .blh-nav { display: none; position: absolute; left: 0; right: 0; top: 100%; background: #fff; border-bottom: 1px solid #D4DADF; box-shadow: 0 18px 30px rgba(20,61,85,.12); padding: 8px max(20px, env(safe-area-inset-left)) 18px; flex-direction: column; align-items: stretch; max-height: calc(100vh - 80px); overflow-y: auto; }
  .blh.menu-open .blh-nav { display: flex; }
  .blh-nav > ul { flex-direction: column; align-items: stretch; }
  .blh-top { width: 100%; justify-content: space-between; padding: 12px 4px; border-bottom: 1px solid #EEF3F8; border-radius: 0; }
  .blh-top.is-here { box-shadow: inset 4px 0 0 #EA4335; padding-left: 12px; }
  .blh-dd { position: static; transform: none; box-shadow: none; border: 0; padding: 4px 4px 12px; grid-auto-flow: row; grid-auto-columns: auto; }
  .blh-col a { white-space: normal; }
  .blh-cta { margin: 14px 0 0; justify-content: center; }
}
@media (max-width: 640px) {
  .blh-bar .blh-in { min-height: 64px; }
  .blh-logo img { height: 32px; }
  .blh-sub .blh-in { flex-direction: column; align-items: stretch; padding-top: 6px; padding-bottom: 8px; }
  .blh-crumb { justify-content: space-between; }
  .blh-crumb .home { width: 100%; }
  .blh-sub .blh-in { position: relative; }
  .blh-tabs { width: 100%; display: grid; grid-template-columns: 1fr 1fr; gap: 4px; }
  .blh-tabs a { justify-content: center; padding: 6px 8px; background: #fff; border: 1px solid #D4DADF; }
  .blh-crumb .home { min-height: 44px; display: flex; align-items: center; }
  .blh-theme { position: absolute; right: max(20px, env(safe-area-inset-right)); top: 8px; min-height: 36px; min-width: 36px; width: 36px; height: 36px; padding: 0; }
  .blh-right:empty { display: none; }
  .blh-right { justify-content: space-between; }
  .blh-where { display: none; }
  .blh-pn { display: grid; grid-template-columns: 1fr 1fr; width: 100%; }
  .blh-pn a { max-width: none; justify-content: center; }
  .blh-pn a span { display: none; }
}
@media (prefers-reduced-motion: reduce) { .blh-top .car { transition: none; } }
@media print { .blh { display: none !important; } }
</style>"""

JS = r"""<script id="bl-header-js">
(function () {
  var h = document.querySelector('.blh'); if (!h) return;
  var burger = h.querySelector('.blh-burger');
  function closeAll(except) { Array.prototype.forEach.call(h.querySelectorAll('.blh-li.open'), function (li) { if (li !== except) { li.classList.remove('open'); var b = li.querySelector('.blh-top'); if (b) b.setAttribute('aria-expanded', 'false'); } }); }
  Array.prototype.forEach.call(h.querySelectorAll('button.blh-top'), function (b) {
    b.addEventListener('click', function () { var li = b.parentNode, open = !li.classList.contains('open'); closeAll(li); li.classList.toggle('open', open); b.setAttribute('aria-expanded', open ? 'true' : 'false'); });
  });
  if (burger) burger.addEventListener('click', function () { var open = !h.classList.contains('menu-open'); h.classList.toggle('menu-open', open); burger.setAttribute('aria-expanded', open ? 'true' : 'false'); });
  document.addEventListener('click', function (e) { if (!h.contains(e.target)) { closeAll(null); } });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { closeAll(null); if (h.classList.contains('menu-open')) { h.classList.remove('menu-open'); burger.setAttribute('aria-expanded', 'false'); burger.focus(); } } });
})();
</script>"""

def rel(frm, to):
    r = os.path.relpath(os.path.join(ROOT, to), os.path.dirname(os.path.join(ROOT, frm))).replace(os.sep, '/')
    return r

def header(page, current, where='', prev=None, nxt=None, extra=''):
    e = html.escape
    hub = rel(page, 'index.html')
    items = []
    for i, (label, url, cols) in enumerate(MENU):
        dd = ''.join(
            '<div class="blh-col">' + (f'<h6>{e(h6)}</h6>' if h6 else '<h6 aria-hidden="true"></h6>') + '<ul>' +
            ''.join(f'<li><a href="{(hub if href == "HUB" else BL + href)}">{e(t)}' + (' <span class="blh-new">New</span>' if href == 'HUB' else '') + '</a></li>' for t, href in links) +
            '</ul></div>' for h6, links in cols)
        items.append(f'<li class="blh-li{" r" if i >= 3 else ""}"><button class="blh-top" type="button" aria-expanded="false">{e(label)}<span class="car" aria-hidden="true"></span></button><div class="blh-dd">{dd}</div></li>')
        if label == 'Resources':
            items.append(f'<li><a class="blh-top is-here" href="{hub}">Free Toolkits <span class="blh-new">New</span></a></li>')
    tabs = [('Toolkits', 'index.html#toolkits', 'toolkits'), ('Widgets & embeds', 'index.html#widgets', 'widgets'), ('Journey map', 'journey.html', 'journey'), ('Team review', 'index.html#review', 'review')]
    tab_html = ''.join(f'<a href="{rel(page, f)}" data-tab="{key}"' + (' aria-current="page"' if key == current else '') + f'>{e(t)}</a>' for t, f, key in tabs)
    pn = ''
    if prev is not None or nxt is not None:
        def lk(item, label, back):
            if not item:
                return f'<a href="{hub}">' + ('← ' if back else '') + f'<b>{label}</b><span>All toolkits</span>' + ('' if back else ' →') + '</a>'
            title, f = item
            return f'<a href="{rel(page, f)}" title="{e(title)}">' + ('← ' if back else '') + f'<b>{label}</b><span>{e(title)}</span>' + ('' if back else ' →') + '</a>'
        pn = '<div class="blh-pn">' + lk(prev, 'Previous', True) + lk(nxt, 'Next', False) + '</div>'
    return ('<!-- bl-header --><header class="blh" role="banner">'
            '<div class="blh-bar"><div class="blh-in">'
            f'<a class="blh-logo" href="{BL}/" aria-label="Big Leap home"><img src="{rel(page, "assets/bigleap-logo.png")}" alt="Big Leap" width="122" height="40"></a>'
            '<button class="blh-burger" type="button" aria-expanded="false" aria-controls="blh-nav"><i aria-hidden="true"></i>Menu</button>'
            f'<nav class="blh-nav" id="blh-nav" aria-label="Big Leap"><ul>{"".join(items)}</ul>'
            f'<a class="blh-cta" href="{BL}/get-started/{UTM}">Get Your Custom Strategy</a></nav>'
            '</div></div>'
            '<div class="blh-sub"><div class="blh-in">'
            f'<div class="blh-crumb"><a class="home" href="{hub}">DIY Toolkits</a><nav class="blh-tabs" aria-label="DIY Toolkits">{tab_html}</nav></div>'
            f'<div class="blh-right">' + (f'<span class="blh-where">{e(where)}</span>' if where else '') + pn + extra + '</div>'
            '</div></div></header><!-- /bl-header -->')

def apply(page, block, before_selector=None):
    p = os.path.join(ROOT, page)
    s = open(p, encoding='utf-8').read()
    # strip old versions (this header + the earlier bl-sitenav bar)
    s = re.sub(r'<!-- bl-header -->.*?<!-- /bl-header -->\n?', '', s, flags=re.S)
    s = re.sub(r'<!-- bl-sitenav -->.*?<!-- /bl-sitenav -->\n?', '', s, flags=re.S)
    s = re.sub(r'<style id="bl-(?:sitenav|header)-css">.*?</style>\n?', '', s, flags=re.S)
    s = re.sub(r'<script id="bl-header-js">.*?</script>\n?', '', s, flags=re.S)
    fonts = rel(page, 'assets/fonts/fonts.css')
    if 'fonts.css' not in s:
        s = s.replace('</head>', f'<link rel="stylesheet" href="{fonts}">\n</head>', 1)
    s = s.replace('</head>', CSS + '\n</head>', 1)
    s = re.sub(r'(<body[^>]*>)', lambda m: m.group(1) + '\n' + block, s, count=1)
    s = s.replace('</body>', JS + '\n</body>', 1)
    open(p, 'w', encoding='utf-8').write(s)

if __name__ == '__main__':
    import sys
    only_pages = 'pages-only' in sys.argv
    d = json.load(open(os.path.join(ROOT, 'toolkits.json')))
    ORDER = ['paid', 'revops', 'seo', 'pr']           # journey order: Business Profile first
    by = {s['id']: s for s in d['series']}
    seq = [(by[sid], t) for sid in ORDER for t in by[sid]['toolkits']]
    for i, (s, t) in enumerate(seq if not only_pages else []):
        prev = seq[i - 1] if i else None
        nxt = seq[i + 1] if i + 1 < len(seq) else None
        fmt = lambda it: None if not it else ((it[1]['title'] if it[0]['id'] == s['id'] else f"{it[0]['name']}: {it[1]['title']}"), it[1]['file'])
        apply(t['file'], header(t['file'], 'toolkit', f"{s['name']} · Toolkit {t['n']} of {len(s['toolkits'])}", fmt(prev) if prev else False, fmt(nxt) if nxt else False))
        print('toolkit', t['file'])
    theme = '<button class="blh-theme" id="theme" type="button" aria-label="Switch light or dark mode" title="Light or dark mode">◐</button>'
    apply('index.html', header('index.html', 'toolkits', '', None, None, theme))
    apply('journey.html', header('journey.html', 'journey', '', None, None, ''))
    apply('mockups/toolkits-landing.html', header('mockups/toolkits-landing.html', 'landing', '', None, None, ''))
    print('index.html, journey.html')
