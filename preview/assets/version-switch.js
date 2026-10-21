/* Big Leap DIY Toolkits: version switch.
   One GitHub Pages site serves up to three versions of the toolkits:
     /            Original (the version on main)
     /preview/    Updated, in review (published from the working branch)
     /final/      Final, approved (published from the final branch)
   This script works out which version it is running in from its own address, shows a slim switch at
   the top of the page, and opens the same page in the other version. If that page doesn't exist
   there (for example a new page), it opens that version's hub instead. Which versions are published
   comes from versions.json at the site root (tools/publish_version.sh keeps it current). The switch
   hides itself when only one version is listed (e.g. a local preview of a branch).
   No data is stored or sent. Same file in every version. */
(function () {
  'use strict';
  var s = document.currentScript; if (!s || !window.fetch) return;
  var VERSIONS = [
    { id: 'original', prefix: '', label: 'Original' },
    { id: 'updated', prefix: 'preview/', label: 'Updated · in review' },
    { id: 'final', prefix: 'final/', label: 'Final · approved' }
  ];
  var root = s.src.replace(/assets\/version-switch\.js(?:[?#].*)?$/, '');          // this version's root URL
  var me = VERSIONS[0];
  VERSIONS.forEach(function (v) { if (v.prefix && root.slice(-v.prefix.length) === v.prefix) me = v; });
  var base = root.slice(0, root.length - me.prefix.length);                          // the site's root URL
  var here = location.href.indexOf(root) === 0 ? location.href.slice(root.length) : 'index.html';
  var path = here.split('#')[0].split('?')[0] || 'index.html', hash = here.indexOf('#') > -1 ? here.slice(here.indexOf('#')) : '';
  // pages that moved between versions
  function mapFor(v) {
    if (v.id === 'original' && path === 'review.html') return 'index.html#review';
    if (v.id !== 'original' && path === 'index.html' && /^#(review|open-items|team-review)$/.test(hash)) return 'review.html' + (hash === '#open-items' ? '#open-items' : '');
    return path + hash;
  }
  function exists(url) { return fetch(url.split('#')[0], { method: 'HEAD', cache: 'no-store' }).then(function (r) { return r.ok; }, function () { return false; }); }
  function go(v) {
    var target = base + v.prefix + mapFor(v);
    exists(target).then(function (ok) { location.href = ok ? target : base + v.prefix + 'index.html'; });
  }
  fetch(base + 'versions.json', { cache: 'no-store' }).then(function (r) { return r.ok ? r.json() : null; }, function () { return null; }).then(function (cfg) {
    var pub = (cfg && cfg.published) || [];
    var live = VERSIONS.filter(function (v) { return v === me || pub.indexOf(v.id) > -1; });
    if (live.length < 2) return;
    var css = document.createElement('style');
    css.textContent = '.blv{font:600 13px/1.3 "Open Sans","Segoe UI",Arial,sans-serif;background:#FFF4E2;color:#5A3B05;border-bottom:1px solid #E9C98A;padding:6px max(16px,env(safe-area-inset-left));display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:6px 10px;position:relative;z-index:70}' +
      '.blv span{white-space:nowrap}.blv-seg{display:inline-flex;border:1px solid #C9A25C;border-radius:999px;overflow:hidden;background:#fff}' +
      '.blv-seg button{font:inherit;border:0;background:transparent;color:#5A3B05;padding:5px 12px;min-height:32px;cursor:pointer}' +
      '.blv-seg button+button{border-left:1px solid #C9A25C}.blv-seg button[aria-current="true"]{background:#5A3B05;color:#fff;cursor:default}' +
      '.blv-seg button:focus-visible{outline:3px solid #3187B5;outline-offset:-3px}@media print{.blv{display:none}}';
    document.head.appendChild(css);
    var bar = document.createElement('div');
    bar.className = 'blv'; bar.setAttribute('role', 'navigation'); bar.setAttribute('aria-label', 'Site version');
    bar.innerHTML = '<span>Review mode · you’re viewing</span><span class="blv-seg">' + live.map(function (v) {
      return '<button type="button" data-v="' + v.id + '"' + (v === me ? ' aria-current="true"' : '') + '>' + v.label + '</button>';
    }).join('') + '</span>';
    bar.addEventListener('click', function (e) {
      var b = e.target.closest && e.target.closest('button[data-v]'); if (!b || b.getAttribute('aria-current')) return;
      var v = VERSIONS.filter(function (x) { return x.id === b.getAttribute('data-v'); })[0];
      try { if (window.blTrack) window.blTrack('diy_version_switch', { label: v.id }); } catch (err) {}
      go(v);
    });
    document.body.insertBefore(bar, document.body.firstChild);
  });
})();
