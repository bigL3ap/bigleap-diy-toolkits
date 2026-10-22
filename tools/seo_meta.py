#!/usr/bin/env python3
"""SEO/AEO metadata for every public DIY Toolkits page: canonical link, robots, Open Graph,
Twitter card and schema.org JSON-LD (BreadcrumbList + WebApplication for toolkits;
Organization/WebSite for the home page; CollectionPage/ItemList for the catalog).

Public pages (made indexable): index.html, toolkits.html, my-profile.html, your-journey.html,
roadmap.html, and every toolkit under toolkits/*. Internal pages (journey, sales, widgets,
review, mockups/*, and every widgets/*.html fragment) are left untouched — they keep
<meta name="robots" content="noindex, nofollow"> and get no schema, since they are not
meant to be found in search or cited by an AI answer on their own.

Titles and descriptions for toolkit pages come from toolkits.json (the same copy already
shown in the catalog), so there is one source of truth; this script does not invent new
marketing copy, only the structured-data and tag plumbing around it.

Idempotent: re-running replaces everything between <!-- bl-seo --> and <!-- /bl-seo -->, and
replaces the existing <title>, <meta name="description"> and <meta name="robots"> in place.
Run from the repo root after any change to toolkits.json, or after adding/removing a public
page:  python3 tools/seo_meta.py
It also regenerates sitemap.xml, robots.txt and llms.txt from the same page list.
"""
import json, os, re
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://bigl3ap.github.io/bigleap-diy-toolkits/'
ORG = {'@type': 'Organization', 'name': 'Big Leap', 'url': 'https://www.bigleap.com', 'logo': SITE + 'assets/bigleap-logo.png'}
OG_IMAGE = SITE + 'assets/bigleap-logo.png'
TODAY = date.today().isoformat()

# Internal pages: never touched by this script. Kept here only so a reviewer can see the
# deliberate split between what's public and what stays hidden.
INTERNAL_PAGES = {'journey.html', 'sales.html', 'widgets.html', 'review.html',
                   'mockups/homepage.html', 'mockups/toolkits-landing.html'}

HUB_PAGES = [
    {'path': 'index.html', 'title': 'Free DIY Marketing Toolkits · Big Leap',
     'description': 'Free DIY marketing toolkits from Big Leap: build your profile, follow your path, keep every answer, roadmap and plan in one place.',
     'kind': 'home'},
    {'path': 'toolkits.html', 'title': 'All Toolkits · Free DIY Marketing Toolkits · Big Leap',
     'description': 'Free, self-serve toolkits from Big Leap. Set up the foundations yourself and save your budget for strategy.',
     'kind': 'catalog'},
    {'path': 'my-profile.html', 'title': 'My Profile · Big Leap DIY Toolkits',
     'description': 'Your Business Profile and every answer you have given the Big Leap DIY toolkits, in one place. Stored only in your browser.',
     'kind': 'page'},
    {'path': 'your-journey.html', 'title': 'Your Journey · Big Leap DIY Toolkits',
     'description': 'Your path through the free Big Leap DIY toolkits: where you are, what you have done, what comes next, and when to bring in an expert.',
     'kind': 'page'},
    {'path': 'roadmap.html', 'title': 'Your Marketing Roadmap · Big Leap DIY Toolkits',
     'description': 'Your top three marketing priorities, built from your Business Profile, strategy starters and toolkit progress, with the free toolkit for each.',
     'kind': 'page'},
]


def esc(s):
    return (s or '').replace('\\', '\\\\').replace('"', '\\"')


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + '</script>'


def breadcrumb(items):
    # items: list of (name, url-or-None-for-last)
    els = []
    for i, (name, url) in enumerate(items, 1):
        e = {'@type': 'ListItem', 'position': i, 'name': name}
        if url:
            e['item'] = url
        els.append(e)
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': els}


def toolkit_schema(title, description, url):
    return {
        '@context': 'https://schema.org', '@type': 'WebApplication', 'name': title,
        'description': description, 'url': url, 'applicationCategory': 'BusinessApplication',
        'operatingSystem': 'Any web browser', 'isAccessibleForFree': True,
        'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'USD'}, 'provider': ORG,
    }


