#!/usr/bin/env python3
"""Big Leap site header for every DIY Toolkits page.

Tier 1 copies the bigleap.com header (logo, Services / Who We Serve / Case Studies / Resources / About menus,
"Get Your Custom Strategy"), with links to the live site, so the toolkits read as part of bigleap.com.
Tier 2 is the toolkit bar. Client-facing pages sit on the left (Toolkits menu · Start here · Roadmap); internal pages
sit on the right under "Internal" (Journey map · Sales assets · Widgets · Mockups · Status & review),
plus Previous / Next on public toolkit pages. Preview pages (toolkits.json "previews") and review.html get the
header but are never added to the Previous / Next sequence.

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
/* Tier 2: one flat toolkit bar */
.blh-sub { background: #EEF3F8; border-bottom: 1px solid #D4DADF; }
.blh-sub .blh-in { display: flex; align-items: center; gap: 12px; min-height: 52px; }
.blh-tabs { flex: 1 1 auto; min-width: 0; display: flex; align-items: center; gap: 2px; overflow-x: auto; scrollbar-width: none; -webkit-overflow-scrolling: touch; padding: 6px 0; }
.blh-tabs::-webkit-scrollbar { display: none; }
.blh-label { flex: 0 0 auto; font: 800 15px "Raleway", "Segoe UI", Arial, sans-serif; color: #143D55; margin-right: 10px; white-space: nowrap; }
.blh-tabs a { flex: 0 0 auto; display: inline-flex; align-items: center; min-height: 40px; padding: 6px 12px; border-radius: 999px; font: 600 14px "Open Sans", Arial, sans-serif; color: #143D55; text-decoration: none; white-space: nowrap; }
.blh-tabs a:hover { background: #DAE9F2; }
.blh-tabs a[aria-current="page"], .blh-tabs a[aria-current="true"] { background: #143D55; color: #fff; }
.blh-div { flex: 0 0 auto; width: 1px; height: 22px; background: #B9C6CF; margin: 0 8px; }
.blh-int { flex: 0 0 auto; margin-left: auto; display: flex; align-items: center; gap: 2px; padding-left: 12px; border-left: 1px solid #B9C6CF; }
.blh-int-l { flex: 0 0 auto; font: 800 11px/1 "Open Sans", Arial, sans-serif; letter-spacing: .08em; text-transform: uppercase; color: #5F6E79; margin-right: 6px; white-space: nowrap; }
.blh-int a { font-weight: 600; color: #3D5566; }
:root[data-theme="dark"] .blh-int { border-left-color: #2D4556; } :root[data-theme="dark"] .blh-int-l, :root[data-theme="dark"] .blh-int a:not([aria-current]) { color: #9AAFBD; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) .blh-int { border-left-color: #2D4556; } :root:not([data-theme="light"]) .blh-int-l, :root:not([data-theme="light"]) .blh-int a:not([aria-current]) { color: #9AAFBD; } }
.blh-sub .blh-in { position: relative; }
.blh-tbtn { flex: 0 0 auto; display: inline-flex; align-items: center; gap: 8px; min-height: 40px; padding: 6px 14px; border: 0; border-radius: 999px; background: transparent; font: 600 14px "Open Sans", Arial, sans-serif; color: #143D55; cursor: pointer; white-space: nowrap; }
.blh-tbtn:hover, .blh-tbtn[aria-expanded="true"] { background: #DAE9F2; }
.blh-tbtn.is-current { background: #143D55; color: #fff; }
.blh-tbtn .car { width: 7px; height: 7px; border-right: 2px solid currentColor; border-bottom: 2px solid currentColor; transform: rotate(45deg); margin-top: -4px; transition: transform .15s ease; }
.blh-tbtn[aria-expanded="true"] .car { transform: rotate(-135deg); margin-top: 3px; }
.blh-tbtn:focus-visible, .blh-tmenu a:focus-visible { outline: 3px solid #3187B5; outline-offset: 2px; }
.blh-tmenu { position: absolute; top: calc(100% - 4px); z-index: 60; min-width: 220px; background: #fff; border: 1px solid #D4DADF; border-radius: 12px; box-shadow: 0 18px 40px rgba(20,61,85,.16); padding: 8px; }
.blh-tmenu[hidden] { display: none; }
.blh-tmenu ul { list-style: none; margin: 0; padding: 0; display: grid; gap: 2px; }
.blh-tmenu li:first-child { border-bottom: 1px solid #EEF3F8; padding-bottom: 4px; margin-bottom: 2px; }
.blh-tmenu a { display: flex; align-items: center; min-height: 40px; padding: 6px 12px; border-radius: 8px; font: 600 14.5px "Open Sans", Arial, sans-serif; color: #143D55; text-decoration: none; white-space: nowrap; }
.blh-tmenu a:hover { background: #EEF3F8; color: #246D96; }
.blh-tmenu a[aria-current="page"], .blh-tmenu a[aria-current="true"] { background: #143D55; color: #fff; }
.blh-right { flex: 0 0 auto; display: flex; align-items: center; gap: 8px; }
.blh-theme { display: inline-grid; place-items: center; min-height: 40px; min-width: 40px; border: 1px solid #D4DADF; border-radius: 999px; background: #fff; color: #143D55; cursor: pointer; font-size: 16px; }
/* Bottom pager on toolkit pages */
.blp { background: #EEF3F8; border-top: 1px solid #D4DADF; margin-top: 16px; font-family: "Open Sans", "Segoe UI", Arial, sans-serif; }
.blp-in { max-width: 1240px; margin: 0 auto; padding: 18px max(20px, env(safe-area-inset-left)) calc(18px + env(safe-area-inset-bottom)) max(20px, env(safe-area-inset-right)); display: grid; grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr); gap: 12px; align-items: stretch; }
.blp a { display: flex; flex-direction: column; justify-content: center; gap: 2px; min-height: 64px; padding: 10px 16px; border: 1px solid #D4DADF; border-radius: 12px; background: #fff; color: #143D55; text-decoration: none; }
.blp a:hover { border-color: #3187B5; }
.blp a:focus-visible { outline: 3px solid #3187B5; outline-offset: 2px; }
.blp small { font-size: 12.5px; color: #5F6E79; font-weight: 600; }
.blp b { font: 700 15px/1.3 "Raleway", "Segoe UI", Arial, sans-serif; }
.blp-a:not(.back) { text-align: right; align-items: flex-end; }
.blp-hub { text-align: center; align-items: center; }
@media (max-width: 640px) { .blp-in { grid-template-columns: 1fr 1fr; } .blp-hub { grid-column: 1 / -1; order: 3; } }
@media print { .blp { display: none !important; } }
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
  .blh-sub .blh-in { gap: 6px; }
  .blh-label { display: none; }
  .blh-tabs { -webkit-mask-image: linear-gradient(90deg, #000 88%, transparent); mask-image: linear-gradient(90deg, #000 88%, transparent); padding-right: 24px; }
}
@media (prefers-reduced-motion: reduce) { .blh-top .car, .blh-tbtn .car { transition: none; } }
.blx-swipe { margin: 6px 0 4px; font: 600 12.5px/1.3 'Open Sans', Arial, sans-serif; color: #5B6B76; text-align: right; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) .blx-swipe { color: #9FB3C1; } }
:root[data-theme="dark"] .blx-swipe { color: #9FB3C1; }

/* ---- Shared toolkit polish (consistent controls across all toolkits) ---- */
.q-row .seg.inline { display: grid; width: 100%; flex: 1 1 100%; }
.seg.inline label { min-width: 0; padding-inline: 12px; }
@media (max-width: 560px) { .q-row .seg.inline { width: 100%; } .q-row .q-sub { flex-basis: 100%; } }
.st-top { display: grid !important; grid-template-columns: minmax(0, 1fr) auto; align-items: start; gap: 4px 12px; }
.st-top .chip-row { justify-self: end; display: flex; flex-wrap: wrap; gap: 4px; justify-content: flex-end; }
@media (max-width: 560px) { .st-top { grid-template-columns: minmax(0, 1fr); } .st-top .chip-row { justify-self: start; justify-content: flex-start; } }
@media (max-width: 420px) { .meta-grid { grid-template-columns: max-content minmax(0, 1fr) !important; } .meta-grid dd { margin-bottom: 0 !important; } }
.draft-banner .nw, .draft-banner b { white-space: nowrap; }
.blx-rel > summary { cursor: pointer; font-size: 12.5px; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; list-style: none; padding: 4px 0; }
.blx-rel > summary::-webkit-details-marker { display: none; }
.blx-rel > summary::before { content: "+ "; } .blx-rel[open] > summary::before { content: "− "; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) .blh-sub { background: #0F1D26; border-bottom-color: #22394A; } :root:not([data-theme="light"]) .blh-tabs a, :root:not([data-theme="light"]) .blh-tbtn { color: #DCE9F2; } :root:not([data-theme="light"]) .blh-tbtn:hover, :root:not([data-theme="light"]) .blh-tbtn[aria-expanded="true"] { background: #1D3A4C; } :root:not([data-theme="light"]) .blh-tbtn.is-current { background: #DCE9F2; color: #0F1D26; } :root:not([data-theme="light"]) .blh-tmenu { background: #142632; border-color: #2D4556; } :root:not([data-theme="light"]) .blh-tmenu a { color: #DCE9F2; } :root:not([data-theme="light"]) .blh-tmenu a:hover { background: #1D3A4C; color: #fff; } :root:not([data-theme="light"]) .blh-tmenu li:first-child { border-bottom-color: #2D4556; } :root:not([data-theme="light"]) .blh-label { color: #fff; } :root:not([data-theme="light"]) .blp { background: #0F1D26; border-top-color: #22394A; } }
:root[data-theme="dark"] .blh-sub { background: #0F1D26; border-bottom-color: #22394A; } :root[data-theme="dark"] .blh-tabs a, :root[data-theme="dark"] .blh-tbtn { color: #DCE9F2; } :root[data-theme="dark"] .blh-tbtn:hover, :root[data-theme="dark"] .blh-tbtn[aria-expanded="true"] { background: #1D3A4C; } :root[data-theme="dark"] .blh-tbtn.is-current { background: #DCE9F2; color: #0F1D26; } :root[data-theme="dark"] .blh-tmenu { background: #142632; border-color: #2D4556; } :root[data-theme="dark"] .blh-tmenu a { color: #DCE9F2; } :root[data-theme="dark"] .blh-tmenu a:hover { background: #1D3A4C; color: #fff; } :root[data-theme="dark"] .blh-tmenu li:first-child { border-bottom-color: #2D4556; } :root[data-theme="dark"] .blh-label { color: #fff; } :root[data-theme="dark"] .blp { background: #0F1D26; border-top-color: #22394A; }

/* ---- Toolkit layout: questions on top (full width), results below ---- */
@media (min-width: 880px) {
  .layout { grid-template-columns: minmax(0, 1fr) !important; grid-template-areas: "q" "r" "d" !important; grid-template-rows: auto !important; row-gap: 22px; }
  .col-q.is-sticky, .results.is-sticky { position: static !important; }
  .results { grid-template-columns: minmax(0, 1fr); }
}
.col-q { scroll-margin-top: 16px; } #results, #answer { scroll-margin-top: 16px; }
/* Live result bar: shows the headline while the results are off screen */
.blx-bar { position: fixed; left: 50%; bottom: max(14px, env(safe-area-inset-bottom)); transform: translate(-50%, 140%); z-index: 60; display: flex; align-items: center; gap: 14px; width: min(760px, calc(100% - 24px)); padding: 10px 10px 10px 18px; border-radius: 16px; background: #143D55; color: #fff; box-shadow: 0 10px 30px rgba(20,61,85,.35); transition: transform .25s ease; font-family: "Open Sans", "Segoe UI", Arial, sans-serif; }
.blx-bar.show { transform: translate(-50%, 0); }
.blx-bar .t { flex: 1 1 auto; min-width: 0; font-size: 14px; line-height: 1.3; }
.blx-bar .t small { display: block; font-size: 11.5px; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; color: #9FC4DC; }
.blx-bar .t b { display: block; font-size: 15.5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.blx-bar button { flex: 0 0 auto; min-height: 44px; padding: 10px 16px; border: 0; border-radius: 12px; background: #EA4335; color: #fff; font: 700 14.5px "Open Sans", Arial, sans-serif; cursor: pointer; }
.blx-bar button:hover { background: #C5372B; }
@media (prefers-reduced-motion: reduce) { .blx-bar { transition: none; } }
@media print { .blx-bar { display: none !important; } }

/* ---- Toolkit form: one panel, one question per row (question left, answers right) ---- */
.col-q.panel { padding: 0 !important; overflow: hidden; }
.col-q .q-head { padding: 20px 28px 16px !important; border-bottom: 1px solid var(--line); }
#answers .q { margin: 0 !important; padding: 22px 28px !important; border: 0 !important; border-top: 1px solid var(--line) !important; }
#answers > .q-head + .q, #answers > .q:first-child, #answers > .q-head + div > .q:first-child { border-top: 0 !important; }
#answers > div:not(.q):not(.q-head) > .q:first-child { border-top: 1px solid var(--line) !important; }
.q legend { float: left !important; width: 100%; margin: 0 0 8px !important; }
.q > legend + * { clear: both; }
.q-label { font-size: 15.5px; }
.q-help { line-height: 1.5; }
/* AA contrast for small text in light mode (dark mode already passes): the red eyebrow, and muted text on the light-blue "do first" row */
@media (prefers-color-scheme: light) { :root:not([data-theme="dark"]) .eyebrow .kit { color: #C5372B; } :root:not([data-theme="dark"]) .steps > li.is-first .st-time, :root:not([data-theme="dark"]) .steps > li.is-first .kit-link, :root:not([data-theme="dark"]) .steps > li.is-first .path-owner { color: #46535D; } }
:root[data-theme="light"] .eyebrow .kit { color: #C5372B; } :root[data-theme="light"] .steps > li.is-first .st-time, :root[data-theme="light"] .steps > li.is-first .kit-link, :root[data-theme="light"] .steps > li.is-first .path-owner { color: #46535D; }
#answers .q[hidden], #answers [hidden] { display: none !important; }
@media (min-width: 880px) {
  #answers .q.blx-split:not([hidden]) { display: flow-root !important; }
  .q.blx-split > legend, .q.blx-split > .q-label { float: left !important; clear: left; width: calc(41.67% - 22px) !important; margin: 2px 0 0 !important; padding: 0 !important; }
  .q.blx-split > .blx-qh { float: left; clear: left; width: calc(41.67% - 22px); display: grid; gap: 6px; padding-top: 6px; }
  .q.blx-split > .blx-qh:empty { display: none; }
  .q.blx-split > .blx-qh .q-help { margin: 0; }
  .q.blx-split > .blx-qc { margin-left: calc(41.67% + 22px); display: grid; gap: 10px; min-width: 0; }
  #answers .q.blx-pairs > .blx-pair { margin-top: 14px; }
  #answers .q.blx-pairs > .blx-pair { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 7fr); column-gap: 44px; align-items: start; }
  #answers .q.blx-pairs > .blx-pair + .blx-pair { margin-top: 14px; }
  #answers .q.blx-pairs .blx-ph > * { margin: 8px 0 0 !important; display: block; }
  #answers .q.blx-pairs .blx-pc { display: grid; gap: 10px; min-width: 0; }
  #answers .q.blx-pairs > .blx-pairhelp { max-width: calc(41.67% - 22px); margin-top: 8px; }
  #answers .q.blx-row > .q-row { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 7fr); column-gap: 44px; align-items: center; }
  #answers .q.blx-row > .q-row > :first-child { min-width: 0; }
  #answers .q.blx-row > .q-row > :not(:first-child) { justify-self: start; }
  #answers .q.blx-row > .q-row + .q-row { margin-top: 10px; }
  #answers .q.blx-row > .sub-q { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 7fr); column-gap: 44px; row-gap: 6px; align-items: center; margin-top: 16px; padding: 0; border: 0; }
  #answers .q.blx-row > .sub-q > .q-label { grid-column: 1; grid-row: 1; }
  #answers .q.blx-row > .sub-q > :not(.q-label):not(.q-help) { grid-column: 2; grid-row: 1; }
  #answers .q.blx-row > .sub-q > .q-help { grid-column: 1; grid-row: 2; margin: 0; }
  #answers .q.blx-row > .q-help { max-width: calc(41.6% - 22px); margin-top: 6px; }
  #answers .q.blx-row .seg.inline { width: 100%; max-width: 420px; }
  .blx-qc .seg:not(.inline) { max-width: 600px; }
}
#answers .q { scroll-margin-top: 16px; }
.blx-pair + .blx-pair { margin-top: 12px; } .blx-pc { display: grid; gap: 8px; } .blx-ph > * { margin-bottom: 6px; }
/* answer controls: lighter */
.seg { gap: 6px !important; border: 0 !important; background: transparent !important; overflow: visible !important; border-radius: 0 !important; }
.seg label { min-height: 42px !important; border: 1px solid var(--line-strong) !important; border-radius: 10px !important; background: var(--field, #fff) !important; font-weight: 600 !important; color: var(--text) !important; transition: background-color .12s ease, border-color .12s ease; }
.seg label:hover { background: var(--hover) !important; }
.seg input:checked + label { background: var(--seg-on) !important; border-color: var(--seg-on) !important; color: var(--on-seg) !important; font-weight: 700 !important; }
.seg input:focus-visible + label { outline: 2px solid var(--focus); outline-offset: 2px; }
.seg.is-focus { outline: 0 !important; }
.opt, .opt-wrap, .text-field, .field { border-radius: 10px !important; }
/* compact floating result card */
.blx-bar { left: auto !important; right: max(16px, env(safe-area-inset-right)); width: min(400px, calc(100% - 32px)) !important; transform: translateY(160%) !important; padding: 10px 10px 10px 16px !important; gap: 12px !important; border-radius: 14px !important; }
.blx-bar.show { transform: translateY(0) !important; }
.blx-bar .t b { font-size: 14.5px !important; white-space: normal !important; display: -webkit-box !important; -webkit-line-clamp: 2; -webkit-box-orient: vertical; }
.blx-bar button { padding: 9px 14px !important; font-size: 14px !important; }
@media (max-width: 560px) { .blx-bar { right: 12px; left: 12px !important; width: auto !important; } }
@media print { .blh { display: none !important; } }
</style>"""

