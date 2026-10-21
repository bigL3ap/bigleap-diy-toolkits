#!/usr/bin/env python3
"""Render each widget as a clean 2x PNG (tiles/live/<id>.png) for the Google Slides sales deck.

The badge "Try me" shows on the first question, so the slide signals it can be clicked. In the deck,
each image links to the live widget. Run from the repo root: python3 tools/build_slide_shots.py [id ...]
"""
import functools, http.server, json, os, socketserver, sys, threading
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def main(ids):
    os.makedirs(os.path.join(ROOT, 'tiles', 'live'), exist_ok=True)
    httpd = socketserver.ThreadingTCPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=ROOT))
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{httpd.server_address[1]}/'
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 480, 'height': 900}, device_scale_factor=2, color_scheme='light', reduced_motion='reduce')
        for wid in ids:
            pg.goto(base + 'widgets/' + wid + '.html'); pg.wait_for_timeout(700)
            box = pg.locator('main.w').bounding_box()
            pg.screenshot(path=os.path.join(ROOT, 'tiles', 'live', wid + '.png'), omit_background=True,
                          clip={'x': box['x'] - 4, 'y': box['y'] - 14, 'width': box['width'] + 8, 'height': box['height'] + 20})
            print('tiles/live/' + wid + '.png', round(box['width']), round(box['height']))
        b.close()
    httpd.shutdown()


if __name__ == '__main__':
    all_ids = [w['id'] for w in json.load(open(os.path.join(ROOT, 'data', 'widgets.json')))['widgets']]
    main(sys.argv[1:] or all_ids)
