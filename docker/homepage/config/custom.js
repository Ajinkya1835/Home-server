// Falling cherry-blossom petals for the daylight theme.
// Injected as plain divs so no markup change is needed; CSS handles the motion.
(function () {
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  if (document.getElementById('blossom-petals')) return;

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
})();