JS = r"""<script id="bl-header-js">
(function () {
  var h = document.querySelector('.blh'); if (!h) return;
  var burger = h.querySelector('.blh-burger');
  var bar = h.querySelector('.blh-tabs');
  function centerCurrent() {
    var cur = bar && (bar.querySelector('a[aria-current="page"]') || bar.querySelector('a[aria-current="true"]')); if (!cur || bar.scrollWidth <= bar.clientWidth) return;
    if (cur.offsetLeft + cur.offsetWidth < bar.clientWidth - 24) { bar.scrollLeft = 0; return; }
    var prev = cur.previousElementSibling; while (prev && prev.tagName !== 'A') prev = prev.previousElementSibling;
    bar.scrollLeft = Math.max(0, (prev ? prev.offsetLeft : cur.offsetLeft) - 6);
  }
  centerCurrent(); window.addEventListener('hashchange', function () { setTimeout(centerCurrent, 60); });
  /* Toolkits dropdown in the toolkit bar. The panel sits outside the scrolling bar so it is never clipped. */
  (function () {
    var btn = h.querySelector('.blh-tbtn'), menu = document.getElementById('blh-tmenu'); if (!btn || !menu) return;
    var wrap = menu.parentNode, links = function () { return menu.querySelectorAll('a'); };
    function place() { var b = btn.getBoundingClientRect(), w = wrap.getBoundingClientRect(); menu.style.left = Math.max(0, Math.min(b.left - w.left, w.width - menu.offsetWidth)) + 'px'; }
    function open(focusFirst) { menu.hidden = false; btn.setAttribute('aria-expanded', 'true'); place(); if (focusFirst) { var a = menu.querySelector('a[aria-current]') || links()[0]; if (a) a.focus(); } }
    function close(refocus) { if (menu.hidden) return; menu.hidden = true; btn.setAttribute('aria-expanded', 'false'); if (refocus) btn.focus(); }
    btn.addEventListener('click', function () { if (menu.hidden) open(false); else close(false); });
    btn.addEventListener('keydown', function (e) { if (e.key === 'ArrowDown') { e.preventDefault(); open(true); } });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !menu.hidden) { e.preventDefault(); close(true); } });
    menu.addEventListener('keydown', function (e) {
      var l = Array.prototype.slice.call(links()), i = l.indexOf(document.activeElement);
      if (e.key === 'ArrowDown') { e.preventDefault(); l[(i + 1) % l.length].focus(); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); l[(i - 1 + l.length) % l.length].focus(); }
    });
    menu.addEventListener('click', function (e) { if (e.target.closest && e.target.closest('a')) close(false); });
    document.addEventListener('click', function (e) { if (!menu.hidden && !menu.contains(e.target) && !btn.contains(e.target)) close(false); });
    menu.addEventListener('focusout', function (e) { if (!menu.hidden && e.relatedTarget && !menu.contains(e.relatedTarget) && e.relatedTarget !== btn) close(false); });
    if (bar) bar.addEventListener('scroll', function () { if (!menu.hidden) place(); });
    window.addEventListener('resize', function () { if (!menu.hidden) place(); });
    /* the hub marks the current group with aria-current; mirror it on the button */
    function sync() { btn.classList.toggle('is-current', !!menu.querySelector('a[aria-current]')); }
    sync();
    if (window.MutationObserver) new MutationObserver(sync).observe(menu, { attributes: true, subtree: true, attributeFilter: ['aria-current'] });
  })();
  function swipeHints() {
    Array.prototype.forEach.call(document.querySelectorAll('.table-wrap, .evt-wrap'), function (w) {
      var over = w.scrollWidth > w.clientWidth + 4, h = w.previousElementSibling, has = h && h.classList && h.classList.contains('blx-swipe');
      if (over && !has) { var p = document.createElement('p'); p.className = 'blx-swipe'; p.setAttribute('aria-hidden', 'true'); p.textContent = 'Swipe to see the whole table →'; w.parentNode.insertBefore(p, w); }
      else if (!over && has) h.parentNode.removeChild(h);
    });
  }
  var SEQ = __SEQ__;
  function seqIdx(href) { try { var p = new URL(href, location.href).pathname; for (var i = 0; i < SEQ.length; i++) if (p.slice(-SEQ[i].length) === SEQ[i]) return i; } catch (e) {} return -1; }
  var me = seqIdx(location.href), pagerNext = document.querySelector('.blp-a:not(.back)');
  function labelNext() {
    var box = document.getElementById('next'); if (!box || me < 0) return;
    var lab = box.querySelector('.next-label'), a = box.querySelector('a[href]'); if (!lab) return;
    var dl = box.getAttribute('data-label');
    if (dl) { if (lab.textContent !== dl) lab.textContent = dl; return; }   /* only write when it changes: the observer watches this box, so an unconditional write loops forever */
    if (!a) { lab.textContent = 'Next toolkit'; return; }
    var t = seqIdx(a.getAttribute('href')), pn = pagerNext ? seqIdx(pagerNext.getAttribute('href')) : -1;
    var txt = t < 0 ? 'Recommended next' : t < me ? 'Fix this first' : t === pn ? 'Next toolkit' : 'Recommended next';
    if (lab.textContent !== txt) lab.textContent = txt;
  }
  var nb = document.getElementById('next'); if (nb && window.MutationObserver) { new MutationObserver(labelNext).observe(nb, { childList: true, subtree: true, characterData: true, attributes: true, attributeFilter: ['data-label'] }); }
  window.addEventListener('load', labelNext); setTimeout(labelNext, 400);
  Array.prototype.forEach.call(document.querySelectorAll('.draft-banner'), function (b) { b.innerHTML = b.innerHTML.replace(/Owner: ([A-Z][a-z]+ [A-Z][A-Za-z-]+)/, 'Owner: <span class="nw">$1</span>'); });
  var xl = document.getElementById('xlinks');
  if (xl && !xl.querySelector('details')) {
    var lab0 = xl.querySelector('.label'), d0 = document.createElement('details'), sm = document.createElement('summary');
    d0.className = 'blx-rel'; sm.textContent = lab0 ? lab0.textContent : 'Related toolkits';
    d0.appendChild(sm); while (xl.firstChild) { if (xl.firstChild === lab0) xl.removeChild(lab0); else d0.appendChild(xl.firstChild); } xl.appendChild(d0);
  }

  (function () {
    var ans = document.getElementById('answer'), res = document.getElementById('results'), q = document.getElementById('col-q');
    if (!ans || !res || !q || !window.IntersectionObserver) return;
    var bar = document.createElement('div'); bar.className = 'blx-bar'; bar.setAttribute('role', 'status'); bar.setAttribute('aria-live', 'off');
    bar.innerHTML = '<div class="t"><small>Your result so far</small><b></b></div><button type="button">See plan ↓</button>';
    document.body.appendChild(bar);
    var label = bar.querySelector('b');
    function summary() {
      var f = ans.querySelector('.hero-fig'), h = f ? Array.prototype.map.call(f.children.length ? f.children : [f], function (c) { return c.hidden ? '' : c.textContent; }).join(' ') : '';
      if (!h || !h.trim()) { var hh = ans.querySelector('h2:not(.label), h3, .answer-line, p'); h = hh ? hh.textContent : ''; }
      return h.replace(/\s+/g, ' ').trim();
    }
    function upd() { label.textContent = summary() || 'Your plan is ready below'; }
    upd(); new MutationObserver(upd).observe(ans, { childList: true, subtree: true, characterData: true });
    var resVisible = false, qVisible = true;
    function toggle() { bar.classList.toggle('show', !resVisible && qVisible && window.innerWidth >= 0); }
    new IntersectionObserver(function (es) { es.forEach(function (e) { resVisible = e.isIntersecting; }); toggle(); }, { rootMargin: '0px 0px -35% 0px' }).observe(res);
    new IntersectionObserver(function (es) { es.forEach(function (e) { qVisible = e.isIntersecting; }); toggle(); }).observe(q);
    bar.querySelector('button').addEventListener('click', function () { ans.scrollIntoView({ behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' }); try { ans.focus({ preventScroll: true }); } catch (e) {} if (window.blTrack) window.blTrack('diy_see_plan_click'); });
  })();


  (function () {
    var form = document.getElementById('answers'); if (!form || !document.getElementById('col-q')) return;
    Array.prototype.forEach.call(form.querySelectorAll('.q'), function (q) {
      if (q.closest('.q') !== q || q.parentElement.closest('.q')) return;
      var kids = Array.prototype.filter.call(q.children, function (c) { return !c.classList.contains('sr-only') && !c.classList.contains('sr'); });
      if (!kids.length) return;
      var heads = kids.filter(function (c) { return c.tagName === 'LEGEND' || c.classList.contains('q-label'); });
      if (kids[0].classList.contains('q-row')) {
        q.classList.add('blx-row');
        if (heads.length) {
          var pr = null; Array.prototype.slice.call(q.children).forEach(function (c) {
            if (heads.indexOf(c) >= 0) { pr = document.createElement('div'); pr.className = 'blx-pair'; q.appendChild(pr); var a1 = document.createElement('div'); a1.className = 'blx-ph'; pr.appendChild(a1); a1.appendChild(c); var b1 = document.createElement('div'); b1.className = 'blx-pc'; pr.appendChild(b1); return; }
            if (pr && c !== pr) pr.querySelector('.blx-pc').appendChild(c);
          });
          q.classList.add('blx-pairs');
        }
        return;
      }
      if (kids[0].tagName === 'LEGEND') heads = [kids[0]];
      if (heads.length > 1 && kids[0] === heads[0]) {
        var nodes = Array.prototype.slice.call(q.children), pair = null, helps = [];
        nodes.forEach(function (c) {
          if (c.classList.contains('q-help')) { helps.push(c); return; }
          if (heads.indexOf(c) >= 0) { pair = document.createElement('div'); pair.className = 'blx-pair'; q.appendChild(pair); var hc = document.createElement('div'); hc.className = 'blx-ph'; pair.appendChild(hc); hc.appendChild(c); var cc = document.createElement('div'); cc.className = 'blx-pc'; pair.appendChild(cc); return; }
          if (pair) pair.querySelector('.blx-pc').appendChild(c);
        });
        if (helps.length) { var hw = document.createElement('div'); hw.className = 'blx-qh blx-pairhelp'; helps.forEach(function (h) { hw.appendChild(h); }); q.appendChild(hw); }
        q.classList.add('blx-pairs'); return;
      }
      if (heads.length !== 1 || kids[0] !== heads[0]) return;
      var head = heads[0], qh = document.createElement('div'), qc = document.createElement('div');
      qh.className = 'blx-qh'; qc.className = 'blx-qc';
      Array.prototype.slice.call(q.children).forEach(function (c) {
        if (c === head) return;
        if (c.classList.contains('q-help')) qh.appendChild(c); else qc.appendChild(c);
      });
      q.appendChild(qh); q.appendChild(qc); q.classList.add('blx-split');
    });
  })();
  var swT; window.addEventListener('resize', function () { clearTimeout(swT); swT = setTimeout(swipeHints, 150); });
  window.addEventListener('load', swipeHints); setTimeout(swipeHints, 600); document.addEventListener('click', function () { setTimeout(swipeHints, 120); });
  function closeAll(except) { Array.prototype.forEach.call(h.querySelectorAll('.blh-li.open'), function (li) { if (li !== except) { li.classList.remove('open'); var b = li.querySelector('.blh-top'); if (b) b.setAttribute('aria-expanded', 'false'); } }); }
  Array.prototype.forEach.call(h.querySelectorAll('button.blh-top'), function (b) {
    b.addEventListener('click', function () { var li = b.parentNode, open = !li.classList.contains('open'); closeAll(li); li.classList.toggle('open', open); b.setAttribute('aria-expanded', open ? 'true' : 'false'); });
  });
  if (burger) burger.addEventListener('click', function () { var open = !h.classList.contains('menu-open'); h.classList.toggle('menu-open', open); burger.setAttribute('aria-expanded', open ? 'true' : 'false'); });
  document.addEventListener('click', function (e) { if (!h.contains(e.target)) { closeAll(null); if (h.classList.contains('menu-open')) { h.classList.remove('menu-open'); if (burger) burger.setAttribute('aria-expanded', 'false'); } } });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { closeAll(null); if (h.classList.contains('menu-open')) { h.classList.remove('menu-open'); burger.setAttribute('aria-expanded', 'false'); burger.focus(); } } });
})();
</script>"""


