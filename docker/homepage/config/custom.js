// Falling cherry-blossom petals + a live subtitle under the greeting.
(function () {
  'use strict';

  /* ---------- 1. petals (skipped when the user prefers reduced motion) ---------- */
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!reduce && !document.getElementById('blossom-petals')) {
    var css = document.createElement('style');
    css.textContent =
      '#blossom-petals{position:fixed;inset:0;pointer-events:none;z-index:0;overflow:hidden}' +
      '#blossom-petals i{position:absolute;top:-24px;width:12px;height:8px;display:block;' +
      'border-radius:60% 60% 60% 60%/70% 70% 40% 40%;background:#f9a8c4;opacity:.45;' +
      'animation:blossomFall linear infinite}' +
      '@keyframes blossomFall{0%{transform:translate3d(0,-40px,0) rotate(0)}' +
      '50%{transform:translate3d(-30px,50vh,0) rotate(200deg)}' +
      '100%{transform:translate3d(60px,105vh,0) rotate(420deg)}}';
    document.head.appendChild(css);

    var host = document.createElement('div');
    host.id = 'blossom-petals';
    var n = window.innerWidth < 820 ? 9 : 16;
    for (var i = 0; i < n; i++) {
      var p = document.createElement('i');
      p.style.left = (Math.random() * 100) + 'vw';
      p.style.animationDuration = (12 + Math.random() * 14).toFixed(1) + 's';
      p.style.animationDelay = (-Math.random() * 24).toFixed(1) + 's';
      p.style.transform = 'scale(' + (0.55 + Math.random() * 0.9).toFixed(2) + ')';
      p.style.opacity = (0.22 + Math.random() * 0.4).toFixed(2);
      host.appendChild(p);
    }
    document.body.appendChild(host);
  }

  /* ---------- 2. subtitle: "server · 14 containers · up 10d 2h" ---------- */
  function fmtUptime(hours) {
    if (hours === undefined || hours === null) return '';
    var d = Math.floor(hours / 24);
    var h = Math.floor(hours % 24);
    return d > 0 ? d + 'd ' + h + 'h' : h + 'h';
  }

  function ensureSub() {
    var greet = document.querySelector('.information-widget-greeting');
    if (!greet) return null;
    var sub = greet.querySelector('.hp-sub');
    if (!sub) {
      sub = document.createElement('div');
      sub.className = 'hp-sub';
      greet.appendChild(sub);
    }
    return sub;
  }

  function paint() {
    var sub = ensureSub();
    if (!sub) return;
    fetch('/deepseek.json', { cache: 'no-store' })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        var bits = [];
        bits.push(d.host || 'server');
        if (typeof d.containers === 'number') {
          bits.push(d.containers + ' container' + (d.containers === 1 ? '' : 's'));
        }
        var up = fmtUptime(d.uptime_hours);
        if (up) bits.push('up ' + up);
        sub.textContent = bits.join('  ·  ');
      })
      .catch(function () { /* keep whatever was there */ });
  }

  var tries = 0;
  var timer = setInterval(function () {
    if (ensureSub()) { clearInterval(timer); paint(); }
    else if (++tries > 40) clearInterval(timer);
  }, 250);
  setInterval(paint, 60000);
})();
