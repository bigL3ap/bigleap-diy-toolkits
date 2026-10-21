#!/usr/bin/env python3
"""Build Google Slides API requests for the sales deck from data/sales.json and data/widgets.json.

Writes three JSON files to the folder given as the first argument:
  deck_a.json  deletes the old per-widget slides and creates the opener + option slides
  deck_b.json  fills them (text, images, links)
  notes.json   {slideId: talk-track text} for the speaker notes
Send them with the Google Slides batchUpdate API (or the Google Slides connector).
No QR codes: each widget image links to the live widget, and option slides link from the service opener.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://bigl3ap.github.io/bigleap-diy-toolkits/'
COLOR = {'start': '#143D55', 'revops': '#143D55', 'paid': '#EA4335', 'seo': '#0F7B5F', 'pr': '#7A4E9C', 'email': '#B45309', 'strategy': '#246D96'}
PHOTO = {'Dallas Olsen': 'dallas-olsen', 'Scott Smoot': 'scott-smoot', 'Shemmah Al-Darweesh': 'shemmah-al-darweesh',
         'Kristina Ainge': 'kristina-ainge', 'Erica Pounder': 'erica-pounder', 'Coby Bush': 'coby-bush'}
NAVY, MUTED, TEXT, SKY, WHITE, PALE, LBLUE = '#143D55', '#5F6E79', '#243642', '#EEF3F8', '#FFFFFF', '#DCE9F2', '#8CC4E4'


def rgb(h):
    h = h.lstrip('#')
    return {'red': round(int(h[0:2], 16) / 255, 3), 'green': round(int(h[2:4], 16) / 255, 3), 'blue': round(int(h[4:6], 16) / 255, 3)}


def utf16(s):
    return len(s.encode('utf-16-le')) // 2


class Deck:
    def __init__(self):
        self.a, self.b = [], []

    def slide(self, sid, idx, bg):
        self.a.append({'createSlide': {'objectId': sid, 'insertionIndex': idx, 'slideLayoutReference': {'predefinedLayout': 'BLANK'}}})
        self.b.append({'updatePageProperties': {'objectId': sid, 'pageProperties': {'pageBackgroundFill': {'solidFill': {'color': {'rgbColor': rgb(bg)}}}}, 'fields': 'pageBackgroundFill.solidFill.color'}})

    def box(self, page, oid, x, y, w, h, shape='TEXT_BOX'):
        self.b.append({'createShape': {'objectId': oid, 'shapeType': shape, 'elementProperties': {'pageObjectId': page, 'size': {'width': {'magnitude': w, 'unit': 'PT'}, 'height': {'magnitude': h, 'unit': 'PT'}}, 'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': x, 'translateY': y, 'unit': 'PT'}}}})

    def rect(self, page, oid, x, y, w, h, fill):
        self.box(page, oid, x, y, w, h, 'RECTANGLE')
        self.b.append({'updateShapeProperties': {'objectId': oid, 'shapeProperties': {'shapeBackgroundFill': {'solidFill': {'color': {'rgbColor': rgb(fill)}}}, 'outline': {'propertyState': 'NOT_RENDERED'}}, 'fields': 'shapeBackgroundFill,outline'}})

    def text(self, page, oid, x, y, w, h, txt, size, color, bold=False, font='Open Sans', space=0, line=115, bullets=False, link=None, autofit=False):
        self.box(page, oid, x, y, w, h)
        self.b.append({'insertText': {'objectId': oid, 'text': txt}})
        st = {'fontSize': {'magnitude': size, 'unit': 'PT'}, 'foregroundColor': {'opaqueColor': {'rgbColor': rgb(color)}}, 'bold': bold, 'fontFamily': font}
        fields = 'fontSize,foregroundColor,bold,fontFamily'
        if link:
            st['link'] = link; fields += ',link'
        self.b.append({'updateTextStyle': {'objectId': oid, 'style': st, 'fields': fields, 'textRange': {'type': 'ALL'}}})
        self.b.append({'updateParagraphStyle': {'objectId': oid, 'textRange': {'type': 'ALL'}, 'style': {'spaceBelow': {'magnitude': space, 'unit': 'PT'}, 'lineSpacing': line}, 'fields': 'spaceBelow,lineSpacing'}})
        if bullets:
            self.b.append({'createParagraphBullets': {'objectId': oid, 'textRange': {'type': 'ALL'}, 'bulletPreset': 'BULLET_DISC_CIRCLE_SQUARE'}})

    def style_range(self, oid, start, end, **kw):
        st, fields = {}, []
        if 'size' in kw: st['fontSize'] = {'magnitude': kw['size'], 'unit': 'PT'}; fields.append('fontSize')
        if 'color' in kw: st['foregroundColor'] = {'opaqueColor': {'rgbColor': rgb(kw['color'])}}; fields.append('foregroundColor')
        if 'bold' in kw: st['bold'] = kw['bold']; fields.append('bold')
        if 'link' in kw: st['link'] = kw['link']; fields.append('link')
        if 'italic' in kw: st['italic'] = kw['italic']; fields.append('italic')
        self.b.append({'updateTextStyle': {'objectId': oid, 'style': st, 'fields': ','.join(fields), 'textRange': {'type': 'FIXED_RANGE', 'startIndex': start, 'endIndex': end}}})

    def image(self, page, oid, url, x, y, w, h, link=None):
        self.b.append({'createImage': {'objectId': oid, 'url': url, 'elementProperties': {'pageObjectId': page, 'size': {'width': {'magnitude': w, 'unit': 'PT'}, 'height': {'magnitude': h, 'unit': 'PT'}}, 'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': x, 'translateY': y, 'unit': 'PT'}}}})
        if link:
            self.b.append({'updateImageProperties': {'objectId': oid, 'imageProperties': {'link': {'url': link}}, 'fields': 'link'}})


def sid_for(wid):
    return 'o_' + wid.replace('-', '_')


def main(out):
    S = json.load(open(os.path.join(ROOT, 'data', 'sales.json'), encoding='utf-8'))
    W = {w['id']: w for w in json.load(open(os.path.join(ROOT, 'data', 'widgets.json'), encoding='utf-8'))['widgets']}
    people = json.load(open(os.path.join(ROOT, 'data', 'widgets.json'), encoding='utf-8'))['people']
    from PIL import Image
    d, notes = Deck(), {}
    # Remove the earlier one-image-per-widget slides.
    for wid in W:
        d.a.append({'deleteObject': {'objectId': 's_' + wid.replace('-', '_')}})
    idx = 2

    def option_slide(sid, svc_id, svc_name, owner, o, n, total, proof):
        nonlocal idx
        c = COLOR[svc_id]; w = W[o['widget']]
        live = SITE + 'widgets/' + o['widget'] + '.html?utm_source=sales-deck&utm_medium=slide&utm_campaign=deck-' + o['widget']
        d.slide(sid, idx, WHITE); idx += 1
        d.rect(sid, sid + '_bar', 0, 0, 720, 6, c)
        d.rect(sid, sid + '_bg', 418, 6, 302, 399, SKY)
        tag = (svc_name.upper() + (' · OPTION %d OF %d' % (n, total) if total > 1 else ''))
        d.text(sid, sid + '_k', 34, 26, 370, 18, tag, 9.5, c, bold=True)
        d.text(sid, sid + '_h', 34, 44, 370, 66, o['headline'], 25, NAVY, bold=True, font='Raleway', line=100)
        q = 'Live widget: ' + w['title']
        d.text(sid, sid + '_q', 34, 110, 370, 18, q, 11, MUTED)
        d.style_range(sid + '_q', 0, utf16('Live widget:'), bold=True)
        d.text(sid, sid + '_l', 34, 136, 370, 16, 'WHY IT MATTERS', 9, MUTED, bold=True)
        d.text(sid, sid + '_b', 34, 152, 370, 118, '\n'.join(o['points']), 12, TEXT, space=5, bullets=True)
        if proof:
            src = 'Source: ' + proof['source']
            t = proof['text'] + '\n' + src
            d.rect(sid, sid + '_pb', 34, 274, 370, 82, SKY)
            d.text(sid, sid + '_p', 40, 278, 360, 76, t, 10.5, NAVY, space=2)
            a = utf16(proof['text']) + 1
            d.style_range(sid + '_p', a, a + utf16(src), size=8.5, color=MUTED, link={'url': proof['url']})
        d.text(sid, sid + '_o', 34, 366, 370, 18, 'Expert: ' + owner + (', ' + people.get(owner, {}).get('title', '') if people.get(owner, {}).get('title') else ''), 9.5, MUTED)
        # Widget image, fitted into the right panel.
        im = Image.open(os.path.join(ROOT, 'tiles', 'live', o['widget'] + '.png'))
        maxh, maxw = 338, 280
        h = maxh; wpt = h * im.size[0] / im.size[1]
        if wpt > maxw: wpt = maxw; h = wpt * im.size[1] / im.size[0]
        x = 418 + (302 - wpt) / 2
        d.image(sid, sid + '_img', SITE + 'tiles/live/' + o['widget'] + '.png', round(x, 1), 18, round(wpt, 1), round(h, 1), live)
        d.text(sid, sid + '_c', 418, 18 + h + 6, 302, 18, 'Click the widget to try it live  ↗', 10.5, '#C5372B', bold=True, link={'url': live})
        d.b.append({'updateParagraphStyle': {'objectId': sid + '_c', 'textRange': {'type': 'ALL'}, 'style': {'alignment': 'CENTER'}, 'fields': 'alignment'}})
        notes[sid] = ('ASK: ' + o['ask'] + '\n\nLISTEN FOR: ' + o['listen'] + '\n\nNEXT STEP: ' + o['next'] +
                      '\n\nUSE IT FOR: ' + w['use'] +
                      ('\n\nPROOF: ' + proof['text'] + ' (' + proof['source'] + ')' if proof else '') +
                      '\n\nLive widget: ' + live + '\nFull toolkit: ' + SITE + w['kit'])

    st = S['start']
    option_slide(sid_for(st['widget']), 'start', 'Start here', 'Scott Smoot', st, 1, 1, None)
    for s in S['services']:
        sv = 'sv_' + s['id']; c = COLOR[s['id']]
        d.slide(sv, idx, NAVY); idx += 1
        d.rect(sv, sv + '_bar', 0, 0, 10, 405, LBLUE if c == NAVY else c)
        photo = PHOTO.get(s['owner'])
        d.text(sv, sv + '_e', 44, 30, 520, 16, 'EXPERT: ' + s['owner'].upper() + (' · ' + people[s['owner']]['title'].upper() if people.get(s['owner'], {}).get('title') else ''), 9.5, LBLUE, bold=True)
        d.text(sv, sv + '_t', 44, 46, 520, 44, s['name'], 34, WHITE, bold=True, font='Raleway')
        if photo:
            d.image(sv, sv + '_ph', SITE + 'assets/people/' + photo + '.png', 610, 28, 72, 72)
        d.text(sv, sv + '_s', 44, 96, 560, 48, s['story'], 15, PALE, line=110)
        d.text(sv, sv + '_vh', 44, 152, 300, 16, 'WHAT BIG LEAP DOES', 9, LBLUE, bold=True)
        d.text(sv, sv + '_v', 44, 170, 300, 130, '\n'.join(s['value']), 11.5, WHITE, space=6, bullets=True)
        if s['proof']:
            d.text(sv, sv + '_ph2', 372, 152, 310, 16, 'PROOF POINTS', 9, LBLUE, bold=True)
            parts, ranges, pos = [], [], 0
            for p in s['proof']:
                line1, line2 = p['text'], 'Source: ' + p['source']
                parts += [line1, line2]
                ranges.append((pos + utf16(line1) + 1, pos + utf16(line1) + 1 + utf16(line2), p['url']))
                pos += utf16(line1) + 1 + utf16(line2) + 1
            d.text(sv, sv + '_pp', 372, 170, 310, 140, '\n'.join(parts), 10, WHITE, space=3)
            for a, b, u in ranges:
                d.style_range(sv + '_pp', a, b, size=8, color=LBLUE, link={'url': u})
        # Option picker: each line links to its slide.
        lines = ['Option %d: %s' % (i + 1, o['headline']) for i, o in enumerate(s['options'])]
        d.text(sv, sv + '_oh', 44, 312, 600, 16, 'PICK AN OPTION', 9, LBLUE, bold=True)
        d.text(sv, sv + '_op', 44, 328, 640, 60, '\n'.join(lines), 11.5, WHITE, bold=True, space=2)
        pos = 0
        for i, o in enumerate(s['options']):
            d.style_range(sv + '_op', pos, pos + utf16(lines[i]), link={'pageObjectId': sid_for(o['widget'])})
            pos += utf16(lines[i]) + 1
        notes[sv] = (s['name'] + ' in one line: ' + s['story'] + '\n\nPick the option that fits the client:\n' +
                     '\n'.join('- %s (%s): %s' % (o['headline'], W[o['widget']]['title'], W[o['widget']]['use']) for o in s['options']) +
                     '\n\nProof sources:\n' + '\n'.join('- %s: %s' % (p['source'], p['url']) for p in s['proof']))
        for i, o in enumerate(s['options']):
            option_slide(sid_for(o['widget']), s['id'], s['name'], s['owner'], o, i + 1, len(s['options']), s['proof'][o.get('proof', i % len(s['proof']))] if s['proof'] else None)
    os.makedirs(out, exist_ok=True)
    json.dump(d.a, open(os.path.join(out, 'deck_a.json'), 'w'))
    json.dump(d.b, open(os.path.join(out, 'deck_b.json'), 'w'))
    json.dump(notes, open(os.path.join(out, 'notes.json'), 'w'), indent=1)
    print(len(d.a), 'structure requests,', len(d.b), 'content requests,', len(notes), 'notes')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'build', 'deck'))