# ---- Engagement tracking ---------------------------------------------------
# Fill these in and rerun `python3 tools/site_header.py` to turn on GA4 (via Tag Manager) and HubSpot.
# Do NOT fill them in until the site is hosted where a cookie-consent banner controls these tags (e.g. bigleap.com),
# or a consent default is added here: as written, both load as soon as an ID is set, with no consent check.
# Until then, events still go into window.dataLayer, so nothing is lost in the page logic.
GTM_ID = ''        # e.g. 'GTM-XXXXXXX' (Big Leap's container)
HUBSPOT_ID = ''    # e.g. '1234567' (Big Leap's HubSpot Hub ID, for the tracking code)

TRACK_TMPL = r"""<script id="bl-track-js">
/* Big Leap DIY toolkits: engagement events. Sends diy_* events to dataLayer (GA4 via Tag Manager). No personal data. */
(function () {
  var GTM = '__GTM__', HUB = '__HUB__';
  window.dataLayer = window.dataLayer || [];
  if (GTM) { (function (w, d, s, l, i) { w[l].push({ 'gtm.start': new Date().getTime(), event: 'gtm.js' }); var f = d.getElementsByTagName(s)[0], j = d.createElement(s); j.async = true; j.src = 'https://www.googletagmanager.com/gtm.js?id=' + i; f.parentNode.insertBefore(j, f); })(window, document, 'script', 'dataLayer', GTM); }
  if (HUB) { var hs = document.createElement('script'); hs.async = true; hs.defer = true; hs.id = 'hs-script-loader'; hs.src = 'https://js.hs-scripts.com/' + HUB + '.js'; document.head.appendChild(hs); }
  var m = location.pathname.match(/toolkits\/([a-z]+)\/(\d+)_/), page = location.pathname.split('/').pop() || 'index.html';
  var ctx = m ? { toolkit: m[1] + '-' + m[2], service: m[1] } : { toolkit: '', service: '' };
  function track(ev, extra) {
    var o = { event: ev, toolkit: ctx.toolkit, service: ctx.service, page: page };
    if (extra) for (var k in extra) o[k] = extra[k];
    window.dataLayer.push(o);
    try { if (window._hsq && ev === 'diy_cta_click') window._hsq.push(['trackCustomBehavioralEvent', { name: 'diy_cta_click', properties: { toolkit: ctx.toolkit } }]); } catch (e) {}
  }
  window.blTrack = track;
  track(m ? 'diy_toolkit_view' : 'diy_page_view');
  var started = false, profiled = false;
  function inMain(el) { return !el.closest('.blh, .blp'); }
  /* Progress, for "Your roadmap": bl_diy_progress_v1 = { v: 1, kits: { "<series>-<nn>": { first, last, worked, headline, planTaken } } }.
     Written only on toolkit pages, only after the visitor changes an answer, never from example answers. Stays in this browser.
     A newer version of the key is left alone. */
  var PK = 'bl_diy_progress_v1', hT = null, worked = false;
  function prog(fn) {
    if (!m) return;
    try {
      var raw = localStorage.getItem(PK), d = raw ? JSON.parse(raw) : null;
      if (d && d.v !== 1) return;
      d = d || { v: 1, kits: {} }; d.kits = d.kits || {};
      var k = d.kits[ctx.toolkit] || {}; fn(k, new Date().toISOString()); d.kits[ctx.toolkit] = k;
      localStorage.setItem(PK, JSON.stringify(d));
    } catch (e) {}
  }
  function isExample() { var p = document.getElementById('example-pill'); return !!(p && /example/i.test(p.textContent || '')); }
  function headline() {
    var a = document.getElementById('answer'); if (!a) return '';
    var f = a.querySelector('.hero-fig'), l = a.querySelector('.answer-line');
    var ft = f ? Array.prototype.map.call(f.childNodes, function (n) { return n.nodeType === 1 && n.hidden ? '' : n.textContent; }).join(' ') : '';
    return (ft + ' · ' + (l ? l.textContent : '')).replace(/\s+/g, ' ').replace(/^ · | · $/g, '').trim().slice(0, 180);
  }
  function saveHeadline() { clearTimeout(hT); hT = setTimeout(function () { if (!worked || isExample()) return; var h = headline(); prog(function (k, now) { k.last = now; if (h) k.headline = h; }); }, 900); }
  function onStart(e) {
    if (!m || !e.target || !inMain(e.target) || !e.isTrusted) return;
    if (!started) { started = true; track('diy_toolkit_start'); }
    if (!worked) { worked = true; prog(function (k, now) { k.first = k.first || now; k.last = now; k.worked = true; }); }
    saveHeadline();
  }
  document.addEventListener('change', onStart, true);
  document.addEventListener('input', onStart, true);
  try {
    var set = Storage.prototype.setItem;
    Storage.prototype.setItem = function (k, v) { if (k === 'bl_diy_profile_v1' && !profiled) { profiled = true; setTimeout(function () { track('diy_profile_saved'); }, 0); } return set.apply(this, arguments); };
  } catch (e) {}
  document.addEventListener('click', function (e) {
    var el = e.target.closest && e.target.closest('a, button'); if (!el) return;
    var txt = (el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 80), href = el.getAttribute('href') || '';
    if (el.closest('.blp, .blh-pn')) return track('diy_next_click', { label: txt });
    if (/utm_medium=talk-to-owner/.test(href) || /^Talk to /i.test(txt) || el.classList.contains('blh-cta') || /get-started/.test(href)) return track('diy_cta_click', { label: txt, link_url: href });
    if (el.tagName === 'BUTTON' && /copy/i.test(txt)) { if (worked && !isExample()) prog(function (k, now) { k.planTaken = now; k.headline = headline() || k.headline; }); return track('diy_plan_copy', { label: txt }); }
    if (/download|print|save as|\.md\b|\.txt\b/i.test(txt) || el.hasAttribute('download')) { if (worked && !isExample()) prog(function (k, now) { k.planTaken = now; k.headline = headline() || k.headline; }); return track('diy_plan_download', { label: txt }); }
    if (/email me/i.test(txt)) return track('diy_plan_email', { label: txt });
    if (el.tagName === 'A' && /toolkits\/[a-z]+\/\d+_/.test(href) && !el.closest('.blh')) return track('diy_crosslink_click', { label: txt, link_url: href });
  }, true);
})();
</script>"""

