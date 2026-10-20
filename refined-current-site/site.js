/* MindInMotion, refined current site (review copy). Plain JavaScript, no framework. */
(function () {
  'use strict';
  var d = document;
  var reduce = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : { matches: false };
  d.documentElement.classList.add('js');

  /* ----- header: solid once the page scrolls past the top (home hero only) ----- */
  var hdr = d.querySelector('.hdr');
  if (hdr && hdr.classList.contains('over')) {
    var onScroll = function () { hdr.classList.toggle('scrolled', window.scrollY > 24); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ----- services dropdown ----- */
  d.querySelectorAll('.dd-btn').forEach(function (btn) {
    var menu = d.getElementById(btn.getAttribute('aria-controls'));
    function set(open) { btn.setAttribute('aria-expanded', open ? 'true' : 'false'); menu.classList.toggle('open', open); }
    btn.addEventListener('click', function (e) { e.stopPropagation(); set(btn.getAttribute('aria-expanded') !== 'true'); });
    d.addEventListener('click', function (e) { if (!menu.contains(e.target)) set(false); });
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape' && btn.getAttribute('aria-expanded') === 'true') { set(false); btn.focus(); } });
    menu.addEventListener('focusout', function (e) { if (!menu.contains(e.relatedTarget) && e.relatedTarget !== btn) set(false); });
  });

  /* ----- mobile menu ----- */
  var mnav = d.getElementById('mnav');
  var mbtn = d.querySelector('.menu-btn');
  if (mnav && mbtn) {
    var mclose = mnav.querySelector('.mnav-close');
    var openMenu = function () { mnav.classList.add('open'); mbtn.setAttribute('aria-expanded', 'true'); d.body.style.overflow = 'hidden'; mclose.focus(); };
    var closeMenu = function () { mnav.classList.remove('open'); mbtn.setAttribute('aria-expanded', 'false'); d.body.style.overflow = ''; mbtn.focus(); };
    mbtn.addEventListener('click', openMenu);
    mclose.addEventListener('click', closeMenu);
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape' && mnav.classList.contains('open')) closeMenu(); });
    mnav.addEventListener('keydown', function (e) {
      if (e.key !== 'Tab') return;
      var f = mnav.querySelectorAll('a, button');
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && d.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && d.activeElement === last) { e.preventDefault(); first.focus(); }
    });
  }

  /* ----- home hero: background reel starts only when motion is fine ----- */
  /* (the service banners use the same thing once they have a reel) */
  d.querySelectorAll('.hero-media[data-bg]').forEach(function (heroMedia) {
  if (!reduce.matches && !(navigator.connection && navigator.connection.saveData)) {
    var startBg = function () {
      var f = d.createElement('iframe');
      var bg = heroMedia.getAttribute('data-bg');
      var yt = bg.indexOf('youtube:') === 0;
      if (yt) {
        /* YouTube has no background mode: no controls, muted, looped through a one-video playlist, and the player
           oversized so its title bar and logo sit outside the banner (site.css). The reel shows only while it is
           playing: when it buffers, pauses or restarts the loop, YouTube puts a spinner or play button over a frozen
           frame, so the still comes back until it plays again. That also keeps an error screen from ever showing. */
        var id = bg.slice(8);
        f.src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&mute=1&loop=1&playlist=' + id +
          '&controls=0&disablekb=1&fs=0&iv_load_policy=3&modestbranding=1&playsinline=1&rel=0&enablejsapi=1' +
          '&origin=' + encodeURIComponent(location.origin);
        f.className = 'yt';
        var showing = null;
        window.addEventListener('message', function (e) {
          if (e.source !== f.contentWindow) return;
          var m; try { m = typeof e.data === 'string' ? JSON.parse(e.data) : e.data; } catch (err) { return; }
          var state = m && (m.event === 'onStateChange' ? m.info : m.info && m.info.playerState);
          if (typeof state !== 'number') return;
          if (state === 1) {
            if (!showing && !f.classList.contains('ready')) showing = setTimeout(function () { showing = null; f.classList.add('ready'); }, 1500);
          } else {
            clearTimeout(showing); showing = null;
            f.classList.remove('ready');
          }
        });
      } else {
        f.src = 'https://player.vimeo.com/video/' + bg + '?background=1&autoplay=1&loop=1&muted=1&dnt=1';
      }
      f.title = 'Background reel (muted)';
      f.setAttribute('aria-hidden', 'true');
      f.setAttribute('tabindex', '-1');
      f.allow = 'autoplay; fullscreen';
      f.addEventListener('load', function () {
        if (yt) f.contentWindow.postMessage(JSON.stringify({ event: 'listening', id: 1, channel: 'widget' }), '*');
        else setTimeout(function () { f.classList.add('ready'); }, 900);
      });
      heroMedia.appendChild(f);
    };
    if (d.readyState === 'complete') setTimeout(startBg, 600); else window.addEventListener('load', function () { setTimeout(startBg, 600); });
  }
  });

  /* ----- timecode in the navigation bar: the viewer's time of day, HH:MM:SS:FF at 24 fps.
     Decoration only, no control. With reduced motion it shows the time once and stays still. ----- */
  var tcs = [].slice.call(d.querySelectorAll('.tc-val')).map(function (c) { return c.querySelectorAll('i'); });
  if (tcs.length) {
    var pad = function (n) { return (n < 10 ? '0' : '') + n; };
    var tcTimer = 0;
    var paintTc = function () {
      var now = new Date();
      var f = Math.floor(now.getMilliseconds() * 24 / 1000);
      var t = pad(now.getHours()) + pad(now.getMinutes()) + pad(now.getSeconds()) + pad(f);
      tcs.forEach(function (digits) {
        for (var i = 0; i < digits.length; i++) if (digits[i].textContent !== t[i]) digits[i].textContent = t[i];
      });
      return now.getMilliseconds();
    };
    var tickTc = function () {
      tcTimer = 0;
      var ms = paintTc();
      if (!d.hidden && !reduce.matches) tcTimer = setTimeout(tickTc, 1000 / 24 - ms % (1000 / 24) + 2);
    };
    d.addEventListener('visibilitychange', function () { if (!d.hidden && !tcTimer) tickTc(); });
    tickTc();
  }

  /* ----- thumbnails fade in as they scroll into view, as on the Squarespace site (Joshua, 2026-10-20).
     Ones already on screen when the page loads show straight away, and reduced motion skips it. Nothing is
     hidden from search: the tiles are in the page either way, only their opacity changes. ----- */
  if (!reduce.matches && 'IntersectionObserver' in window) {
    var fadeIo = new IntersectionObserver(function (en) {
      en.forEach(function (e) {
        if (!e.isIntersecting) return;
        var t = e.target, grid = t.parentNode;
        var cols = getComputedStyle(grid).gridTemplateColumns.split(' ').length || 1;
        var i = [].filter.call(grid.children, function (c) { return !c.hidden; }).indexOf(t);
        t.style.transitionDelay = (i < 0 ? 0 : i % cols) * 90 + 'ms';
        t.classList.add('in');
        fadeIo.unobserve(t);
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    d.querySelectorAll('.grid > .tile').forEach(function (t) {
      if (t.getBoundingClientRect().top < window.innerHeight) return;
      t.classList.add('fade');
      fadeIo.observe(t);
    });
  }

  /* ----- video player ----- */
  var player = d.getElementById('player');
  var frame = player && player.querySelector('.player-frame');
  var ptitle = player && player.querySelector('.player-title');
  var lastOpener = null;
  function embedUrl(btn) {
    var v = btn.getAttribute('data-vimeo');
    var y = btn.getAttribute('data-youtube');
    if (v) {
      var parts = v.split('?h=');
      return 'https://player.vimeo.com/video/' + parts[0] + '?autoplay=1&title=0&byline=0&portrait=0&dnt=1' + (parts[1] ? '&h=' + parts[1] : '');
    }
    if (y) return 'https://www.youtube-nocookie.com/embed/' + y + '?autoplay=1&rel=0&modestbranding=1';
    return null;
  }
  function closePlayer() {
    if (!player || !player.open) return;
    player.close();
  }
  if (player) {
    player.addEventListener('close', function () { frame.innerHTML = ''; if (lastOpener) lastOpener.focus(); });
    player.querySelector('.player-close').addEventListener('click', closePlayer);
    player.addEventListener('click', function (e) { if (e.target === player) closePlayer(); });
  }
  d.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-vimeo], [data-youtube]');
    if (!btn || !player || typeof player.showModal !== 'function') return;
    var url = embedUrl(btn);
    if (!url) return;
    e.preventDefault();
    lastOpener = btn;
    ptitle.textContent = btn.getAttribute('data-title') || 'Video';
    frame.innerHTML = '';
    var f = d.createElement('iframe');
    f.src = url;
    f.title = btn.getAttribute('data-title') || 'Video';
    f.allow = 'autoplay; fullscreen; picture-in-picture';
    f.setAttribute('allowfullscreen', '');
    frame.appendChild(f);
    player.showModal();
  });

  /* ----- work filters ----- */
  d.querySelectorAll('[data-filters]').forEach(function (bar) {
    var grid = d.getElementById(bar.getAttribute('data-filters'));
    var tiles = [].slice.call(grid.querySelectorAll('.tile'));
    var status = bar.parentNode.querySelector('.filter-status');
    bar.querySelectorAll('button').forEach(function (b) {
      b.addEventListener('click', function () {
        var cat = b.getAttribute('data-cat');
        bar.querySelectorAll('button').forEach(function (o) { o.setAttribute('aria-pressed', o === b ? 'true' : 'false'); });
        var shown = 0;
        tiles.forEach(function (t) {
          var cats = (t.getAttribute('data-cats') || '').split(' ');
          var show = cat === 'all' ? t.hasAttribute('data-all') : cats.indexOf(cat) > -1;
          t.hidden = !show;
          if (show) shown++;
        });
        if (status) status.textContent = shown + ' ' + (shown === 1 ? 'project' : 'projects') + ' shown';
      });
    });
  });

  /* ----- slideshows: advance on their own every few seconds.
     Pause on hover or keyboard focus, when off screen or the tab is hidden, and when the visitor
     asks for reduced motion. No pause button (Joshua, 2026-10-15). ----- */
  d.querySelectorAll('.show').forEach(function (show) {
    var slides = [].slice.call(show.querySelectorAll('.show-stage figure'));
    if (slides.length < 2) return;
    var n = show.querySelector('.show-n');
    var cap = show.querySelector('.show-cap');
    var bar = show.querySelector('.show-progress');
    var dur = parseInt(show.getAttribute('data-interval') || '5000', 10);
    show.style.setProperty('--dur', dur + 'ms');
    var i = 0, timer = null, hovering = false, focused = false, visible = true, stopped = reduce.matches;

    function load(k) {
      var img = slides[k].querySelector('img[data-src]');
      if (img) { img.src = img.getAttribute('data-src'); img.removeAttribute('data-src'); }
    }
    function paint() {
      slides.forEach(function (s, k) { s.classList.toggle('on', k === i); s.setAttribute('aria-hidden', k === i ? 'false' : 'true'); });
      if (n) n.textContent = (i + 1) + ' / ' + slides.length;
      if (cap) cap.textContent = slides[i].querySelector('img').getAttribute('alt') || '';
      load((i + 1) % slides.length);
    }
    function restartBar() {
      if (!bar) return;
      show.classList.remove('playing');
      void bar.offsetWidth;
      if (running()) show.classList.add('playing');
    }
    function go(step) { i = (i + step + slides.length) % slides.length; load(i); paint(); schedule(); }
    function running() { return !stopped && !hovering && !focused && visible && !d.hidden; }
    function schedule() {
      clearTimeout(timer);
      restartBar();
      if (running()) timer = setTimeout(function () { go(1); }, dur);
    }
    show.querySelector('.prev').addEventListener('click', function () { go(-1); });
    show.querySelector('.next').addEventListener('click', function () { go(1); });
    show.addEventListener('mouseenter', function () { hovering = true; schedule(); });
    show.addEventListener('mouseleave', function () { hovering = false; schedule(); });
    show.addEventListener('focusin', function (e) {
      var kb = true;
      try { kb = e.target.matches(':focus-visible'); } catch (err) { /* older browsers */ }
      if (kb) { focused = true; schedule(); }
    });
    show.addEventListener('focusout', function (e) { if (!show.contains(e.relatedTarget)) { focused = false; schedule(); } });
    var x0 = null;
    show.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    show.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 40) go(dx < 0 ? 1 : -1);
      x0 = null;
    });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (en) { visible = en[0].isIntersecting; schedule(); }, { threshold: .25 }).observe(show);
    }
    d.addEventListener('visibilitychange', schedule);
    if (reduce.addEventListener) reduce.addEventListener('change', function () { stopped = reduce.matches; schedule(); });
    paint();
    schedule();
  });

  /* ----- quote forms: this is the review copy, so they check the fields and say they didn't send ----- */
  d.querySelectorAll('form.form').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var st = form.querySelector('.form-status');
      st.hidden = false;
      st.textContent = 'This is the review copy of the site, so the form doesn’t send. On mindinmotion.tv it goes to Josh and Victor.';
      st.focus();
    });
  });
})();
