#!/usr/bin/env python3
"""Big Leap site header for every DIY Toolkits page.

Tier 1 copies the bigleap.com header (logo, Services / Who We Serve / Case Studies / Resources / About menus,
"Get Your Custom Strategy"), with links to the live site, so the toolkits read as part of bigleap.com.
Tier 2 is the toolkit bar. Client-facing pages sit on the left (Toolkits menu · Start here · Your journey · Roadmap); internal pages
sit on the right under "Internal" (Customer journey · Sales assets · Widgets · Mockups · Status & review),
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
.blh-pill { margin-left: 6px; padding: 1px 7px; border-radius: 999px; background: #EA4335; color: #fff; font: 800 10px/1.6 "Open Sans", Arial, sans-serif; letter-spacing: .04em; text-transform: uppercase; white-space: nowrap; }
.blh-pill[hidden] { display: none; }
.blh-strip { background: #143D55; color: #fff; font: 600 13px/1.4 "Open Sans", Arial, sans-serif; text-align: center; padding: 8px 16px; }
.draft-strip, .draft-banner { display: none !important; }
.blh-tabs a .count { display: none !important; }
.blf .blh-theme { background: #22394A; border-color: #2D4556; color: #DCE9F2; }
.blh-subnav { background: #fff; border-bottom: 1px solid #D4DADF; }
.blh-subnav .blh-in { display: flex; align-items: center; min-height: 46px; }
.blh-stabs { display: flex; align-items: center; gap: 4px; overflow-x: auto; scrollbar-width: none; padding: 5px 0; }
.blh-stabs::-webkit-scrollbar { display: none; }
.blh-slabel { flex: 0 0 auto; margin-right: 8px; font: 700 12px "Open Sans", Arial, sans-serif; letter-spacing: .06em; text-transform: uppercase; color: #5F6E79; }
.blh-stabs a { flex: 0 0 auto; display: inline-flex; align-items: center; min-height: 36px; padding: 4px 12px; border-radius: 8px; font: 600 14px "Open Sans", Arial, sans-serif; color: #143D55; text-decoration: none; white-space: nowrap; border-bottom: 3px solid transparent; }
.blh-stabs a:hover { background: #EEF3F8; }
.blh-stabs a[aria-current="page"] { border-radius: 0; border-bottom-color: #EA4335; font-weight: 700; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) .blh-subnav { background: #142632; border-bottom-color: #22394A; } :root:not([data-theme="light"]) .blh-stabs a { color: #DCE9F2; } :root:not([data-theme="light"]) .blh-stabs a:hover { background: #1D3A4C; } }
:root[data-theme="dark"] .blh-subnav { background: #142632; border-bottom-color: #22394A; } :root[data-theme="dark"] .blh-stabs a { color: #DCE9F2; } :root[data-theme="dark"] .blh-stabs a:hover { background: #1D3A4C; }
@media print { .blh-subnav { display: none !important; } }
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
#blh-tmenu li:first-child { border-bottom: 1px solid #EEF3F8; padding-bottom: 4px; margin-bottom: 2px; }
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
  /* the "Start here" pill on My Profile shows until the visitor has a Business Profile */
  try { if (localStorage.getItem('bl_diy_profile_v1')) Array.prototype.forEach.call(h.querySelectorAll('[data-start-pill]'), function (x) { x.hidden = true; }); } catch (e) {}
  function centerCurrent() {
    var cur = bar && (bar.querySelector('a[aria-current="page"]') || bar.querySelector('a[aria-current="true"]')); if (!cur || bar.scrollWidth <= bar.clientWidth) return;
    if (cur.offsetLeft + cur.offsetWidth < bar.clientWidth - 24) { bar.scrollLeft = 0; return; }
    var prev = cur.previousElementSibling; while (prev && prev.tagName !== 'A') prev = prev.previousElementSibling;
    bar.scrollLeft = Math.max(0, (prev ? prev.offsetLeft : cur.offsetLeft) - 6);
  }
  centerCurrent(); window.addEventListener('hashchange', function () { setTimeout(centerCurrent, 60); });
  /* Dropdowns in the toolkit bar (All toolkits, My Profile, Assets). Panels sit outside the scrolling bar so they are never clipped. */
  var dds = [];
  Array.prototype.forEach.call(h.querySelectorAll('.blh-tbtn'), function (btn) {
    var menu = document.getElementById(btn.getAttribute('aria-controls')); if (!menu) return;
    var wrap = menu.parentNode, links = function () { return menu.querySelectorAll('a'); };
    function place() { var b = btn.getBoundingClientRect(), w = wrap.getBoundingClientRect(); menu.style.left = Math.max(0, Math.min(b.left - w.left, w.width - menu.offsetWidth)) + 'px'; }
    function open(focusFirst) { dds.forEach(function (d) { if (d.menu !== menu) d.close(false); }); menu.hidden = false; btn.setAttribute('aria-expanded', 'true'); place(); if (focusFirst) { var a = menu.querySelector('a[aria-current]') || links()[0]; if (a) a.focus(); } }
    function close(refocus) { if (menu.hidden) return; menu.hidden = true; btn.setAttribute('aria-expanded', 'false'); if (refocus) btn.focus(); }
    dds.push({ menu: menu, close: close });
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
    /* the catalog marks the current service with aria-current; mirror it on the button */
    function sync() { btn.classList.toggle('is-current', !!menu.querySelector('a[aria-current]')); }
    sync();
    if (window.MutationObserver) new MutationObserver(sync).observe(menu, { attributes: true, subtree: true, attributeFilter: ['aria-current'] });
  });
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
  /* Has the visitor already worked the toolkit at this href, per their own saved progress? Read-only. */
  function kitWorked(href) {
    try {
      var m = new URL(href, location.href).pathname.match(/toolkits\/([a-z]+)\/(\d+)_/);
      if (!m) return false;
      var d = JSON.parse(localStorage.getItem('bl_diy_progress_v1') || 'null');
      var k = d && d.kits && d.kits[m[1] + '-' + m[2]];
      return !!(k && k.worked);
    } catch (e) { return false; }
  }
  function labelNext() {
    var box = document.getElementById('next'); if (!box || me < 0) return;
    var lab = box.querySelector('.next-label'), a = box.querySelector('a[href]'); if (!lab) return;
    var dl = box.getAttribute('data-label');
    if (dl) { if (lab.textContent !== dl) lab.textContent = dl; return; }   /* only write when it changes: the observer watches this box, so an unconditional write loops forever */
    if (!a) { lab.textContent = 'Next toolkit'; return; }
    var href = a.getAttribute('href'), t = seqIdx(href), pn = pagerNext ? seqIdx(pagerNext.getAttribute('href')) : -1;
    /* Earlier in sequence AND not already worked: a real skipped prerequisite. Already worked: don't call it a gap. */
    var txt = t < 0 ? 'Recommended next' : (t < me && !kitWorked(href)) ? 'Fix this first' : t === pn ? 'Next toolkit' : 'Recommended next';
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
    if (/utm_medium=talk-to-owner/.test(href) || /^Talk to /i.test(txt) || /^mailto:/i.test(href) || /^Email /i.test(txt) || el.classList.contains('blh-cta') || /get-started/.test(href)) return track('diy_cta_click', { label: txt, link_url: href });
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

# Expert card: the service owner's "Talk To An Expert" card (banner photo, bio, QR code that opens an email),
# placed above the closing buttons of every toolkit. It also turns the closing "Talk to ..." button into
# "Email <owner>", a mailto link with the toolkit in the subject. Data comes from data/widgets.json (people).
OWNER_TMPL = r"""<script id="bl-owner-js">
(function () {
  var P = __OWNER__;
  var box = document.querySelector('section.closing .closing-actions');
  if (!box || !P.name || document.querySelector('.bl-expert')) return;
  var first = P.name.split(/\s+/)[0];
  var title = ((document.querySelector('h1') || {}).textContent || document.title.split(' · ')[0]).trim();
  var page = location.href.split('#')[0];
  var mail = P.email ? 'mailto:' + P.email + '?subject=' + encodeURIComponent(title + ': a question for ' + first) + '&body=' + encodeURIComponent('Hi ' + first + ',\n\nI worked through "' + title + '" (' + page + ') and would like to talk about the next step.\n\n') : '';
  var st = document.createElement('style');
  st.textContent = '.bl-expert{margin:4px 0 8px;border-radius:14px;overflow:hidden;background:#0F1B24;color:#fff}' +
    '.bl-expert .bx-photo{height:210px;background:#0F1B24 center 28%/cover no-repeat;position:relative}' +
    '.bl-expert .bx-photo:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(15,27,36,0) 50%,#0F1B24 100%)}' +
    '.bl-expert .bx-body{display:flex;gap:18px;align-items:center;padding:14px 20px 20px}' +
    '.bl-expert .bx-text{flex:1 1 auto;min-width:0}' +
    '.bl-expert h3{margin:0 0 6px;font:700 22px/1.2 "Raleway",Arial,sans-serif;color:#fff}' +
    '.bl-expert p{margin:0;font-size:14.5px;line-height:1.55;color:#C9D3DA}' +
    '.bl-expert .bx-who{display:flex;align-items:center;gap:10px;margin-top:12px;font-size:13px;color:#9FB0BC}' +
    '.bl-expert .bx-who b{color:#fff}' +
    '.bl-expert .bx-who img,.bl-expert .ini{width:40px;height:40px;border-radius:50%;object-fit:cover;flex:0 0 auto;box-shadow:0 0 0 2px rgba(255,255,255,.85)}' +
    '.bl-expert .ini{display:grid;place-items:center;background:rgba(255,255,255,.18);font:800 15px "Raleway",Arial,sans-serif;color:#fff}' +
    '.bl-expert .bx-qr{flex:0 0 auto;background:#fff;border-radius:12px;padding:8px 8px 6px;text-align:center;text-decoration:none}' +
    '.bl-expert .bx-qr img{display:block;width:132px;height:132px}' +
    '.bl-expert .bx-qr span{display:block;margin-top:3px;font:700 11px/1.3 Arial,sans-serif;color:#0F1B24}' +
    '@media (max-width:700px){.bl-expert .bx-qr{display:none}.bl-expert .bx-photo{height:170px}.bl-expert .bx-body{padding:12px 16px 16px}}' +
    '@media print{.bl-expert{background:#fff;color:#000;border:1px solid #bbb;break-inside:avoid}.bl-expert h3,.bl-expert .bx-who b{color:#000}.bl-expert p,.bl-expert .bx-who{color:#333}.bl-expert .bx-qr{display:block!important;border:1px solid #ddd}.bl-expert .bx-photo{display:none}}';
  document.head.appendChild(st);
  var d = document.createElement('div'); d.className = 'bl-expert';
  var ini = P.name.split(/\s+/).map(function (w) { return w.charAt(0); }).join('').slice(0, 2);
  d.innerHTML = (P.banner ? '<div class="bx-photo" role="img" aria-label=""></div>' : '') +
    '<div class="bx-body"><div class="bx-text"><h3>Talk To An Expert</h3><p class="bx-bio"></p>' +
    '<div class="bx-who">' + (P.photo ? '<img src="' + P.photo + '" alt="" width="40" height="40">' : '<span class="ini" aria-hidden="true">' + ini + '</span>') + '<span><b></b><br><span class="bx-t"></span></span></div></div>' +
    (P.qr && mail ? '<a class="bx-qr" href="' + mail + '"><img src="' + P.qr + '" alt="QR code: email ' + first + '" width="132" height="132"><span>Scan to email ' + first + '</span></a>' : '') + '</div>';
  if (P.banner) d.querySelector('.bx-photo').style.backgroundImage = 'url("' + P.banner + '")';
  d.querySelector('.bx-bio').textContent = P.bio || ('Meet ' + first + '. ' + (P.title || 'Your Big Leap expert') + '.');
  d.querySelector('.bx-who b').textContent = P.name;
  d.querySelector('.bx-t').textContent = (P.title ? P.title + ' · ' : '') + 'Your Big Leap expert';
  box.parentNode.insertBefore(d, box);
  /* the closing button: email the owner instead of a contact form */
  var cta = document.getElementById('cta-link');
  if (cta && mail) { cta.href = mail; cta.removeAttribute('target'); cta.textContent = 'Email ' + first + (/optional/i.test(cta.textContent) ? ' (optional)' : ''); }
})();
</script>"""

def owner_js(page, name, people):
    pp = people.get(name, {})
    r = lambda k: rel(page, pp[k]) if pp.get(k) else ''
    return OWNER_TMPL.replace('__OWNER__', json.dumps({'name': name, 'title': pp.get('title', ''), 'photo': r('photo'), 'banner': r('banner'), 'qr': r('qr'), 'bio': pp.get('bio', ''), 'email': pp.get('email', '')}, ensure_ascii=False))


# Saved answers, for "My Profile": every toolkit remembers its own answers in this browser and restores them on the
# next visit. bl_diy_answers_v1 = { v: 1, kits: { "<folder>-<nn>": { v: 1, title, url, updated, fields: [ { k, type, label, value, text } ] } } }
# Saved only after a real (trusted) answer change, never while the page shows example answers. Strategy starters
# restore themselves from bl_diy_assess_v1, so here they are only recorded for display. Paid 01 is the Business
# Profile itself, which has its own key. A newer version of the key is left alone.
ANSWERS_JS = r"""<script id="bl-answers-js">
(function () {
  var m = location.pathname.match(/toolkits\/([a-z]+)\/(\d+)_/); if (!m) return;
  var KEY = 'bl_diy_answers_v1', kit = m[1] + '-' + m[2];
  if (kit === 'paid-01') return;
  var form = document.getElementById('answers'); if (!form) return;
  var selfRestoring = m[1] === 'plan', restoring = false, sT = null;
  function load() { try { var d = JSON.parse(localStorage.getItem(KEY)); return d && d.v === 1 ? d : (d ? null : { v: 1, kits: {} }); } catch (e) { return { v: 1, kits: {} }; } }
  function isExample() { var p = document.getElementById('example-pill'); return !!(p && /example/i.test(p.textContent || '')); }
  function clean(el) { if (!el) return ''; var c = el.cloneNode(true); Array.prototype.forEach.call(c.querySelectorAll('.pf-tag, .bl-try-badge, .sr-only, .sr, .chip'), function (x) { x.remove(); }); return (c.textContent || '').replace(/\s+/g, ' ').trim(); }
  function labelFor(el) {
    var g = el.closest('[role="radiogroup"], [role="group"]'), id = g && g.getAttribute('aria-labelledby');
    if (id && document.getElementById(id)) return clean(document.getElementById(id));
    if (el.id) { var l = form.querySelector('label[for="' + el.id + '"]'); if (l && el.type !== 'radio' && el.type !== 'checkbox') return clean(l); }
    var lb = el.getAttribute('aria-labelledby'); if (lb && document.getElementById(lb)) return clean(document.getElementById(lb));
    var q = el.closest('.q-row, .data-f, .q'); var t = q && q.querySelector('.row-label, .data-l, .q-label, legend'); return clean(t) || el.name || el.id;
  }
  function optText(el) { var l = el.id && form.querySelector('label[for="' + el.id + '"]'); return clean(l || el.closest('label')) || el.value; }
  function serialize() {
    /* Besides the current value, also capture every option a choice field offered (opts: [{v,t}]),
       so a page outside this toolkit (My Profile's inline editor) can rebuild the same choice -
       not just display what was picked. Free-text fields need no opts; there's nothing to choose from. */
    var seen = {}, out = [];
    Array.prototype.forEach.call(form.querySelectorAll('input, select, textarea'), function (el) {
      if (el.disabled || el.type === 'button' || el.type === 'submit' || el.type === 'hidden') return;
      if (el.type === 'radio' || el.type === 'checkbox') {
        var k = el.name || el.id; if (!k || seen[k]) return; seen[k] = 1;
        var all = form.querySelectorAll('input[name="' + k + '"]'); if (!all.length) all = [el];
        var on = Array.prototype.filter.call(all, function (x) { return x.checked; });
        out.push({ k: k, type: el.type, label: labelFor(el), value: el.type === 'radio' ? (on[0] ? on[0].value : '') : on.map(function (x) { return x.value; }), text: on.map(optText).join(', '), opts: Array.prototype.map.call(all, function (x) { return { v: x.value, t: optText(x) }; }) });
      } else if (el.tagName === 'SELECT') {
        var k3 = el.id || el.name; if (!k3 || seen[k3]) return; seen[k3] = 1;
        var sel = el.selectedOptions && el.selectedOptions[0];
        out.push({ k: k3, type: 'select', label: labelFor(el), value: el.value, text: sel ? sel.text : el.value, opts: Array.prototype.map.call(el.options, function (o) { return { v: o.value, t: o.text }; }) });
      } else {
        var k2 = el.id || el.name; if (!k2 || seen[k2]) return; seen[k2] = 1;
        out.push({ k: k2, type: 'value', label: labelFor(el), value: el.value, text: el.value });
      }
    });
    return out;
  }
  function save() {
    if (restoring || isExample()) return;
    var d = load(); if (!d) return;
    d.kits = d.kits || {};
    var h1 = document.querySelector('h1');
    d.kits[kit] = { v: 1, title: (h1 ? h1.textContent : document.title).trim(), url: 'toolkits/' + location.pathname.split('/toolkits/')[1], updated: new Date().toISOString(), fields: serialize() };
    try { localStorage.setItem(KEY, JSON.stringify(d)); } catch (e) {}
  }
  function onUser(e) { if (!e.isTrusted || !form.contains(e.target)) return; clearTimeout(sT); sT = setTimeout(save, 700); }
  form.addEventListener('input', onUser, true); form.addEventListener('change', onUser, true);
  var rx = document.getElementById('restore-example');
  if (rx) rx.addEventListener('click', function () { var d = load(); if (d && d.kits && d.kits[kit]) { delete d.kits[kit]; try { localStorage.setItem(KEY, JSON.stringify(d)); } catch (e) {} } });
  /* restore: set the saved values, then fire the page's own input/change handlers so it recalculates */
  function apply(fields) {
    var changed = 0;
    fields.forEach(function (f) {
      if (f.type === 'radio') { var r = f.value && form.querySelector('input[name="' + f.k + '"][value="' + String(f.value).replace(/"/g, '') + '"]'); if (r && !r.checked) { r.checked = true; fire(r); changed++; } }
      else if (f.type === 'checkbox') { var all = form.querySelectorAll('input[name="' + f.k + '"]'); if (!all.length) { var one = document.getElementById(f.k); all = one ? [one] : []; } Array.prototype.forEach.call(all, function (x) { var want = (f.value || []).indexOf(x.value) > -1; if (x.checked !== want) { x.checked = want; fire(x); changed++; } }); }
      else { var el = document.getElementById(f.k) || form.querySelector('[name="' + f.k + '"]'); if (el && form.contains(el) && el.value !== f.value) { el.value = f.value; fire(el); changed++; } }
    });
    return changed;
  }
  function fire(el) { el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); }
  function restore() {
    var d = load(), s = d && d.kits && d.kits[kit]; if (!s || !s.fields || !s.fields.length) return;
    restoring = true;
    try { apply(s.fields); apply(s.fields); } finally { restoring = false; }   /* twice: some questions appear only after an earlier answer */
    var head = form.querySelector('.q-head'); if (!head || document.getElementById('bl-restored')) return;
    var n = document.createElement('p'); n.id = 'bl-restored'; n.setAttribute('role', 'status');
    n.style.cssText = 'margin:8px 0 0;font-size:13px;line-height:1.45;color:var(--muted,#5F6E79)';
    n.innerHTML = 'Welcome back: your saved answers are loaded. <a href="' + (location.pathname.indexOf('/toolkits/') > -1 ? '../../' : '') + 'my-profile.html" style="font-weight:700">See all your answers in My Profile</a>';
    head.appendChild(n);
  }
  if (!selfRestoring) setTimeout(restore, 0);
})();
</script>"""

def track_js():
    return TRACK_TMPL.replace('__GTM__', GTM_ID).replace('__HUB__', HUBSPOT_ID)

def rel(frm, to):
    r = os.path.relpath(os.path.join(ROOT, to), os.path.dirname(os.path.join(ROOT, frm))).replace(os.sep, '/')
    return r

# Pages that share a top tab and show their own sub-tabs under the bar.
GROUPS = {
    'profile': [('Profile, answers & progress', 'my-profile.html', 'profile-home'), ('Journey', 'your-journey.html', 'yourjourney'), ('Roadmap', 'roadmap.html', 'roadmap')],
    'assets': [('Sales deck & talk tracks', 'sales.html', 'sales'), ('Widgets & tiles', 'widgets.html', 'widgets'), ('Page mockups', 'mockups/homepage.html', 'mockups')],
}
INTERNAL_KEYS = {'journey', 'sales', 'widgets', 'mockups', 'review', 'cannibalization'}

def header(page, current, where='', prev=None, nxt=None, extra='', service=None):
    e = html.escape
    hub = rel(page, 'index.html')
    cat = rel(page, 'toolkits.html')
    items = []
    for i, (label, url, cols) in enumerate(MENU):
        dd = ''.join(
            '<div class="blh-col">' + (f'<h6>{e(h6)}</h6>' if h6 else '<h6 aria-hidden="true"></h6>') + '<ul>' +
            ''.join(f'<li><a href="{(hub if href == "HUB" else BL + href)}">{e(t)}' + (' <span class="blh-new">New</span>' if href == 'HUB' else '') + '</a></li>' for t, href in links) +
            '</ul></div>' for h6, links in cols)
        items.append(f'<li class="blh-li{" r" if i >= 3 else ""}"><button class="blh-top" type="button" aria-expanded="false">{e(label)}<span class="car" aria-hidden="true"></span></button><div class="blh-dd">{dd}</div></li>')
        if label == 'Resources':
            items.append(f'<li><a class="blh-top is-here" href="{hub}">Small Leaps <span class="blh-new">New</span></a></li>')
    SERVICES = [('RevOps', 'revops'), ('Paid Media', 'paid'), ('SEO', 'seo'), ('Digital PR', 'pr'), ('Email Marketing', 'email'), ('Strategy', 'strategy')]
    # "Toolkits" dropdown: every service group, plus All toolkits. Then the other pages as tabs, so every page is one
    # click from the bar. Client-facing pages sit on the left; internal pages are grouped on the right under "Internal".
    menu_items = [('All toolkits', 'toolkits.html#toolkits', 'toolkits')] + [(n, 'toolkits.html#' + k, k) for n, k in SERVICES]
    # One bar on every page. Client side: Start here, All toolkits (menu), My Profile (menu).
    # Internal side: Customer journey, Assets (menu), Status & review. Only the highlight changes.
    group = next((g for g, items in GROUPS.items() if any(k == current for _, _, k in items)), None)
    def tab(t_, f, key):
        # one aria-current="page" per page; the service a toolkit belongs to is marked "true" (same look)
        cur = ' aria-current="page"' if key == current else (' aria-current="true"' if key == service else '')
        return f'<a href="{rel(page, f)}" data-tab="{key}"' + cur + f'>{e(t_)}</a>'
    def dd(label, mid, items, on):
        btn = (f'<button type="button" class="blh-tbtn{" is-current" if on else ""}" data-tab="{mid}" aria-expanded="false" aria-controls="blh-{mid}menu">'
               f'{e(label)}<span class="car" aria-hidden="true"></span></button>')
        panel = (f'<div class="blh-tmenu" id="blh-{mid}menu" hidden><ul>' + ''.join('<li>' + tab(*x) + '</li>' for x in items) + '</ul></div>')
        return btn, panel
    in_menu = any(k in (current, service) for _, _, k in menu_items)
    t_btn, t_menu = dd('All toolkits', 't', menu_items, in_menu)
    p_btn, p_menu = dd('My Profile', 'p', GROUPS['profile'], group == 'profile')
    a_btn, a_menu = dd('Assets', 'a', GROUPS['assets'], group == 'assets')
    menu_html = t_menu + p_menu + a_menu
    tab_html = (tab('Start here', 'index.html', 'home') + t_btn + p_btn +
                '<span class="blh-int" role="group" aria-label="Internal pages"><span class="blh-int-l" aria-hidden="true">Internal</span>'
                + tab('Customer journey', 'journey.html', 'journey') + a_btn
                + tab('Service cannibalization', 'cannibalization.html', 'cannibalization')
                + tab('Status & review', 'review.html', 'review') + '</span>')
    internal = current in INTERNAL_KEYS
    strip = ('<div class="blh-strip" role="note">' + ('Internal page · for the Big Leap team · not shown to clients' if internal else 'Draft 1 · for internal review · not launched yet') + '</div>')
    pn = ''
    if prev is not None or nxt is not None:
        def lk(item, label, back):
            if not item:
                return f'<a href="{cat}">' + ('← ' if back else '') + f'<b>{label}</b><span>All toolkits</span>' + ('' if back else ' →') + '</a>'
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
            '</div></div>' + strip + '</header><!-- /bl-header -->')

def pager(page, prev, nxt, where):
    e = html.escape
    hub = rel(page, 'toolkits.html')
    def lk(item, label, back):
        if not item:
            return f'<a class="blp-a{" back" if back else ""}" href="{hub}"><small>{label}</small><b>All toolkits</b></a>'
        title, f = item
        return f'<a class="blp-a{" back" if back else ""}" href="{rel(page, f)}"><small>{"← " if back else ""}{label}{"" if back else " →"}</small><b>{e(title)}</b></a>'
    return ('<!-- bl-pager --><nav class="blp" aria-label="Previous and next toolkit"><div class="blp-in">'
            + lk(prev, 'Previous', True) + f'<a class="blp-hub" href="{hub}"><small>{e(where)}</small><b>All toolkits</b></a>' + lk(nxt, 'Next', False)
            + '</div></nav><!-- /bl-pager -->')

SEQ_JSON = '[]'
WHY_PAGES = {'index.html', 'your-journey.html'}

# ---------------------------------------------------------------------------------------------------
# bigleap.com alignment: a "Why Big Leap" band (hub and Your journey) and a bigleap.com-style footer
# (every page). Claims and links are only what bigleap.com itself publishes (homepage, Oct 22, 2026).
FOOT_CSS = r"""<style id="bl-footer-css">
.blw, .blf { font-family: "Open Sans", "Segoe UI", Arial, sans-serif; }
.blw { background: #fff; color: #143D55; border-top: 1px solid #D4DADF; padding: 56px 20px; }
.blw-in, .blf-in { max-width: 1120px; margin: 0 auto; }
.blw-in { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1.6fr); gap: 40px; align-items: start; }
.blw-eye { margin: 0 0 8px; color: #C5372B; font: 800 13px/1.4 "Open Sans", Arial, sans-serif; letter-spacing: .08em; text-transform: uppercase; }
.blw h2 { margin: 0 0 14px; color: #143D55; font: 800 clamp(26px, 3.2vw, 36px)/1.15 "Raleway", "Segoe UI", Arial, sans-serif; }
.blw-lede { margin: 0 0 22px; color: #2D4556; font-size: 16px; line-height: 1.6; }
.blw-stats { display: flex; flex-wrap: wrap; gap: 22px; margin: 0 0 24px; padding: 0; list-style: none; }
.blw-stats b { display: block; color: #143D55; font: 800 30px/1.1 "Raleway", "Segoe UI", Arial, sans-serif; }
.blw-stats span { color: #5F6E79; font-size: 13px; }
.blw-btn { display: inline-flex; align-items: center; gap: 8px; min-height: 44px; padding: 10px 22px; border-radius: 25px; background: #EA4335; color: #fff !important; font: 700 15px "Raleway", "Segoe UI", Arial, sans-serif; text-decoration: none; }
.blw-btn:hover, .blw-btn:focus-visible { background: #C5372B; }
.blw-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 26px 30px; margin: 0; padding: 0; list-style: none; }
.blw-grid li { display: grid; grid-template-columns: 48px 1fr; gap: 14px; align-items: start; }
.blw-ic { display: grid; place-items: center; width: 48px; height: 48px; border-radius: 50%; background: #EEF3F8; color: #143D55; }
.blw-grid h3 { margin: 2px 0 4px; color: #143D55; font: 800 17px/1.3 "Raleway", "Segoe UI", Arial, sans-serif; }
.blw-grid p { margin: 0; color: #2D4556; font-size: 14.5px; line-height: 1.55; }
.blf { background: #0F1D26; color: #DCE9F2; padding: 48px 20px 28px; }
.blf a { color: #DCE9F2; text-decoration: none; }
.blf a:hover, .blf a:focus-visible { color: #fff; text-decoration: underline; }
.blf-top { display: grid; grid-template-columns: 1.2fr repeat(3, minmax(0, 1fr)) 1.25fr; gap: 28px; }
.blf-logo img { height: 36px; width: auto; filter: brightness(0) invert(1); }
.blf-tag { margin: 14px 0 0; max-width: 280px; color: #B9C7D2; font-size: 14px; line-height: 1.55; }
.blf h2 { margin: 0 0 12px; color: #fff; font: 800 15px/1.3 "Raleway", "Segoe UI", Arial, sans-serif; letter-spacing: .02em; }
.blf ul { margin: 0; padding: 0; list-style: none; display: grid; gap: 8px; font-size: 14px; }
.blf address { font-style: normal; font-size: 14px; line-height: 1.6; color: #B9C7D2; }
.blf-cta { display: inline-flex; margin-top: 14px; min-height: 40px; align-items: center; padding: 8px 16px; border-radius: 25px; background: #EA4335; color: #fff !important; font: 700 14px "Raleway", "Segoe UI", Arial, sans-serif; white-space: nowrap; }
.blf-cta:hover, .blf-cta:focus-visible { background: #C5372B; text-decoration: none !important; }
.blf-bot { display: flex; flex-wrap: wrap; gap: 12px 24px; justify-content: space-between; align-items: center; margin-top: 36px; padding-top: 20px; border-top: 1px solid #22394A; font-size: 13px; color: #B9C7D2; }
.blf .blf-soc { display: flex; grid-auto-flow: column; gap: 10px; margin: 0; padding: 0; list-style: none; }
.blf-soc a { display: grid; place-items: center; width: 36px; height: 36px; border-radius: 50%; background: #22394A; }
.blf-soc a:hover, .blf-soc a:focus-visible { background: #3187B5; }
.blf-legal { display: flex; flex-wrap: wrap; gap: 6px 16px; }
@media (max-width: 1000px) { .blf-top { grid-template-columns: repeat(2, minmax(0, 1fr)); } .blf-brand { grid-column: 1 / -1; } }
@media (max-width: 860px) { .blw-in { grid-template-columns: 1fr; gap: 28px; } }
@media (max-width: 560px) { .blw { padding: 40px 16px; } .blw-grid { grid-template-columns: 1fr; } .blf { padding: 36px 16px 24px; } .blf-top { grid-template-columns: 1fr; gap: 24px; } }
@media print { .blw, .blf { display: none !important; } }
</style>"""

def _ic(d):
    return f'<span class="blw-ic" aria-hidden="true"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{d}</svg></span>'

WHY_ITEMS = [
    ('Strategy First', 'We start with strategy, not a pitch, making sure we’re the right partner for your goals.', '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>'),
    ('Brand-Led Performance', 'Your brand fuels your funnel. We build performance campaigns that align and scale.', '<path d="M3 11v2a1 1 0 0 0 1 1h2l5 4V6L6 10H4a1 1 0 0 0-1 1z"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/><path d="M18.5 5.5a9 9 0 0 1 0 13"/>'),
    ('AI SEO', 'Stay front and center in AI-driven search results and channels before competitors do.', '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m20 20-4.8-4.8"/><path d="M10.5 7.5v6M7.5 10.5h6"/>'),
    ('RevOps Alignment', 'Connect marketing to revenue to bridge the gap and drive measurable impact.', '<path d="M4 12a8 8 0 0 1 14-5.3"/><path d="M18 3v4h-4"/><path d="M20 12a8 8 0 0 1-14 5.3"/><path d="M6 21v-4h4"/>'),
    ('Full Ownership', 'Maintain access to tools, data, and results. No black boxes. No locked-in platforms.', '<circle cx="8" cy="15" r="4"/><path d="m11 12 9-9"/><path d="m17 6 3 3"/><path d="m15 8 2 2"/>'),
    ('95.3% Client Retention', '17+ years of staying ahead, so our clients never fall behind.', '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>'),
]

def why_block(page):
    e = html.escape
    items = ''.join(f'<li>{_ic(d)}<div><h3>{e(t)}</h3><p>{e(p)}</p></div></li>' for t, p, d in WHY_ITEMS)
    return ('<!-- bl-why --><section class="blw" aria-labelledby="blw-h"><div class="blw-in"><div>'
            '<p class="blw-eye">Why Big Leap</p>'
            '<h2 id="blw-h">A Growth Partner That Gets It, and Gets It Done</h2>'
            '<p class="blw-lede">The DIY toolkits are written by the same team that runs these programs for our clients. Big Leap combines brand and performance marketing to deliver clarity and consistency.</p>'
            '<ul class="blw-stats"><li><b>17+</b><span>years in digital marketing</span></li><li><b>4.8</b><span>average rating, 150+ verified reviews</span></li></ul>'
            f'<a class="blw-btn" href="{BL}/about-us/">Learn more about us <span aria-hidden="true">→</span></a>'
            f'</div><ul class="blw-grid">{items}</ul></div></section><!-- /bl-why -->')

SOCIAL = [
    ('Facebook', 'https://www.facebook.com/bigleapmktg/', '<path d="M14 8h3V4h-3a4 4 0 0 0-4 4v3H7v4h3v6h4v-6h3l1-4h-4V8z"/>'),
    ('X', 'https://x.com/BigLeapMKTG/', '<path d="M4 4l16 16M20 4 4 20"/>'),
    ('YouTube', 'https://www.youtube.com/@bigleapmarketing', '<rect x="3" y="6" width="18" height="12" rx="3"/><path d="m10 9 5 3-5 3z"/>'),
    ('Instagram', 'https://www.instagram.com/bigleapmktg/', '<rect x="4" y="4" width="16" height="16" rx="4"/><circle cx="12" cy="12" r="3.5"/><path d="M16.5 7.5h.01"/>'),
    ('LinkedIn', 'https://www.linkedin.com/company/bigleap/', '<rect x="4" y="9" width="3" height="11"/><circle cx="5.5" cy="5.5" r="1.5"/><path d="M11 20v-6a3 3 0 0 1 6 0v6M11 9v11"/>'),
]

THEME_BTN = '<button class="blh-theme" id="theme" type="button" aria-label="Switch light or dark mode" title="Light or dark mode"><svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 3a9 9 0 0 0 0 18z" fill="currentColor"/></svg></button>'

def site_footer(page, theme=False):
    e = html.escape
    r = lambda f: rel(page, f)
    col = lambda h, links: f'<div><h2>{e(h)}</h2><ul>' + ''.join(f'<li><a href="{u}">{e(t)}</a></li>' for t, u in links) + '</ul></div>'
    diy = col('DIY Toolkits', [('Start here', r('index.html')), ('All toolkits', r('toolkits.html')), ('My Profile', r('my-profile.html')), ('Your journey', r('your-journey.html')), ('Roadmap', r('roadmap.html'))])
    svc = col('Services', [('SEO Marketing', BL + '/services/seo-marketing/'), ('Paid Advertising', BL + '/services/paid-advertising/'), ('RevOps', BL + '/services/revops-agency/'), ('Content Marketing', BL + '/services/content-marketing/'), ('CRO Marketing', BL + '/services/cro-marketing/')])
    co = col('Company', [('About', BL + '/about-us/'), ('Areas Served', BL + '/areas-served/'), ('Blog', BL + '/blog/'), ('Case Studies', BL + '/digital-marketing-seo-case-studies/'), ('About Sweet Takes Podcast', BL + '/sweet-story/')])
    contact = ('<div><h2>Contact</h2><address><a href="tel:+18014363003">(801) 436-3003</a><br>4101 N Thanksgiving Way, Suite 175<br>Lehi, Utah 84043</address>'
               f'<a class="blf-cta" href="{BL}/get-started/?utm_source=diy-toolkits&amp;utm_medium=site-footer">Get Your Custom Strategy</a></div>')
    soc = '<ul class="blf-soc">' + ''.join(f'<li><a href="{u}" aria-label="Big Leap on {e(n)}" rel="noopener"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{d}</svg></a></li>' for n, u, d in SOCIAL) + '</ul>'
    return ('<!-- bl-footer --><footer class="blf" aria-label="Big Leap"><div class="blf-in"><div class="blf-top">'
            f'<div class="blf-brand"><a class="blf-logo" href="{BL}/" aria-label="Big Leap home"><img src="{r("assets/bigleap-logo.png")}" alt="Big Leap" width="110" height="36" loading="lazy"></a>'
            '<p class="blf-tag">Brand-led performance marketing. Free DIY toolkits for the small leaps; our team for the Big Leap.</p></div>'
            f'{diy}{svc}{co}{contact}</div>'
            f'<div class="blf-bot">{soc}<div class="blf-legal">' + (THEME_BTN if theme else '') + f'<a href="{BL}/privacy-policy/">Privacy Policy</a><a href="{BL}/terms-of-use/">Terms of Use</a><span>© 2026 Big Leap, All Rights Reserved</span></div></div>'
            '</div></footer><!-- /bl-footer -->')

def apply(page, block, before_selector=None, bottom='', theme=False):
    p = os.path.join(ROOT, page)
    s = open(p, encoding='utf-8').read()
    # strip old versions (this header + the earlier bl-sitenav bar)
    s = re.sub(r'<!-- bl-header -->.*?<!-- /bl-header -->\n?', '', s, flags=re.S)
    s = re.sub(r'<!-- bl-sitenav -->.*?<!-- /bl-sitenav -->\n?', '', s, flags=re.S)
    s = re.sub(r'<style id="bl-(?:sitenav|header|footer)-css">.*?</style>\n?', '', s, flags=re.S)
    s = re.sub(r'<!-- bl-(why|footer) -->.*?<!-- /bl-\1 -->\n?', '', s, flags=re.S)
    s = re.sub(r'<script id="bl-header-js">.*?</script>\n?', '', s, flags=re.S)
    s = re.sub(r'<!-- bl-pager -->.*?<!-- /bl-pager -->\n?', '', s, flags=re.S)
    s = re.sub(r'<script id="bl-track-js">.*?</script>\n?', '', s, flags=re.S)
    s = re.sub(r'<script id="bl-try-js">.*?</script>\n?', '', s, flags=re.S)
    s = re.sub(r'<script id="bl-owner-js">.*?</script>\n?', '', s, flags=re.S)
    s = re.sub(r'<script id="bl-answers-js">.*?</script>\n?', '', s, flags=re.S)
    s = re.sub(r'<script id="bl-version-js"[^>]*></script>\n?', '', s)   # removes the retired version switch
    fonts = rel(page, 'assets/fonts/fonts.css')
    if 'fonts.css' not in s:
        s = s.replace('</head>', f'<link rel="stylesheet" href="{fonts}">\n</head>', 1)
    s = s.replace('</head>', CSS + '\n' + FOOT_CSS + '\n' + track_js() + '\n</head>', 1)
    if page in WHY_PAGES:
        i = s.rfind('<footer class="foot"')
        s = (s[:i] + why_block(page) + '\n' + s[i:]) if i >= 0 else s.replace('</body>', why_block(page) + '\n</body>', 1)
    s = re.sub(r'(<body[^>]*>)', lambda m: m.group(1) + '\n' + block, s, count=1)
    s = s.replace('</body>', (bottom + '\n' if bottom else '') + site_footer(page, theme) + '\n' + JS.replace('__SEQ__', SEQ_JSON) + '\n' + TRY_JS + '\n</body>', 1)
    open(p, 'w', encoding='utf-8').write(s)

if __name__ == '__main__':
    import sys
    only_pages = 'pages-only' in sys.argv
    d = json.load(open(os.path.join(ROOT, 'toolkits.json')))
    PEOPLE = json.load(open(os.path.join(ROOT, 'data', 'widgets.json'))).get('people', {})
    ORDER = [x for x in ['paid', 'revops', 'seo', 'pr', 'email', 'strategy'] if x in {s['id'] for s in d['series']}]           # series order after the universal Business Profile step below
    by = {s['id']: s for s in d['series']}
    # The Business Profile ("start" in toolkits.json) is a universal first step ahead of every series,
    # not owned by one of them - inject it as a synthetic series/toolkit pair so it gets the normal
    # header/pager treatment as seq[0], instead of being listed as a numbered Paid Media toolkit.
    START_SERIES = {'id': 'start', 'name': 'Start here', 'owner': 'Scott Smoot'}
    START_TOOLKIT = {'n': 0, 'title': d['start']['title'], 'file': d['start']['file']}
    seq = [(START_SERIES, START_TOOLKIT)] + [(by[sid], t) for sid in ORDER for t in by[sid]['toolkits']]
    SEQ_JSON = json.dumps([t['file'] for _, t in seq])
    for i, (s, t) in enumerate(seq if not only_pages else []):
        prev = seq[i - 1] if i else None
        nxt = seq[i + 1] if i + 1 < len(seq) else None
        fmt = lambda it: None if not it else ((it[1]['title'] if it[0]['id'] == s['id'] else f"{it[0]['name']}: {it[1]['title']}"), it[1]['file'])
        cur = 'toolkit'
        where = 'Business Profile · Before any toolkit' if s is START_SERIES else f"{s['name']} · Toolkit {t['n']} of {len(s['toolkits'])}"
        apply(t['file'], header(t['file'], cur, '', None, None, '', s['id']),
              bottom=pager(t['file'], fmt(prev), fmt(nxt), where) + '\n' + owner_js(t['file'], s['owner'], PEOPLE) + '\n' + ANSWERS_JS)
        print('toolkit', t['file'])
    theme = '<button class="blh-theme" id="theme" type="button" aria-label="Switch light or dark mode" title="Light or dark mode"><svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 3a9 9 0 0 0 0 18z" fill="currentColor"/></svg></button>'
    # Start here: the landing page (the site's front door). All toolkits: the catalog.
    apply('index.html', header('index.html', 'home', '', None, None, ''))
    apply('toolkits.html', header('toolkits.html', 'toolkits', '', None, None, ''), theme=True)
    # Assets (internal): widgets and slide tiles; shares sub-tabs with the sales deck and mockups.
    apply('widgets.html', header('widgets.html', 'widgets', '', None, None, ''), theme=True)
    apply('journey.html', header('journey.html', 'journey', '', None, None, ''))
    # Service cannibalization: moved out of journey.html's own tabs into its own page, so the case
    # against cannibalizing a service line's book is a first-class, easy-to-find internal destination.
    if os.path.exists(os.path.join(ROOT, 'cannibalization.html')):
        apply('cannibalization.html', header('cannibalization.html', 'cannibalization', '', None, None, ''))
    # My Profile: the Business Profile, every toolkit's saved answers, and the visitor's progress, in one place.
    if os.path.exists(os.path.join(ROOT, 'my-profile.html')):
        apply('my-profile.html', header('my-profile.html', 'profile-home', '', None, None, ''))
    # Your journey: the client-facing journey map (the visitor's own path). journey.html is the internal map.
    if os.path.exists(os.path.join(ROOT, 'your-journey.html')):
        apply('your-journey.html', header('your-journey.html', 'yourjourney', '', None, None, ''))
    apply('mockups/homepage.html', header('mockups/homepage.html', 'mockups', '', None, None, ''))
    # Internal Team Review page (not linked from toolkit content, only from the toolkit bar).
    if os.path.exists(os.path.join(ROOT, 'review.html')):
        apply('review.html', header('review.html', 'review', '', None, None, ''), theme=True)
    # Sales assets: the live-call deck, per-service options and talk tracks. Internal; tab only.
    if os.path.exists(os.path.join(ROOT, 'sales.html')):
        apply('sales.html', header('sales.html', 'sales', '', None, None, ''))
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
    print('index.html, journey.html, cannibalization.html, review.html, sales.html')