# "Try me" cue: a small red badge on the first control a visitor can play with, until they touch it.
# Targets: the first [data-try] element on the page; on toolkit pages, otherwise the first answer group.
# Badge is positioned in page coordinates so containers with overflow:hidden don't clip it.
TRY_JS = r"""<script id="bl-try-js">
(function () {
  'use strict';
  var css = '.bl-try-badge{position:absolute;z-index:40;padding:1px 8px;border-radius:999px;background:#EA4335;color:#fff;font:700 11px/1.6 "Open Sans","Segoe UI",Arial,sans-serif;pointer-events:none;white-space:nowrap;box-shadow:0 2px 6px rgba(20,61,85,.25)}' +
    '@media (prefers-reduced-motion:no-preference){.bl-try-glow{animation:bl-try-glow 2.4s ease-in-out infinite}.bl-try-badge{animation:bl-try-bob 2.4s ease-in-out infinite}}' +
    '@keyframes bl-try-glow{0%,100%{box-shadow:0 0 0 0 rgba(49,135,181,0)}50%{box-shadow:0 0 0 5px rgba(49,135,181,.3)}}' +
    '@keyframes bl-try-bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-2px)}}' +
    '@media print{.bl-try-badge{display:none}}';
  function find() {
    var t = document.querySelector('[data-try]');
    if (t) return t.offsetParent ? t : null;
    if (!/\/toolkits\/[a-z]+\//.test(location.pathname)) return null;
    var all = document.querySelectorAll('[role="radiogroup"], label.opt, .seg');
    for (var i = 0; i < all.length; i++) if (all[i].offsetParent && !all[i].closest('.blh, .blx-bar, details:not([open])')) return all[i];
    return null;
  }
  function start(t) {
    var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
    var b = document.createElement('span'); b.className = 'bl-try-badge'; b.setAttribute('aria-hidden', 'true'); b.textContent = t.getAttribute('data-try') || 'Try me';
    document.body.appendChild(b); t.classList.add('bl-try-glow');
    function place() {
      if (!document.body.contains(t) || !t.offsetParent) { b.style.display = 'none'; if (!document.body.contains(t)) stop(); return; }
      var r = t.getBoundingClientRect(); b.style.display = '';
      b.style.top = Math.round(r.top + window.scrollY - 10) + 'px';
      b.style.left = Math.round(r.right + window.scrollX - b.offsetWidth + 6) + 'px';
    }
    var iv = setInterval(place, 800);
    function stop() { clearInterval(iv); window.removeEventListener('resize', place); if (b.parentNode) b.parentNode.removeChild(b); t.classList.remove('bl-try-glow'); }
    ['pointerdown', 'keydown', 'change'].forEach(function (ev) { t.addEventListener(ev, stop, { once: true }); });
    window.addEventListener('resize', place); place();
  }
  var tries = 0;
  (function go() { var t = find(); if (t) return start(t); if (++tries < 6) setTimeout(go, 500); })();
})();
</script>"""