def seo_block(canonical, title, description, ld_list):
    parts = ['<!-- bl-seo -->', '<link rel="canonical" href="' + canonical + '">',
             '<meta property="og:type" content="website">',
             '<meta property="og:site_name" content="Big Leap DIY Toolkits">',
             '<meta property="og:title" content="' + esc(title) + '">',
             '<meta property="og:description" content="' + esc(description) + '">',
             '<meta property="og:url" content="' + canonical + '">',
             '<meta property="og:image" content="' + OG_IMAGE + '">',
             '<meta name="twitter:card" content="summary">',
             '<meta name="twitter:title" content="' + esc(title) + '">',
             '<meta name="twitter:description" content="' + esc(description) + '">',
             '<meta name="twitter:image" content="' + OG_IMAGE + '">']
    parts += [jsonld(ld) for ld in ld_list]
    parts.append('<!-- /bl-seo -->')
    return '\n'.join(parts)


def apply_head(text, path, title, description, ld_list):
    canonical = SITE + path
    # title
    text, n = re.subn(r'<title>.*?</title>', '<title>' + title.replace('&', '&amp;') + '</title>', text, count=1)
    assert n == 1, 'no <title> in ' + path
    # description
    text, n = re.subn(r'<meta name="description" content="[^"]*">',
                       '<meta name="description" content="' + description.replace('"', '&quot;') + '">', text, count=1)
    assert n == 1, 'no description meta in ' + path
    # robots: replace if present, else insert right after description
    if re.search(r'<meta name="robots"[^>]*>', text):
        text, n = re.subn(r'<meta name="robots" content="[^"]*">', '<meta name="robots" content="index, follow">', text, count=1)
    else:
        text, n = re.subn(r'(<meta name="description" content="[^"]*">)',
                           r'\1\n<meta name="robots" content="index, follow">', text, count=1)
    assert n == 1, 'robots meta step failed in ' + path
    block = seo_block(canonical, title, description, ld_list)
    if '<!-- bl-seo -->' in text:
        text = re.sub(r'<!-- bl-seo -->.*?<!-- /bl-seo -->', block, text, count=1, flags=re.S)
    else:
        text = re.sub(r'(<meta name="robots" content="[^"]*">)', r'\1\n' + block, text, count=1)
    return text


