/* Copied from ../index.html by _build/build.py. Edit index.html, then rebuild. */
(function () {
  var d = document, html = d.documentElement;
  var FPS = 24;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');

  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function docTop(el) { return el.getBoundingClientRect().top + window.scrollY; }

  /* ----- timecode: the viewer's local time of day, HH:MM:SS:FF at 24 frames a second -----
     Two slots exist (header, and the hero slate row); CSS shows exactly one. A timer wakes just past
     each frame boundary and stops while no slot is on screen. With reduced motion it ticks once a
     second, on the second, so the frames read 00. Either slot pauses and restarts it (WCAG 2.2.2).
     The motion preference is cached here: reading reduce.matches every frame stops Chrome firing
     its change event, which applyMotionPref relies on. */
  var slots = [].slice.call(d.querySelectorAll('[data-clock]'));
  var clocks = slots.map(function (sl) { return sl.querySelector('.tc-val'); });
  var FRAME_MS = 1000 / FPS, lastTC = '', clockTimer = 0, reduced = reduce.matches, paused = false;
  var onScreen = slots.map(function () { return true; });
  function paintClock() {
    var now = new Date();
    var f = reduced ? 0 : Math.floor(now.getMilliseconds() * FPS / 1000);
    var t = pad(now.getHours()) + ':' + pad(now.getMinutes()) + ':' + pad(now.getSeconds()) + ':' + pad(f);
    if (t !== lastTC) {
      lastTC = t;
      clocks.forEach(function (c) { c.textContent = t; c.parentNode.classList.add('on'); });
    }
    return now;
  }
  function tick() {
    clockTimer = 0;
    if (paused || onScreen.indexOf(true) < 0) return;
    var ms = paintClock().getMilliseconds();
    clockTimer = setTimeout(tick, (reduced ? 1000 - ms : FRAME_MS - ms % FRAME_MS) + 2);
  }
  function startClock() { clearTimeout(clockTimer); reduced = reduce.matches; tick(); }
  if ('IntersectionObserver' in window) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { onScreen[slots.indexOf(en.target)] = en.isIntersecting; });
      if (!clockTimer) tick();
    });
    slots.forEach(function (sl) { cio.observe(sl); });
  }
  d.addEventListener('visibilitychange', function () { if (!d.hidden) startClock(); });
  slots.forEach(function (sl) {
    sl.addEventListener('click', function () {
      paused = !paused;
      slots.forEach(function (o) { o.setAttribute('aria-pressed', paused ? 'true' : 'false'); });
      if (paused) clearTimeout(clockTimer); else startClock();
    });
  });

  /* ----- scenes: sticky stage, bars close between shots, credits swap under the matte ----- */
  var scenes = [].slice.call(d.querySelectorAll('.scene[data-shots]')).map(function (s) {
    return { el: s, stage: s.querySelector('.stage'), shots: [].slice.call(s.querySelectorAll('.shot')), n: +s.getAttribute('data-shots'), shotLabel: s.querySelector('.sl-shot'), idx: 0 };
  });
  function setShot(sc, i) {
    if (sc.idx === i) return;
    sc.idx = i;
    sc.shots.forEach(function (sh, k) { sh.classList.toggle('is-on', k === i); });
    if (sc.shotLabel) sc.shotLabel.textContent = 'Shot ' + (i + 1) + '/' + sc.n;
  }
  function smooth(x) { return x * x * (3 - 2 * x); }
  var WIN = 0.17; // half-width of the matte wipe, in shots
  function updateScenes() {
    var vh = window.innerHeight;
    scenes.forEach(function (sc) {
      var r = sc.el.getBoundingClientRect();
      if (r.bottom < -vh || r.top > vh * 1.5) return;
      var total = Math.max(1, r.height - sc.stage.offsetHeight);
      var p = Math.min(1, Math.max(0, -r.top / total));
      var pos = p * sc.n;
      var i = Math.min(sc.n - 1, Math.floor(pos));
      var close = 0;
      for (var k = 1; k < sc.n; k++) { var dist = Math.abs(pos - k); if (dist < WIN) close = Math.max(close, 1 - dist / WIN); }
      var st = sc.stage.style;
      st.setProperty('--p', p.toFixed(4));
      st.setProperty('--close', smooth(close).toFixed(4));
      st.setProperty('--push', Math.min(1, Math.max(0, pos - i)).toFixed(4));
      setShot(sc, i);
    });
  }
  function clearScenes() {
    scenes.forEach(function (sc) {
      ['--p', '--close', '--push'].forEach(function (v) { sc.stage.style.removeProperty(v); });
      sc.idx = -1; setShot(sc, 0);
    });
  }
  // Keyboard: focus inside a scene always parks the scroll at the middle of that shot, where the
  // matte is open and the credit is fully visible. The scroll waits a frame so it lands after the
  // browser's own scroll-into-view for the focused button, which would otherwise win.
  d.addEventListener('focusin', function (e) {
    if (!html.classList.contains('seq')) return;
    var shot = e.target.closest && e.target.closest('.scene .shot');
    if (!shot) return;
    var sc = scenes.filter(function (s) { return s.el.contains(shot); })[0];
    if (!sc) return;
    // Mouse clicks on Play also focus the button; only keyboard focus should move the page.
    try { if (!e.target.matches(':focus-visible')) return; } catch (err) {}
    var i = sc.shots.indexOf(shot);
    requestAnimationFrame(function () {
      var total = sc.el.offsetHeight - sc.stage.offsetHeight;
      window.scrollTo(0, docTop(sc.el) + total * ((i + 0.5) / sc.n));
    });
  });

  var ticking = false;
  function frame() {
    ticking = false;
    if (html.classList.contains('seq')) updateScenes();
  }
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  window.addEventListener('load', onScroll);

  function applyMotionPref() {
    html.classList.toggle('seq', !reduce.matches);
    if (reduce.matches) clearScenes();
    startClock(); onScroll();
  }
  if (reduce.addEventListener) reduce.addEventListener('change', applyMotionPref);

  /* ----- scenes get .entered once their stage is on screen, so the first credits arrive in sequence ----- */
  if ('IntersectionObserver' in window) {
    var sio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('entered'); sio.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -88% 0px', threshold: 0 });
    scenes.forEach(function (sc) { sio.observe(sc.el); });
  } else { scenes.forEach(function (sc) { sc.el.classList.add('entered'); }); }

  /* ----- reveal headings once as they enter (motion only) ----- */
  var rv = [].slice.call(d.querySelectorAll('.rv, .mt'));
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.1 });
    rv.forEach(function (el) { io.observe(el); });
  } else { rv.forEach(function (el) { el.classList.add('in'); }); }

  /* ----- films: the monitor shows the still for the hovered or focused title ----- */
  var films = [].slice.call(d.querySelectorAll('.film'));
  var monItems = [].slice.call(d.querySelectorAll('.mon-frame > *'));
  function monitor(li) {
    var i = +li.getAttribute('data-i');
    monItems.forEach(function (m, k) { m.classList.toggle('on', k === i); });
    films.forEach(function (f) { f.classList.toggle('is-mon', f === li); });
  }
  films.forEach(function (li) {
    li.addEventListener('mouseenter', function () { monitor(li); });
    li.addEventListener('focusin', function () { monitor(li); });
  });

  /* ----- video player: native modal dialog ----- */
  var player = d.getElementById('player'), box = player.querySelector('.player-frame'), ttl = d.getElementById('player-title'), opener = null;
  function openVideo(btn) {
    var v = btn.getAttribute('data-vimeo'), y = btn.getAttribute('data-youtube');
    var src = v ? 'https://player.vimeo.com/video/' + v + (v.indexOf('?') < 0 ? '?' : '&') + 'autoplay=1&dnt=1' : 'https://www.youtube-nocookie.com/embed/' + y + '?autoplay=1&rel=0';
    var title = btn.getAttribute('data-title') || 'Video';
    ttl.textContent = title;
    var f = d.createElement('iframe');
    f.src = src; f.title = title; f.allow = 'autoplay; fullscreen; picture-in-picture'; f.setAttribute('allowfullscreen', '');
    box.replaceChildren(f);
    opener = btn;
    player.showModal();
    player.querySelector('.player-close').focus();
  }
  d.addEventListener('click', function (e) {
    var fp = e.target.closest('.frame-play');
    if (fp) { var real = d.getElementById(fp.getAttribute('data-for')); if (real) openVideo(real); return; }
    var b = e.target.closest('[data-vimeo], [data-youtube]');
    if (b) { e.preventDefault(); openVideo(b); }
  });
  player.querySelector('.player-close').addEventListener('click', function () { player.close(); });
  player.addEventListener('click', function (e) { if (e.target === player) player.close(); });
  player.addEventListener('close', function () {
    box.replaceChildren();
    if (opener) { opener.focus({ preventScroll: true }); opener = null; }
  });

  /* ----- Services dropdown: click or hover opens it; Escape, a click outside or tabbing away closes it ----- */
  var dd = d.querySelector('.dd'), ddBtn = dd && dd.querySelector('.dd-btn'), ddTimer = 0, ddHoverAt = 0;
  function setDD(open) { dd.classList.toggle('open', open); ddBtn.setAttribute('aria-expanded', open ? 'true' : 'false'); }
  if (dd) {
    ddBtn.addEventListener('click', function () {
      // A click right after hover opened the panel keeps it open instead of closing it again.
      if (dd.classList.contains('open') && Date.now() - ddHoverAt < 500) return;
      setDD(!dd.classList.contains('open'));
    });
    dd.addEventListener('mouseenter', function () { clearTimeout(ddTimer); if (!dd.classList.contains('open')) { ddHoverAt = Date.now(); setDD(true); } });
    dd.addEventListener('mouseleave', function () { ddTimer = setTimeout(function () { if (!dd.contains(d.activeElement) || d.activeElement === ddBtn) setDD(false); }, 180); });
    dd.addEventListener('keydown', function (e) { if (e.key === 'Escape' && dd.classList.contains('open')) { setDD(false); ddBtn.focus(); } });
    dd.addEventListener('focusout', function (e) { if (!dd.contains(e.relatedTarget)) setDD(false); });
    d.addEventListener('click', function (e) { if (!dd.contains(e.target)) setDD(false); });
  }

  /* ----- mobile menu: native modal dialog ----- */
  var menu = d.getElementById('menu'), menuBtn = d.querySelector('.menu-btn'), menuNav = false;
  menuBtn.addEventListener('click', function () { menu.showModal(); menuBtn.setAttribute('aria-expanded', 'true'); });
  menu.querySelector('.menu-close').addEventListener('click', function () { menu.close(); });
  menu.addEventListener('click', function (e) { if (e.target.closest('a')) { menuNav = true; menu.close(); } });
  menu.addEventListener('close', function () {
    menuBtn.setAttribute('aria-expanded', 'false');
    if (!menuNav) menuBtn.focus();
    menuNav = false;
  });

  startClock();
  frame();
})();