# Expert card: the service owner's photo, name and title, placed above the "Talk to ..." buttons in a
# toolkit's closing section. Data comes from data/widgets.json (people) at build time.
OWNER_TMPL = r"""<script id="bl-owner-js">
(function () {
  var P = __OWNER__;
  var box = document.querySelector('section.closing .closing-actions');
  if (!box || !P.name || document.querySelector('.bl-expert')) return;
  var st = document.createElement('style');
  st.textContent = '.bl-expert{display:flex;align-items:center;gap:14px;margin:2px 0}.bl-expert img,.bl-expert .ini{width:56px;height:56px;border-radius:50%;object-fit:cover;flex:0 0 auto;box-shadow:0 0 0 3px rgba(255,255,255,.85)}.bl-expert .ini{display:grid;place-items:center;background:rgba(255,255,255,.18);font:800 18px "Raleway",Arial,sans-serif}.bl-expert b{display:block;font-size:16px;line-height:1.3}.bl-expert span{display:block;font-size:14px;color:var(--cta-muted,inherit)}@media print{.bl-expert img{box-shadow:none}}';
  document.head.appendChild(st);
  var d = document.createElement('div'); d.className = 'bl-expert';
  var ini = P.name.split(/\s+/).map(function (w) { return w.charAt(0); }).join('').slice(0, 2);
  d.innerHTML = (P.photo ? '<img src="' + P.photo + '" alt="" width="56" height="56">' : '<span class="ini" aria-hidden="true">' + ini + '</span>') +
    '<div><b></b><span></span></div>';
  d.querySelector('b').textContent = P.name;
  d.querySelector('span').textContent = (P.title ? P.title + ' · ' : '') + 'Your Big Leap expert';
  box.parentNode.insertBefore(d, box);
})();
</script>"""

