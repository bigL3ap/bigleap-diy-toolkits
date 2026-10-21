#!/usr/bin/env python3
"""Render 16:9 slide tiles (tiles/<id>-16x9.png) for widgets: headline + QR on the left, the live widget on the right.

Needs Python Playwright with Chromium, and segno for the QR code (pip install segno).
Run from the repo root:  python3 tools/build_tiles.py [widget-id ...]
With no ids it renders every widget in TILES below. The QR opens the full toolkit, tagged
utm_source=sales-deck&utm_medium=slide-tile&utm_campaign=tile-<id>.
"""
import base64, functools, http.server, io, json, os, socketserver, sys, threading
import segno
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://bigl3ap.github.io/bigleap-diy-toolkits/'
ACCENT = {'RevOps': '#143D55', 'Paid Media': '#EA4335', 'SEO': '#0F7B5F', 'Digital PR': '#7A4E9C', 'Email Marketing': '#B45309', 'Strategy': '#246D96'}

TILES = {  # id: (headline, subline)
    'lead-speed': ('Reply before they move on.', 'Three checks on how fast, and how reliably, every new lead hears back.'),
    'conversions-check': ('Teach your ads what a customer is.', 'Three checks that show whether Google Ads learns from results or from clicks.'),
    'campaign-pick': ('Start with the right campaign.', 'Your goal, demand and budget point to the first campaign worth running.'),
    'local-ready': ('Get found nearby.', 'Four checks that decide whether you show up when people search close by.'),
    'review-health': ('Reviews people trust.', 'Count, recency and replies: a quick read on the reviews people see first.'),
    'media-kit': ('Make it easy to quote you.', 'Four things a journalist looks for before they pick up the phone.'),
    'podcast-ready': ('Ready for the mic.', 'Three checks before you pitch yourself as a podcast guest.'),
    'email-flows': ('Emails that send themselves.', 'Find the automated emails your business is missing.'),
    'email-health': ('Keep reaching the inbox.', 'Complaints, list hygiene and results: a one-minute health check.'),
    'situation-check': ('Solve the right problem first.', 'Two questions that point to where your marketing should focus.'),
    'foundations-check': ('Fix the foundation first.', 'Four checks that show which layer everything else depends on.'),
    'referral-ready': ('Worth recommending.', 'Three habits that turn customers into reviews and referrals.'),
}

PAGE = """<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="assets/fonts/fonts.css"><style>
*{box-sizing:border-box}html,body{margin:0;width:1920px;height:1080px;overflow:hidden}
body{display:grid;grid-template-columns:1160px 760px;font-family:"Open Sans",Arial,sans-serif;color:#243642;background:#fff}
.l{position:relative;background:#EEF3F8;padding:108px 120px 90px 142px;display:flex;flex-direction:column}
.l::before{content:"";position:absolute;left:0;top:0;bottom:0;width:22px;background:{accent}}
.logo{height:60px;width:auto;align-self:flex-start}
.k{margin-top:auto;font:700 30px "Open Sans",Arial,sans-serif;color:{accent}}
h1{font:800 96px/1.02 "Raleway",Arial,sans-serif;color:#143D55;letter-spacing:-.02em;margin:18px 0 28px}
p{font:400 36px/1.4 "Open Sans",Arial,sans-serif;margin:0;max-width:760px}
.try{margin-top:auto;display:flex;align-items:center;gap:34px}
.qr{width:170px;height:170px;background:#fff;border-radius:14px;padding:10px}
.qr img{width:150px;height:150px;display:block;image-rendering:pixelated}
.try b{display:block;font:700 32px "Open Sans",Arial,sans-serif;color:#143D55}
.try span{font:400 25px "Open Sans",Arial,sans-serif;color:#5F6E79}
.r{display:flex;align-items:center;justify-content:center;background:#fff}
.frame{width:460px;height:{h}px;border:0;border-radius:14px;background:transparent;box-shadow:0 30px 70px rgba(20,61,85,.16);transform:scale({scale});transform-origin:center}
</style></head><body>
<div class="l"><img class="logo" src="assets/bigleap-logo.png" alt=""><div class="k">{service} · Free DIY toolkit</div><h1>{headline}</h1><p>{sub}</p>
<div class="try"><div class="qr">{qr}</div><div><b>Try it free</b><span>Scan, or visit bigl3ap.github.io/bigleap-diy-toolkits</span></div></div></div>
<div class="r"><iframe class="frame" src="widgets/{id}.html?theme=light" scrolling="no"></iframe></div>
</body></html>"""


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def main(ids):
    meta = {w['id']: w for w in json.load(open(os.path.join(ROOT, 'data', 'widgets.json')))['widgets']}
    httpd = socketserver.ThreadingTCPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=ROOT))
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{httpd.server_address[1]}/'
    with sync_playwright() as p:
        b = p.chromium.launch()
        for wid in ids:
            w = meta[wid]; headline, sub = TILES[wid]
            url = SITE + w['kit'] + '?utm_source=sales-deck&utm_medium=slide-tile&utm_campaign=tile-' + wid
            qr = segno.make(url, error='m'); n = qr.symbol_size(border=0)[0]
            buf = io.BytesIO(); qr.save(buf, kind='png', scale=max(1, 300 // n), border=0, dark='#143D55')
            qrtag = '<img alt="" src="data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode() + '">'
            h = w['height'] - 20; scale = min(1.45, 940 / h)
            html = (PAGE.replace('{accent}', ACCENT[w['service']]).replace('{service}', w['service']).replace('{headline}', headline)
                    .replace('{sub}', sub).replace('{qr}', qrtag).replace('{id}', wid).replace('{h}', str(h)).replace('{scale}', f'{scale:.3f}'))
            open(os.path.join(ROOT, '_tile.html'), 'w', encoding='utf-8').write(html)
            pg = b.new_page(viewport={'width': 1920, 'height': 1080})
            pg.goto(base + '_tile.html'); pg.wait_for_timeout(900)
            pg.screenshot(path=os.path.join(ROOT, 'tiles', wid + '-16x9.png'))
            pg.close(); print('tiles/' + wid + '-16x9.png')
        b.close()
    os.remove(os.path.join(ROOT, '_tile.html')); httpd.shutdown()


if __name__ == '__main__':
    main(sys.argv[1:] or list(TILES))