def main():
    tj = json.load(open(os.path.join(ROOT, 'toolkits.json')))
    public_urls = []

    # The universal Business Profile builder (toolkits.json "start"): linked from every
    # page and every toolkit, but not part of any one service's list, so it needs its own entry.
    start = tj['start']
    p = os.path.join(ROOT, start['file'])
    text = open(p, encoding='utf-8').read()
    start_title_tag = re.search(r'<title>(.*?)</title>', text).group(1)
    title = start_title_tag + ' · Big Leap'
    description = re.search(r'<meta name="description" content="([^"]*)">', text).group(1)
    url = SITE + start['file']
    ld = [toolkit_schema(start_title_tag, description, url), breadcrumb([('Home', SITE), (start_title_tag, None)])]
    new_text = apply_head(text, start['file'], title, description, ld)
    if new_text != text:
        open(p, 'w', encoding='utf-8').write(new_text)
    public_urls.append((start['file'], 0.9))

    # Hub pages
    for hp in HUB_PAGES:
        p = os.path.join(ROOT, hp['path'])
        text = open(p, encoding='utf-8').read()
        url = SITE + hp['path']
        if hp['kind'] == 'home':
            faq = []
            for qm in re.finditer(r'<details[^>]*><summary>(.*?)</summary><p>(.*?)</p></details>', text, re.S):
                faq.append({'@type': 'Question', 'name': qm.group(1).strip(),
                            'acceptedAnswer': {'@type': 'Answer', 'text': qm.group(2).strip()}})
            ld = [ORG, {'@context': 'https://schema.org', '@type': 'WebSite', 'name': 'Big Leap DIY Toolkits',
                        'url': SITE, 'publisher': ORG}]
            if faq:
                ld.append({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': faq})
        elif hp['kind'] == 'catalog':
            items = []
            for s in tj['series']:
                for t in s['toolkits']:
                    items.append({'@type': 'ListItem', 'position': len(items) + 1, 'name': t['title'],
                                   'url': SITE + t['file']})
            ld = [{'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': hp['title'],
                   'url': url, 'hasPart': {'@type': 'ItemList', 'itemListElement': items}},
                  breadcrumb([('Home', SITE), ('All toolkits', None)])]
        else:
            ld = [breadcrumb([('Home', SITE), (hp['title'].split(' · ')[0], None)])]
        new_text = apply_head(text, hp['path'], hp['title'], hp['description'], ld)
        if new_text != text:
            open(p, 'w', encoding='utf-8').write(new_text)
        public_urls.append((hp['path'], 0.9 if hp['kind'] in ('home', 'catalog') else 0.5))

    # Toolkit pages
    for s in tj['series']:
        for t in s['toolkits']:
            path = t['file']
            p = os.path.join(ROOT, path)
            text = open(p, encoding='utf-8').read()
            title = t['title'] + ' · Big Leap'
            description = t['description']
            url = SITE + path
            ld = [toolkit_schema(t['title'], description, url),
                  breadcrumb([('Home', SITE), ('All toolkits', SITE + 'toolkits.html'), (s['name'], SITE + 'toolkits.html#' + s['id']), (t['title'], None)])]
            new_text = apply_head(text, path, title, description, ld)
            if new_text != text:
                open(p, 'w', encoding='utf-8').write(new_text)
            public_urls.append((path, 0.8))

    # sitemap.xml
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, priority in public_urls:
        lines.append('  <url><loc>' + SITE + path + '</loc><lastmod>' + TODAY + '</lastmod><priority>' + str(priority) + '</priority></url>')
    lines.append('</urlset>')
    open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')

    # robots.txt
    robots = [
        'User-agent: *', 'Allow: /',
        'Disallow: /sales.html', 'Disallow: /widgets.html', 'Disallow: /journey.html',
        'Disallow: /review.html', 'Disallow: /mockups/', 'Disallow: /widgets/', 'Disallow: /tools/',
        '', 'Sitemap: ' + SITE + 'sitemap.xml',
    ]
    open(os.path.join(ROOT, 'robots.txt'), 'w', encoding='utf-8').write('\n'.join(robots) + '\n')

    # llms.txt
    llm_lines = [
        '# Big Leap DIY Toolkits', '',
        '> Free, self-serve marketing toolkits from Big Leap (bigleap.com). Each toolkit asks a few',
        '> quick questions about one specific marketing problem and returns a plan built from the',
        '> answers, not a generic article. Nothing a visitor enters is stored on a server; it stays',
        '> in their own browser. The toolkits are free; Big Leap also offers full-service management',
        '> of RevOps, Paid Media, SEO, Digital PR, Email Marketing and Strategy for businesses that',
        '> want an expert to do the work instead.', '',
        '## Start here', '',
        '- [All toolkits](' + SITE + 'toolkits.html): the full catalog, organized by service.',
        '- [Free DIY Marketing Toolkits](' + SITE + 'index.html): how the toolkits work and which to start with.',
        '- [' + tj['start']['title'] + '](' + SITE + tj['start']['file'] + '): ' + tj['start']['description'],
        '',
    ]
    for s in tj['series']:
        llm_lines.append('## ' + s['name'])
        llm_lines.append('')
        for t in s['toolkits']:
            llm_lines.append('- [' + t['title'] + '](' + SITE + t['file'] + '): ' + t['description'])
        llm_lines.append('')
    llm_lines.append('## Notes for AI assistants and crawlers')
    llm_lines.append('')
    llm_lines.append('- Each toolkit page states its own assumptions and labels any rule-of-thumb estimate as Big Leap\'s own, not an external fact.')
    llm_lines.append('- Visitor answers are never sent to or stored on a server. There is no login and no tracking of individual answers.')
    llm_lines.append('- Pages under /widgets/, /sales.html, /widgets.html, /journey.html, /review.html and /mockups/ are internal tools and previews, not standalone content, and are excluded from crawling.')
    open(os.path.join(ROOT, 'llms.txt'), 'w', encoding='utf-8').write('\n'.join(llm_lines) + '\n')

    print('Updated', len(public_urls), 'public pages; wrote sitemap.xml, robots.txt, llms.txt')


if __name__ == '__main__':
    main()