def owner_js(page, name, people):
    pp = people.get(name, {})
    photo = rel(page, pp['photo']) if pp.get('photo') else ''
    return OWNER_TMPL.replace('__OWNER__', json.dumps({'name': name, 'title': pp.get('title', ''), 'photo': photo}))

def track_js():
    return TRACK_TMPL.replace('__GTM__', GTM_ID).replace('__HUB__', HUBSPOT_ID)

def rel(frm, to):
    r = os.path.relpath(os.path.join(ROOT, to), os.path.dirname(os.path.join(ROOT, frm))).replace(os.sep, '/')
    return r

def header(page, current, where='', prev=None, nxt=None, extra='', service=None):
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
    SERVICES = [('RevOps', 'revops'), ('Paid Media', 'paid'), ('SEO', 'seo'), ('Digital PR', 'pr'), ('Email Marketing', 'email'), ('Strategy', 'strategy')]
    # "Toolkits" dropdown: every service group, plus All toolkits. Then the other pages as tabs, so every page is one
    # click from the bar. Client-facing pages sit on the left; internal pages are grouped on the right under "Internal".
    menu_items = [('All toolkits', 'index.html#toolkits', 'toolkits')] + [(n, 'index.html#' + k, k) for n, k in SERVICES]
    tabs = [('Start here', 'toolkits/paid/01_What_Kind_of_Business_Are_You.html', 'start'), ('Roadmap', 'roadmap.html', 'roadmap'), ('Journey map', 'journey.html', 'journey')]
    tabs = [x for x in tabs if x[2] != 'journey']   # the Journey map is internal
    tools_tabs = [('Journey map', 'journey.html', 'journey'), ('Sales assets', 'sales.html', 'sales'), ('Widgets', 'index.html#widgets', 'widgets'), ('Mockups', 'mockups/homepage.html', 'mockups'), ('Status & review', 'review.html', 'review')]
    def tab(t_, f, key):
        # one aria-current="page" per page; the service a toolkit belongs to is marked "true" (same look)
        cur = ' aria-current="page"' if key == current else (' aria-current="true"' if key == service else '')
        return f'<a href="{rel(page, f)}" data-tab="{key}"' + cur + f'>{e(t_)}</a>'
    in_menu = any(k in (current, service) for _, _, k in menu_items)
    menu_btn = (f'<button type="button" class="blh-tbtn{" is-current" if in_menu else ""}" aria-expanded="false" aria-controls="blh-tmenu">'
                'Toolkits<span class="car" aria-hidden="true"></span></button>')
    menu_html = ('<div class="blh-tmenu" id="blh-tmenu" hidden><ul>' + ''.join('<li>' + tab(*x) + '</li>' for x in menu_items) + '</ul></div>')
    tab_html = (menu_btn + ''.join(tab(*x) for x in tabs) +
                '<span class="blh-int" role="group" aria-label="Internal pages"><span class="blh-int-l" aria-hidden="true">Internal</span>' + ''.join(tab(*x) for x in tools_tabs) + '</span>')
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
            f'<nav class="blh-tabs" aria-label="DIY Toolkits"><span class="blh-label">DIY Toolkits</span>{tab_html}</nav>{menu_html}'
            + (f'<div class="blh-right">{extra}</div>' if extra else '') +
            '</div></div></header><!-- /bl-header -->')

