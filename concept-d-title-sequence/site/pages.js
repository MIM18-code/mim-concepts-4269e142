(function () {
  var d = document;

  /* ----- portfolio filters: toggle buttons that hide tiles outside the chosen category ----- */
  var bar = d.querySelector('.filters');
  if (bar) {
    var tiles = [].slice.call(d.querySelectorAll('.sheet > li[data-cat]'));
    var count = d.querySelector('.sheet-count');
    bar.addEventListener('click', function (e) {
      var b = e.target.closest('button[data-f]');
      if (!b) return;
      var f = b.getAttribute('data-f'), shown = 0;
      [].forEach.call(bar.querySelectorAll('button'), function (o) { o.setAttribute('aria-pressed', o === b ? 'true' : 'false'); });
      tiles.forEach(function (li) {
        var on = f === 'all' || (' ' + li.getAttribute('data-cat') + ' ').indexOf(' ' + f + ' ') > -1;
        li.hidden = !on;
        if (on) shown++;
      });
      if (count) count.textContent = shown + (shown === 1 ? ' film' : ' films');
    });
  }

  /* ----- behind-the-scenes strips: previous and next scroll by most of a screen ----- */
  [].forEach.call(d.querySelectorAll('.strip-sec'), function (sec) {
    var s = sec.querySelector('.strip'), prev = sec.querySelector('.prev'), next = sec.querySelector('.next');
    if (!s || !prev || !next) return;
    function sync() {
      prev.disabled = s.scrollLeft < 8;
      next.disabled = s.scrollLeft + s.clientWidth > s.scrollWidth - 8;
    }
    function go(dir) {
      var smooth = !window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      s.scrollBy({ left: dir * s.clientWidth * 0.8, behavior: smooth ? 'smooth' : 'auto' });
    }
    prev.addEventListener('click', function () { go(-1); });
    next.addEventListener('click', function () { go(1); });
    s.addEventListener('scroll', sync, { passive: true });
    window.addEventListener('resize', sync);
    sync();
  });

  /* ----- contact form: this is a design preview, so it checks the fields and says it didn't send ----- */
  var form = d.querySelector('form.form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var st = form.querySelector('.form-status');
      st.hidden = false;
      st.textContent = 'Design preview: this form does not send yet. On the live site it goes to Josh and Victor.';
      st.focus();
    });
  }
})();