def pager(page, prev, nxt, where):
    e = html.escape
    hub = rel(page, 'index.html')
    def lk(item, label, back):
        if not item:
            return f'<a class="blp-a{" back" if back else ""}" href="{hub}"><small>{label}</small><b>All toolkits</b></a>'
        title, f = item
        return f'<a class="blp-a{" back" if back else ""}" href="{rel(page, f)}"><small>{"← " if back else ""}{label}{"" if back else " →"}</small><b>{e(title)}</b></a>'
    return ('<!-- bl-pager --><nav class="blp" aria-label="Previous and next toolkit"><div class="blp-in">'
            + lk(prev, 'Previous', True) + f'<a class="blp-hub" href="{hub}"><small>{e(where)}</small><b>All toolkits</b></a>' + lk(nxt, 'Next', False)
            + '</div></nav><!-- /bl-pager -->')

SEQ_JSON = '[]'

def apply(page, block, before_selector=None, bottom=''):
    p = os.path.join(ROOT, page)
    s = open(p, encoding='utf-8').read()
    # strip old versions (this header + the earlier bl-sitenav bar)
    s = re.sub(r'<!-- bl-header -->.*?<!-- /bl-header -->\n?', '', s, flags=re.S)
    s = re.sub(r'<!-- bl-sitenav -->.*?<!-- /bl-sitenav -->\n?', '', s, flags=re.S)
    s = re.sub(r'<style id="bl-(?:sitenav|header)-css">.*?</style>\n?', '', s, flags=re.S)
    s = re.sub(r'<script id="bl-header-js">.*?</script>\n?', '', s, flags=re.S)
    s = re.sub(r'<!-- bl-pager -->.*?<!-- /bl-pager -->\n?', '', s, flags=re.S)
    s = re.sub(r'<script id="bl-track-js">.*?</script>\n?', '', s, flags=re.S)
    s = re.sub(r'<script id="bl-try-js">.*?</script>\n?', '', s, flags=re.S)
    s = re.sub(r'<script id="bl-owner-js">.*?</script>\n?', '', s, flags=re.S)
    s = re.sub(r'<script id="bl-version-js"[^>]*></script>\n?', '', s)   # removes the retired version switch
    fonts = rel(page, 'assets/fonts/fonts.css')
    if 'fonts.css' not in s:
        s = s.replace('</head>', f'<link rel="stylesheet" href="{fonts}">\n</head>', 1)
    s = s.replace('</head>', CSS + '\n' + track_js() + '\n</head>', 1)
    s = re.sub(r'(<body[^>]*>)', lambda m: m.group(1) + '\n' + block, s, count=1)
    s = s.replace('</body>', (bottom + '\n' if bottom else '') + JS.replace('__SEQ__', SEQ_JSON) + '\n' + TRY_JS + '\n</body>', 1)
    open(p, 'w', encoding='utf-8').write(s)

if __name__ == '__main__':
    import sys
    only_pages = 'pages-only' in sys.argv
    d = json.load(open(os.path.join(ROOT, 'toolkits.json')))
    PEOPLE = json.load(open(os.path.join(ROOT, 'data', 'widgets.json'))).get('people', {})
    ORDER = [x for x in ['paid', 'revops', 'seo', 'pr', 'email', 'strategy'] if x in {s['id'] for s in d['series']}]           # journey order: Business Profile first
    by = {s['id']: s for s in d['series']}
    seq = [(by[sid], t) for sid in ORDER for t in by[sid]['toolkits']]
    SEQ_JSON = json.dumps([t['file'] for _, t in seq])
    for i, (s, t) in enumerate(seq if not only_pages else []):
        prev = seq[i - 1] if i else None
        nxt = seq[i + 1] if i + 1 < len(seq) else None
        fmt = lambda it: None if not it else ((it[1]['title'] if it[0]['id'] == s['id'] else f"{it[0]['name']}: {it[1]['title']}"), it[1]['file'])
        cur = 'start' if t['file'].endswith('paid/01_What_Kind_of_Business_Are_You.html') else 'toolkit'
        apply(t['file'], header(t['file'], cur, '', None, None, '', s['id']),
              bottom=pager(t['file'], fmt(prev), fmt(nxt), f"{s['name']} · Toolkit {t['n']} of {len(s['toolkits'])}") + '\n' + owner_js(t['file'], s['owner'], PEOPLE))
        print('toolkit', t['file'])
    theme = '<button class="blh-theme" id="theme" type="button" aria-label="Switch light or dark mode" title="Light or dark mode"><svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 3a9 9 0 0 0 0 18z" fill="currentColor"/></svg></button>'
    apply('index.html', header('index.html', 'toolkits', '', None, None, theme))
    apply('journey.html', header('journey.html', 'journey', '', None, None, ''))
    apply('mockups/homepage.html', header('mockups/homepage.html', 'mockups', '', None, None, ''))
    apply('mockups/toolkits-landing.html', header('mockups/toolkits-landing.html', 'mockups', '', None, None, ''))
    # Internal Team Review page (not linked from toolkit content, only from the toolkit bar).
    if os.path.exists(os.path.join(ROOT, 'review.html')):
        apply('review.html', header('review.html', 'review', '', None, None, theme))
    # Sales assets: the live-call deck, per-service options and talk tracks. Internal; tab only.
    if os.path.exists(os.path.join(ROOT, 'sales.html')):
        apply('sales.html', header('sales.html', 'sales', '', None, None, theme))
    # Your Marketing Roadmap: a shared output page with its own tab; no pager.
    if os.path.exists(os.path.join(ROOT, 'roadmap.html')):
        apply('roadmap.html', header('roadmap.html', 'roadmap', '', None, None, ''))
    # Preview modules: drafts listed under "previews" in toolkits.json. They get the site header but
    # no Previous/Next pager, and they are never added to SEQ, so the public sequence is unchanged
    # until a draft is approved and moved into a series.
    for pv in d.get('previews', []):
        if os.path.exists(os.path.join(ROOT, pv['file'])):
            apply(pv['file'], header(pv['file'], 'preview', '', None, None, ''))
            print('preview', pv['file'])
    print('index.html, journey.html, review.html, sales.html')
