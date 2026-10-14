#!/usr/bin/env python3
"""Build the whole concept D site into concept-d-title-sequence/site/.

The homepage (../index.html, the picked concept) stays the source of truth for the look. This script
copies its CSS, script, header, menu, footer and player out of it, rewrites the live-site links so they
point at the pages built here, and writes the inner pages from the data below. Run it again after
index.html changes and every page picks the change up.

    python3 site/_build/build.py        (from concept-d-title-sequence/)
"""
import html
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE = HERE.parent
D = SITE.parent
SRC = (D / 'index.html').read_text()
A = '../../assets/img/'
LIVE = 'https://mindinmotion.tv'
SLUGS = ['portfolio', 'commercial-video-production', 'corporate-video-production', 'film-production',
         'post-production', 'about', 'contact']
SERVICE_SLUGS = SLUGS[1:5]
e = html.escape


# ---------------------------------------------------------------- pieces of the homepage
def grab(pattern):
    m = re.search(pattern, SRC, re.S)
    if not m:
        raise SystemExit('build.py: could not find %r in index.html' % pattern)
    return m.group(0)


def relink(s, depth_fix=True):
    for slug in SLUGS:
        s = s.replace('href="%s/%s"' % (LIVE, slug), 'href="%s.html"' % slug)
    s = s.replace('href="./"', 'href="index.html"')
    if depth_fix:
        s = s.replace('"../assets/', '"../../assets/')
    return s


styles = re.findall(r'<style[^>]*>(.*?)</style>', SRC, re.S)
SCRIPT = re.findall(r'<script>\n(\(function \(\) \{.*?)</script>', SRC, re.S)[-1]
SYMBOLS = grab(r'<svg width="0" height="0".*?</svg>')
HEADER = relink(grab(r'<header class="hdr">.*?</header>'))
MENU = relink(grab(r'<dialog class="menu".*?</dialog>'))
FOOTER = relink(grab(r'<footer class="end">.*?</footer>'))
PLAYER = grab(r'<dialog class="player".*?</dialog>')
FONTS = grab(r'<link rel="preconnect" href="https://fonts.googleapis.com">.*?rel="stylesheet">')
EARLY = grab(r'<script>\n  // Runs before first paint.*?</script>')


def current(s, slug):
    """Mark the current page in the header and the menu."""
    s = s.replace('href="%s.html">' % slug, 'href="%s.html" aria-current="page">' % slug)
    s = s.replace('href="%s.html"><span' % slug, 'href="%s.html" aria-current="page"><span' % slug)
    s = s.replace('class="disp" href="%s.html"' % slug, 'class="disp" href="%s.html" aria-current="page"' % slug)
    if slug in SERVICE_SLUGS:
        s = s.replace('<li class="dd">', '<li class="dd cur">')
    return s


# ---------------------------------------------------------------- business facts (Baltimore only)
BUSINESS = {
    '@type': ['LocalBusiness', 'ProfessionalService'],
    '@id': LIVE + '/#business',
    'name': 'MindInMotion',
    'url': LIVE + '/',
    'logo': LIVE + '/images/mindinmotion-logo.png',
    'image': LIVE + '/images/og-share.jpg',
    'description': 'Film and video production in Baltimore for nonprofits, universities and public agencies.',
    'telephone': '+1-443-527-5181',
    'email': 'mindinmotionpro@gmail.com',
    'foundingDate': '2012',
    'founder': [{'@type': 'Person', 'name': 'Joshua Land'}, {'@type': 'Person', 'name': 'Victor Fink'}],
    'address': {'@type': 'PostalAddress', 'streetAddress': '3617 Chestnut Ave', 'addressLocality': 'Baltimore',
                'addressRegion': 'MD', 'postalCode': '21211', 'addressCountry': 'US'},
    'areaServed': ['Baltimore', 'Maryland', 'Washington, DC'],
    'sameAs': ['https://www.instagram.com/mindinmotionpro', 'https://vimeo.com/mindinmotionpro',
               'https://www.youtube.com/@mindinmotionpro', 'https://www.facebook.com/mindinmotionpro',
               'https://www.linkedin.com/company/mindinmotion', 'https://www.imdb.com/name/nm4644677/'],
}


def ld(page):
    url = LIVE + '/' + page['slug']
    linked = [(n, s) for n, s in page['crumbs'] if s is not None]
    crumbs = [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': LIVE + ('/' + s if s else '/')}
              for i, (n, s) in enumerate(linked)]
    graph = [BUSINESS,
             {'@type': 'WebPage', '@id': url + '#page', 'url': url, 'name': page['title'],
              'description': page['desc'], 'isPartOf': {'@id': LIVE + '/#site'},
              'about': {'@id': LIVE + '/#business'}},
             {'@type': 'BreadcrumbList', 'itemListElement': crumbs}]
    if page.get('service'):
        graph.append({'@type': 'Service', 'serviceType': page['service'], 'provider': {'@id': LIVE + '/#business'},
                      'areaServed': BUSINESS['areaServed'], 'url': url})
    if page.get('faq'):
        graph.append({'@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': re.sub('<[^>]+>', '', a)}}
            for q, a in page['faq']]})
    return json.dumps({'@context': 'https://schema.org', '@graph': graph}, indent=1, ensure_ascii=False)


# ---------------------------------------------------------------- page template
def page_html(page, body):
    slug = page['slug']
    return f'''<!doctype html>
<html lang="en">
<head>
<meta name="robots" content="noindex, nofollow, noarchive">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(page['title'])}</title>
<meta name="description" content="{e(page['desc'])}">
<!-- At launch: the canonical URL is the live address, without .html. -->
<link rel="canonical" href="{LIVE}/{slug}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="MindInMotion">
<meta property="og:title" content="{e(page['title'])}">
<meta property="og:description" content="{e(page['desc'])}">
<meta property="og:url" content="{LIVE}/{slug}">
<meta property="og:image" content="{LIVE}/images/og-share.jpg">
<meta name="theme-color" content="#000000">
<link rel="icon" type="image/png" href="{A}mindinmotion-logo.png">
{EARLY}
{FONTS}
<link rel="preload" as="image" href="{A}{page['hero']['img']}" fetchpriority="high">
<link rel="stylesheet" href="d.css">
<link rel="stylesheet" href="pages.css">
<script type="application/ld+json">
{ld(page)}
</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

{SYMBOLS}

{current(HEADER, slug)}

{current(MENU, slug)}

<main id="main">
{hero(page)}
{body}
</main>

{FOOTER}

{PLAYER}

<script src="d.js"></script>
<script src="pages.js"></script>
</body>
</html>
'''


# ---------------------------------------------------------------- building blocks
ARR = '<svg class="arr"><use href="#arr"/></svg>'
TRI = '<svg class="tri"><use href="#tri"/></svg>'


def play_attrs(v):
    """v is 'vimeo:ID', 'youtube:ID' or 'link:URL'."""
    kind, ref = v.split(':', 1)
    return 'data-%s="%s"' % (kind, e(ref))


def hero(page):
    h = page['hero']
    crumbs = []
    for i, (name, s) in enumerate(page['crumbs']):
        if i == len(page['crumbs']) - 1:
            crumbs.append('<li><span aria-current="page">%s</span></li>' % e(name))
        elif s is None:
            crumbs.append('<li><span>%s</span></li>' % e(name))
        else:
            crumbs.append('<li><a href="%s">%s</a></li>' % ((s + '.html') if s else 'index.html', e(name)))
    stats = ''.join('<div><dt class="wide">%s</dt><dd>%s</dd></div>' % (e(k), v) for k, v in h.get('stats', []))
    ctas = h.get('ctas') or [('contact.html', 'Tell us what you need', True),
                             ('reel', 'Watch the reel', False)]
    cta = []
    for href, label, solid in ctas:
        if href == 'reel':
            cta.append('<button class="btn" type="button" data-vimeo="851026180" data-title="Demo reel">%s%s</button>' % (TRI, e(label)))
        else:
            cta.append('<a class="btn%s" href="%s">%s%s</a>' % (' btn-solid' if solid else '', href, e(label), (' ' + ARR) if solid else ''))
    return f'''
  <!-- SC 00 · Main titles -->
  <section class="stage hero ph{' short' if h.get('short') else ''}" aria-labelledby="hero-title" style="--fp:{h.get('pos', '50% 40%')}">
    <div class="frame">
      <img src="{A}{h['img']}" width="{h['w']}" height="{h['h']}" fetchpriority="high"
           alt="{e(h['alt'])}">
    </div>
    <div class="bar bar-t" aria-hidden="true"></div>
    <div class="bar bar-b" aria-hidden="true"></div>

    <div class="hero-slate mono in1">
      <span class="slate-l"><b aria-hidden="true">SC 00</b><nav class="crumbs" aria-label="Breadcrumb"><ol>{''.join(crumbs)}</ol></nav></span>
      <span class="slate-r"><button class="tc clock" type="button" aria-pressed="false" aria-label="Pause the timecode" data-clock><span class="tc-lbl">TC </span><span class="tc-val">00:00:00:00</span></button></span>
    </div>

    <p class="presents wide in2">{e(h.get('presents', 'Baltimore'))}</p>

    <div class="hero-body">
      <div class="hero-main">
        <h1 id="hero-title" class="disp"><span class="h1-in">{h['h1']}</span></h1>
        <div class="hero-ctas in4">
          {chr(10).join(cta)}
        </div>
      </div>
      <div class="hero-side">
        <p class="hero-sub in3">{h['sub']}</p>
        {'<dl class="stats in3">' + stats + '</dl>' if stats else ''}
      </div>
    </div>
  </section>
'''


def copy_sec(sc, h2, lede, paras, cast=None, black=False, link=None, figs=None, hid=None):
    if h2 is None:
        return f'''
  <section class="copy-sec{' black' if black else ''}" aria-label="{e(hid or 'Introduction')}">
    <div class="wrap">
      <p class="sec-slate mono" aria-hidden="true"><b>{sc}</b></p>
      <div class="copy solo">
        <p class="solo-lede rv">{lede}</p>
        <div class="copy-body">
          {''.join('<p class="about-p">%s</p>' % p for p in paras)}
        </div>
      </div>
    </div>
  </section>
'''
    hid = hid or 'h-' + re.sub(r'[^a-z0-9]+', '-', re.sub('<[^>]+>', '', h2).lower()).strip('-')[:32]
    cast_html = ''
    if cast:
        cast_html = '<dl class="cast">' + ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (k, v) for k, v in cast) + '</dl>'
    link_html = '<a class="link-arrow" href="%s">%s %s</a>' % (link[0], e(link[1]), ARR) if link else ''
    left = '<h2 id="%s" class="sec-h disp rv">%s</h2>' % (hid, h2)
    if figs:
        left = '<div class="copy-figs">%s%s</div>' % (left, figs)
    return f'''
  <section class="copy-sec{' black' if black else ''}" aria-labelledby="{hid}">
    <div class="wrap">
      <p class="sec-slate mono" aria-hidden="true"><b>{sc}</b></p>
      <div class="copy">
        {left}
        <div class="copy-body">
          <p class="about-lede">{lede}</p>
          {''.join('<p class="about-p">%s</p>' % p for p in paras)}
          {cast_html}
          {link_html}
        </div>
      </div>
    </div>
  </section>
'''


def scene(num, label, shots, nfac=None):
    """shots: list of dicts with img,w,h,pos,alt,client,title,sub,kind,desc,play,id,quote,hold."""
    n = len(shots)
    nfac = nfac if nfac is not None else (2 if n > 1 else .45)
    out = []
    for i, s in enumerate(shots):
        cls = 'shot' + (' hold' if s.get('hold') else '') + (' is-on' if i == 0 else '')
        pid = s.get('id') or 'p-%s-%d' % (num, i)
        frame_play = '<button class="frame-play" type="button" tabindex="-1" aria-hidden="true" data-for="%s"><svg><use href="#tri-lg"/></svg></button>' % (s.get('for') or pid)
        if s.get('card'):
            pic = '<div class="frame card-frame"><div class="intertitle">%s</div>%s</div>' % (''.join('<p>%s</p>' % t for t in s['card'] if t), frame_play)
        else:
            pic = '''<div class="frame">
            <img src="%s%s" width="%d" height="%d" loading="lazy" style="object-position:%s"
                 alt="%s">
            %s
          </div>''' % (A, s['img'], s['w'], s['h'], s.get('pos', '50% 40%'), e(s['alt']), frame_play)
        if s.get('quote'):
            q, who, role = s['quote']
            cap = '''<blockquote class="subs">
            <p><span>%s</span></p>
            <footer class="mono"><b>%s</b> <span class="by-role">%s</span></footer>
          </blockquote>''' % (q, who, role)
        else:
            sub = ' <span class="cr-sub">- %s</span>' % s['sub'] if s.get('sub') else ''
            kind = '<p class="cr-kind mono">%s</p>' % s['kind'] if s.get('kind') else ''
            long_ = ' long' if s.get('long') else ''
            cap = f'''<figcaption class="credit">
            <div class="cr-main"><p class="cr-client wide">{s['client']}</p><h3 class="cr-title disp{long_}">{s['title']}{sub}</h3></div>
            <div class="cr-body">
              {kind}
              {'<p class="cr-desc">%s</p>' % s['desc'] if s.get('desc') else ''}
            </div>
            <button class="btn play" id="{pid}" type="button" {play_attrs(s['play'])} data-title="{e(s['ptitle'])}" aria-label="Play {e(s['ptitle'])}">{TRI}Play</button>
          </figcaption>'''
        out.append('''
        <figure class="%s">
          %s
          %s
        </figure>''' % (cls, pic, cap))
    return f'''
  <!-- {num} · {e(label)} -->
  <section class="scene" id="sc-{num.split()[-1]}" data-shots="{n}" style="--n:{nfac}" aria-label="{e(label)}">
    <div class="stage">
      <p class="slate mono"><span class="slate-l"><b aria-hidden="true">{num}</b><span class="sl-client">{e(label)}</span></span><span class="slate-r"><span class="sl-shot" aria-hidden="true">Shot 1/{n}</span></span></p>
      <div class="shots">{''.join(out)}
      </div>
      <div class="bar bar-t" aria-hidden="true"></div>
      <div class="bar bar-b" aria-hidden="true"></div>
      <div class="scrub" aria-hidden="true"><i></i></div>
    </div>
  </section>
'''


CAT_LABEL = {'commercial': 'Commercial', 'corporate': 'Corporate', 'nonprofit': 'Nonprofit', 'film': 'Film',
             'music-video': 'Music video'}


def tile(w):
    """w: dict(cat, label, title, cr, img, w, h, play, alt, card_kind, crop, pname)."""
    title = w['title']
    name = w.get('pname') or title
    if w.get('img'):
        crop = ' class="crop-l3"' if w.get('crop') else ''
        frame_in = '<img%s src="%s%s" width="%d" height="%d" loading="lazy" alt="%s">' % (crop, A, w['img'], w['w'], w['h'], e(w['alt']))
        fcls = 'tile-frame'
    else:
        frame_in = '<span class="tcard-t">%s</span><span class="tcard-s mono">%s</span>' % (e(w.get('card_t') or title), e(w['card_kind']))
        fcls = 'tile-frame tcard'
    is_link = w['play'].startswith('link:')
    cue = ('<span class="tile-cue mono">Prime Video %s</span>' % '<svg class="arr" style="width:22px;height:10px"><use href="#arr"/></svg>') if is_link else \
          '<span class="tile-cue mono">%sPlay</span>' % TRI
    cr = '<span class="tile-cr mono">%s</span>' % e(w['cr']) if w.get('cr') else ''
    meta = '<span class="tile-meta"><span class="tile-client wide">%s</span><span class="tile-title">%s</span>%s</span>' % (
        e(w['label']), e(title), cr)
    if is_link:
        el = '<a class="tile-btn" href="%s" aria-label="%s on Prime Video">' % (e(w['play'][5:]), e(name))
        end = '</a>'
    else:
        el = '<button class="tile-btn" type="button" %s data-title="%s" aria-label="Play %s">' % (play_attrs(w['play']), e(name), e(name))
        end = '</button>'
    cat = ' data-cat="%s"' % w['cat'] if w.get('cat') else ''
    return '''
        <li%s>
          %s
            <span class="%s">%s%s</span>
            %s
          %s
        </li>''' % (cat, el, fcls, frame_in, cue, meta, end)


def sheet_sec(sc, h2, p, works, endcta=None, hid=None, black=True, filters=False, cols=None):
    hid = hid or 'h-' + re.sub(r'[^a-z0-9]+', '-', h2.lower()).strip('-')[:32]
    fl = ''
    if filters:
        counts = {k: sum(1 for w in works if k in w['cat'].split()) for k in CAT_LABEL}
        order = ['commercial', 'corporate', 'film', 'music-video', 'nonprofit']
        fl = '<div class="filters" role="group" aria-label="Filter by type"><button type="button" data-f="all" aria-pressed="true">All<span class="n">%d</span></button>%s</div><p class="sheet-count mono" aria-live="polite">%d projects</p>' % (
            len(works), ''.join('<button type="button" data-f="%s" aria-pressed="false">%s<span class="n">%d</span></button>' % (k, CAT_LABEL[k], counts[k]) for k in order),
            len(works))
    end = ''
    if endcta:
        end = '''
      <div class="endcta">
        <p>%s</p>
        <div class="btns">
          <a class="btn btn-solid" href="contact.html">%s %s</a>
          %s
        </div>
      </div>''' % (endcta[0], endcta[1], ARR, endcta[2] if len(endcta) > 2 else '<a class="btn" href="portfolio.html">See all projects</a>')
    return f'''
  <section class="sheet-sec"{'' if black else ' style="background:var(--ink)"'} aria-labelledby="{hid}">
    <div class="wrap">
      <p class="sec-slate mono" aria-hidden="true"><b>{sc}</b></p>
      <div class="sec-head">
        <h2 id="{hid}" class="sec-h disp rv">{h2}</h2>
        {'<p>%s</p>' % p if p else ''}
      </div>
      {fl}
      <ul class="sheet{' two' if cols == 2 else ''}">{''.join(tile(w) for w in works)}
      </ul>{end}
    </div>
  </section>
'''


def strip_sec(sc, h2, p, folder, items):
    hid = 'h-bts'
    lis = []
    for i, (f, alt) in enumerate(items):
        path = SITE.parent.parent / 'assets' / 'img' / 'bts' / folder / f
        from PIL import Image  # only needed at build time
        w, h = Image.open(path).size
        lis.append('''
          <li><figure><img src="%sbts/%s/%s" width="%d" height="%d" loading="lazy" alt="%s"></figure></li>''' % (
            A, folder, f, w, h, e(alt)))
    return f'''
  <section class="strip-sec" aria-labelledby="{hid}">
    <div class="wrap">
      <p class="sec-slate mono" aria-hidden="true"><b>{sc}</b><span>{len(items)} stills</span></p>
      <div class="sec-head">
        <h2 id="{hid}" class="sec-h disp rv">{h2}</h2>
        <div style="display:grid;gap:18px;justify-items:start">
          {'<p>%s</p>' % p if p else ''}
          <div class="strip-nav"><button class="icon-btn prev" type="button" aria-label="Previous stills">{ARR}</button><button class="icon-btn next" type="button" aria-label="Next stills">{ARR}</button></div>
        </div>
      </div>
    </div>
    <ul class="strip" tabindex="0" role="region" aria-label="Behind-the-scenes stills, scroll sideways">{''.join(lis)}
    </ul>
  </section>
'''


def pull(q, who, role):
    return f'''
  <section class="pull-sec" aria-label="What a client said">
    <figure class="pull">
      <blockquote><p>{q}</p></blockquote>
      <figcaption><span class="wide">{who}</span><span class="wide role">{role}</span></figcaption>
    </figure>
  </section>
'''


# ---------------------------------------------------------------- copy rule
# Joshua, 2026-10-12: keep the live site's copy unless a new line is actively better. Every visible line
# below is the live copy (mindinmotion.tv, main at 288d3fb), the homepage copy Joshua approved for concept
# D on 2026-10-07, or a change listed with its reason in ../COPY-REVIEW.md. Case follows the type system
# (sentence case); the words don't change.

# Related services reuse the homepage's own section (approved copy).
SVC = {
    'commercial-video-production': ('Commercial', 'TV spots and social cuts. Commercials live or die in the first three seconds. Our Maryland Excels PSAs aired statewide, and we made a WellPoint spot for InterPublic.'),
    'corporate-video-production': ('Corporate', 'Not every video needs to sell something. Some recruit, train a team or show donors where their money goes. Our interviews run like conversations, not depositions.'),
    'film-production': ('Film', "Features, shorts, documentaries and music videos. We can produce the whole film or join your crew. Tell us your budget and we'll talk through what's possible."),
    'post-production': ('Post-Production', 'Editing, color grading, VFX and motion graphics. We can handle the full post workflow or pick up a project already in progress.'),
}


def related(sc, this):
    items, n = [], 0
    for slug, (name, d) in SVC.items():
        if slug == this:
            continue
        n += 1
        items.append('<li><span class="svc-n mono" aria-hidden="true">%02d</span><h3 class="svc-t"><a href="%s.html">%s<svg class="arr" aria-hidden="true"><use href="#arr"/></svg></a></h3><p class="svc-d">%s</p></li>' % (n, slug, name, d))
    return f'''
  <section class="svc-sec" aria-labelledby="h-more">
    <div class="wrap">
      <p class="sec-slate mono" aria-hidden="true"><b>{sc}</b></p>
      <div class="sec-head">
        <h2 id="h-more" class="sec-h disp rv">Production and post</h2>
        <p>We plan, shoot, edit and finish films. Bring us in for the whole production or for the part you need.</p>
      </div>
      <ol class="svc-list plain">
        {''.join(items)}
      </ol>
    </div>
  </section>
'''


def closing(sc, img, w, h, alt, pos='50% 40%', h2='Tell us about your project',
            lede='Add your budget and deadline if you know them. Josh or Victor replies within 24 hours.',
            btn='Get a free quote'):
    return f'''
  <!-- {sc} · Contact: the closing title card (the homepage's) -->
  <section class="cta-sec" aria-labelledby="cta-title">
    <p class="ec-slate mono" aria-hidden="true"><b>{sc}</b></p>
    <figure class="ec-frame mt">
      <img src="{A}{img}" width="{w}" height="{h}" loading="lazy" style="object-position:{pos}"
           alt="{e(alt)}">
    </figure>
    <div class="ec-bar">
      <div>
        <h2 id="cta-title" class="disp rv">{h2}</h2>
        <p class="cta-lede">{lede}</p>
        <div class="cta-btns">
          <a class="btn btn-solid" href="contact.html">{btn} {ARR}</a>
        </div>
      </div>
      <dl class="ec-credits">
        <div><dt class="wide">Baltimore</dt><dd><a href="tel:+14435275181">(443) 527-5181</a></dd></div>
        <div><dt class="wide">Email</dt><dd><a href="mailto:mindinmotionpro@gmail.com">mindinmotionpro@gmail.com</a></dd></div>
      </dl>
    </div>
  </section>
'''


# ---------------------------------------------------------------- the work: titles and credit lines as on the live portfolio
DIR = 'Director: Josh Land & Victor Fink'
MSDE = 'Client: Maryland State Department of Education'
JHAAP = 'Client: Johns Hopkins Advanced Academic Programs'
ALA = 'Client: American Lung Association'
W = {
    'reel': dict(cat='commercial corporate film music-video nonprofit', label='Reel', title='Demo Reel', cr='MindInMotion', img='reel-tile.webp', w=1280, h=720, play='vimeo:851026180', alt='The MindInMotion wordmark over blurred city lights.'),
    'playground': dict(cat='commercial nonprofit', label='Commercial', title='Maryland Excels - Moms at the Playground', cr=DIR + ', DP: John Grove', img='Screen-Shot-2022-06-24-at-5.18.24-PM.webp', w=1200, h=675, play='vimeo:723874620', alt='A girl in a yellow dress runs past two mothers sitting on a playground bench.'),
    'goodmom': dict(cat='commercial nonprofit', label='Commercial', title='Good Mom MD Excels TV PSA', cr=DIR + ', DP: Alex Guckert', img='Screen-Shot-2022-06-24-at-6.14.31-PM-2.webp', w=2500, h=1406, play='vimeo:794207449', alt='A woman stands in a dark bathroom at night, lit by cold blue light.'),
    'ghost': dict(cat='music-video', label='Music video', title='Juliet Lloyd - Ghost Light', cr=DIR + ', DP: Ryan Celli', img='ghost-light-thumbnail.webp', w=2500, h=1250, play='youtube:lxHxaH-awBM', alt='A singer at a grand piano in gold stage light and haze.'),
    'cyw': dict(cat='music-video', label='Music video', title='Juliet Lloyd - Call Your Wife', cr=DIR, img='vimeo-1937932446.webp', w=640, h=360, play='vimeo:1019535308', alt='A woman with a guitar in an overgrown field, the sun flaring behind her.'),
    'joe': dict(cat='nonprofit corporate', label='Nonprofit', title='Infinite Legacy - Joe', cr='Client: Infinite Legacy', img='Joe-ILF.webp', w=2500, h=1406, play='vimeo:836987067', alt='A man in silhouette against an evening sky, his head resting in his hand.'),
    'checklist': dict(cat='commercial nonprofit', label='Commercial', title='Maryland Excels - Checklist Moments', cr=MSDE, img='vimeo-1784674291.webp', w=640, h=360, play='vimeo:904194910', alt="A small child with curly hair holds a parent's hand."),
    'eng': dict(cat='corporate', label='Corporate', title='Johns Hopkins Masters in Science and Engineering Management', cr='Client: Johns Hopkins', img='vimeo-1864108460.webp', w=640, h=360, crop=True, play='vimeo:953655351', alt='A program director in a gray jacket, interviewed in an engineering lab.'),
    'illegal': dict(cat='commercial nonprofit', label='Commercial', title='Maryland State Department of Education - Illegal Childcare', cr=DIR + ', DP: Alex Guckert', img='Screenshot-2024-01-18-at-2.33.57-PM.webp', w=2500, h=1406, play='vimeo:794249489', alt='A couple sits on a living room couch, one of them working on a laptop.'),
    'lotus': dict(cat='film', label='Film', title='Lotus Eyes (feature film, 2016)', cr='Director: Joshua Land', img='lotus-eyes.webp', w=1920, h=1080, play='youtube:D4CIiTOL16c', alt='A woman and a boy at a window in soft side light.'),
    'cuba': dict(cat='corporate', label='Corporate', title='Cuba, The Field Course Experience', cr=JHAAP, img='child-horse-cuba.webp', w=1200, h=675, play='vimeo:376001457', alt='A boy in a yellow shirt sits on a horse beside a thatched hut under a storm sky.'),
    'pearlstone': dict(cat='nonprofit corporate', label='Nonprofit', title='Pearlstone', cr='Client: Pearlstone', img='vimeo-1458914655.webp', w=640, h=360, play='vimeo:724562331', alt='Kids in life jackets wave from a canoe on a lake.'),
    'cdspg': dict(cat='nonprofit', label='Nonprofit', title='Chesapeake Down Syndrome Parent Group - Building Friendships', cr='Client: Chesapeake Down Syndrome Parent Group', img='cdspg-building-friendships.webp', w=1920, h=1080, play='youtube:G42RJGRNlGY', alt='Two boys hug on a front lawn. One wears glasses and a red sweater.'),
    'residency': dict(cat='corporate', label='Corporate', title='Johns Hopkins AAP Teaching Writing - 2018 Residency', cr=JHAAP, img='residency.webp', w=1920, h=1080, play='youtube:gSCIClcxpMw', alt='A woman looks up in a wood-paneled library.'),
    'layne': dict(cat='corporate', label='Corporate', title='Johns Hopkins AAP Teaching Writing - Precious Layne', cr=JHAAP, img='precious-layne.webp', w=480, h=270, play='youtube:juCJhFbIsXs', alt='A young woman with braids smiles during an interview in a classroom.'),
    'packard': dict(cat='nonprofit corporate', label='Nonprofit', title='The Packard Center for ALS Research', cr='Client: The Packard Center', img='Screen-Shot-2019-12-09-at-2.15.52-PM-2-1.webp', w=1920, h=1080, play='vimeo:378347545?h=65f9bfe1c5', alt='Researchers at laptops in a meeting room, shot with shallow focus.'),
    'sydney': dict(cat='nonprofit corporate', label='Nonprofit', title='Sydney B. - Biomarker Testing Story', cr=ALA, play='youtube:MkNrUkNgVfA', card_kind='American Lung Association'),
    'ashley': dict(cat='nonprofit corporate', label='Nonprofit', title='Ashley & Dr. Reed - Patient-Provider Story', cr=ALA, play='youtube:dxUx8L3rQos', card_kind='American Lung Association'),
    'lungforce': dict(cat='nonprofit corporate', label='Nonprofit', title='LUNG FORCE Advocacy Day 2025', cr=ALA, play='youtube:kaDZAOgjiR8', card_kind='American Lung Association'),
    'ape': dict(cat='film', label='Film', title='Ape Canyon (feature film, 2019)', cr='Directors: Joshua Land & Victor Fink', img='ape-canyon.webp', w=1842, h=1036, play='link:https://www.amazon.com/gp/video/detail/B091SXZYT8', alt='Two young people lie in tall grass, alarmed.'),
    'quality': dict(cat='commercial nonprofit', label='Commercial', title='Because Quality Matters', cr=MSDE, img='checklist.webp', w=2500, h=1406, play='vimeo:1021087594?h=2c0add4aa6', alt='Preschoolers laugh and shape clay at a classroom table.'),
    'aacpd': dict(cat='commercial', label='Commercial', title='AACPD Recruitment', cr=DIR + ', DP: Alex Guckert', img='Screen-Shot-2022-06-24-at-5.40.56-PM.webp', w=2500, h=1406, play='vimeo:723880294', alt='A young woman at night, rim-lit, with red and blue police lights blurred behind her.'),
    'farmhouse': dict(cat='film', label='Film', title='The Farmhouse (short film, 2023)', cr=DIR, play='youtube:8oQABz68coc', card_t='The Farmhouse', card_kind='Short film, 2023'),
    'chelsea': dict(cat='nonprofit corporate', label='Nonprofit', title='Infinite Legacy - Chelsea', cr='Client: Infinite Legacy', img='chelsea-ilf.webp', w=1920, h=1080, play='vimeo:836990393', alt='A mother holds her baby close, cheek to cheek, in warm light.'),
    'wouldnt': dict(cat='commercial nonprofit', label='Commercial', title="Maryland State Department of Education - You Wouldn't", cr=MSDE, img='Screen-Shot-2023-01-30-at-2.23.33-PM.webp', w=2500, h=1406, play='vimeo:794227360', alt="Extreme close-up of an older man looking through a jeweler's loupe."),
    'finding': dict(cat='nonprofit', label='Nonprofit', title='Maryland Excels - Finding Childcare', cr=DIR + ', DP: Alex Guckert', img='Screenshot-2024-01-18-at-2.36.22-PM.webp', w=2500, h=1406, play='vimeo:723892095?h=bef550ce0c', alt='A woman presents an on-screen graphic for the Maryland Excels program directory.'),
    'wellpoint': dict(cat='commercial', label='Commercial', title='WellPoint', cr='Client: InterPublic', img='Screen-Shot-2022-10-19-at-3.10.25-PM.webp', w=2500, h=1406, play='vimeo:762000615', alt='A mother and daughter read together on a bedroom floor.'),
    'ilikeme': dict(cat='film', label='Film', title='I Like Me (feature film, 2018)', cr='Director: Joshua Land', img='i-like-me.webp', w=1200, h=675, play='link:https://www.amazon.com/dp/b07v5qtljq', alt='Two women laugh on the grass on a summer day.'),
    'hiking': dict(cat='film', label='Film', title="Don't Go Hiking (short film, 2019)", cr=DIR, play='vimeo:567645681', card_t="Don't Go Hiking", card_kind='Short film, 2019'),
    'odom': dict(cat='corporate', label='Corporate', title='Teaching Writing Profile - Mike Odom', cr=JHAAP, img='mike-odom.webp', w=1920, h=1080, play='youtube:FTm7CsQ0ug0', alt='A man in glasses looks off camera, trees soft behind him.'),
    'tidewater': dict(cat='corporate', label='Corporate', title='Tidewater Direct', cr='Client: Tidewater Direct', img='Screenshot-2024-09-10-at-2.02.32-PM.webp', w=2288, h=1150, play='vimeo:967087552', alt='The Tidewater Direct warehouse, a blue building across a green lawn.'),
    'badwitch': dict(cat='film', label='Film', title='Bad Witch (feature film, 2018)', cr='Directors: Joshua Land & Victor Fink', img='bad-witch.webp', w=1920, h=1081, play='youtube:ecRv4nLSXaE', alt='A young man at dusk, lit by hard orange light against a dark forest.'),
    'lovers': dict(cat='music-video', label='Music video', title='FIVES - Lovers in Lullaby', cr='Production/Post: MindInMotion', img='fives-lovers.webp', w=2179, h=1226, play='youtube:95TjgxYdpVo', alt='Two women at a lit makeup mirror, one in a red dress.'),
    'thunder': dict(cat='music-video', label='Music video', title='FIVES - Heart & Thunder', cr='Client: FIVES', img='fives-heart-thunder.webp', w=1280, h=720, play='youtube:R_O5CnzEmoY', alt='A drummer and a singer in blue light against a red wall.'),
    'risingtide': dict(cat='corporate', label='Corporate', title='Rising Tide Innovation Center, St. Petersburg FL', cr='Client: Rising Tide Innovation Center', img='rising-tide-tile.webp', w=1280, h=720, play='vimeo:436161742', alt='A bright open office with a wave mural, a long wood table and lounge seating.'),
    'bennetts': dict(cat='commercial', label='Commercial', title="Bennett's Curse St. Patrick's Day", cr="Client: Bennett's Curse", play='vimeo:1019980973?h=63b47d2669', card_t="St. Patrick's Day", card_kind="Bennett's Curse"),
}


def works(*keys):
    return [W[k] for k in keys]


def svc_block(sc, h2, lede, rows, fig=None, hid='h-svc', black=False):
    lis = ''.join('<li><span class="svc-n mono" aria-hidden="true">%02d</span><h3 class="svc-t">%s</h3><p class="svc-d">%s</p></li>' % (i + 1, t, d) for i, (t, d) in enumerate(rows))
    side = ''
    if fig:
        side = '<div class="svc-side"><figure class="svc-fig"><div class="fr vf"><img src="%s%s" width="%d" height="%d" loading="lazy" alt="%s"></div></figure></div>' % (A, fig[0], fig[1], fig[2], e(fig[3]))
    lede_html = '<p class="svc-lede rv">%s</p>' % lede if lede else ''
    return f'''
  <section class="svc-sec{' black' if black else ''}" aria-labelledby="{hid}">
    <div class="wrap">
      <p class="sec-slate mono" aria-hidden="true"><b>{sc}</b></p>
      <div class="svc"{'' if fig else ' style="grid-template-columns:minmax(0,1fr)"'}>
        <div>
          <h2 id="{hid}" class="sec-h disp rv">{h2}</h2>
          {lede_html}
          <ol class="svc-list">
            {lis}
          </ol>
        </div>
        {side}
      </div>
    </div>
  </section>
'''


# ================================================================ PAGES
PAGES = []

# ---------------------------------------------------------------- commercial
PAGES.append(dict(
    slug='commercial-video-production',
    title='Commercial Video Production in Baltimore | MindInMotion',
    desc='TV commercials, digital ads & brand videos that convert. Commercial video production in Baltimore. Request a free quote today.',
    crumbs=[('Home', ''), ('Services', None), ('Commercial', 'commercial-video-production')],
    service='Commercial video production',
    hero=dict(img='Screen-Shot-2022-06-24-at-6.14.31-PM-2.webp', w=2500, h=1406, pos='50% 45%',
              alt='From the Maryland Excels "Good Mom" spot: a woman in a dark bathroom at night, lit by cold blue light.',
              h1='Commercial Video Production',
              sub='Commercials live or die in the first three seconds.',
              ctas=[('contact.html', 'Tell Us About Your Project', True), ('reel', 'Watch the reel', False)]),
    body=lambda: ''.join([
        copy_sec('SC 01', None,
                 "Our team has spent years crafting spots that grab attention and hold it—for broadcast TV, streaming platforms, YouTube pre-roll, and social feeds. We've partnered with ad agencies and brands directly to produce campaigns that actually perform, not just look good in a conference room.",
                 ["What sets us apart is our background in narrative filmmaking. Every commercial we produce has intention behind every frame: motivated lighting, purposeful camera movement, performances that feel real. Whether it's a 15-second social cut or a 60-second broadcast spot, we approach it with the same discipline we bring to feature films. That's how you make something memorable when you're competing with a skip button.",
                  "From concept through final delivery, we handle production and post under one roof—which means fewer handoffs, tighter timelines, and creative that stays consistent from first frame to last. If you've got a campaign coming up, <a href=\"contact.html\">let's talk</a>."]),
        scene('SC 02', 'Maryland State Department of Education', [dict(
            img='Screen-Shot-2022-06-24-at-5.18.24-PM.webp', w=1200, h=675, pos='50% 45%',
            alt='A girl in a yellow dress runs past two mothers sitting on a playground bench.',
            client='Maryland State Department of Education', title='Maryland Excels', sub='Moms at the Playground',
            kind='Commercial &middot; <span class="nw">Director: Josh Land &amp; Victor Fink,</span> <span class="nw">DP: John Grove</span>',
            desc='The result was a multi-video campaign that aired statewide and drove traffic to the Maryland Excels program.',
            play='vimeo:723874620', ptitle='Maryland Excels - Moms at the Playground')]),
        scene('SC 03', 'InterPublic', [
            dict(img='Screen-Shot-2022-10-19-at-3.10.25-PM.webp', w=2500, h=1406, pos='50% 40%', id='p-wellpoint',
                 alt='A mother and daughter read together on a bedroom floor.',
                 client='Client: InterPublic', title='WellPoint', kind='Commercial',
                 play='vimeo:762000615', ptitle='WellPoint')]),
        pull('Super professional, a lot of fun to work with and always on schedule. Would recommend them for virtually any project!', 'Nate Lanzino', 'Entrepreneur'),
        sheet_sec('SC 04', 'Selected Work', 'A few of the commercials we’ve produced.',
                  works('goodmom', 'aacpd', 'wouldnt', 'checklist', 'wellpoint', 'playground', 'illegal', 'quality', 'bennetts'),
                  endcta=('Have a campaign in mind?', 'Tell Us About Your Project')),
        strip_sec('SC 05', 'Behind the Scenes', '', 'commercial', [
            ('01-dolly-track.webp', 'Camera operator on dolly track filming alongside lighting setup outdoors'),
            ('02-living-room-crew.webp', 'Film crew shooting a family scene on a living room set'),
            ('03-living-room-monitor.webp', 'Monitor showing the family scene being filmed in a living room'),
            ('04-park-shoot.webp', 'Crew filming an actor in a park under tall trees'),
            ('05-park-boom.webp', 'Boom operator and camera operator filming an actor in a park'),
            ('06-assistant-director.webp', 'Assistant director with radio and clipboard on an outdoor set'),
            ('07-crew-monitor-outdoors.webp', 'Crew gathered around a camera monitor during an outdoor shoot'),
            ('08-building-entrance.webp', 'Crew filming a scene outside a glass office building'),
            ('09-doctor-scene.webp', 'Actor in a white coat on set between takes'),
            ('10-bedroom-monitor.webp', "Two crew members smiling behind a camera monitor in a child's bedroom"),
            ('11-couch-scene.webp', 'Actors reading papers on a couch during a scene'),
            ('12-laptop-scene.webp', 'Camera framing an actor with a laptop on a living room couch'),
            ('13-studio-officers.webp', 'Crew filming a uniformed officer on a dark studio set'),
            ('14-officer-smiling.webp', 'Smiling officer on a black studio set during a recruitment shoot'),
        ]),
        related('SC 06', 'commercial-video-production'),
        closing('SC 07', 'wellpoint_md_2022--646---131231.webp', 2500, 1668,
                'The assistant director on set with a radio and a clipboard, the camera rig beside her.', pos='60% 35%'),
    ])))

# ---------------------------------------------------------------- corporate
PAGES.append(dict(
    slug='corporate-video-production',
    title='Corporate Video Production in Baltimore | MindInMotion',
    desc='Training videos, testimonials & internal communications. Corporate and nonprofit video production in Baltimore trusted by Johns Hopkins. Get a free quote.',
    crumbs=[('Home', ''), ('Services', None), ('Corporate', 'corporate-video-production')],
    service='Corporate and nonprofit video production',
    hero=dict(img='mike-odom.webp', w=1920, h=1080, pos='38% 35%',
              alt='From a Johns Hopkins AAP profile: a man in glasses looks off camera, trees soft behind him.',
              h1='Corporate Video Production',
              sub="Not every video needs to sell something. Sometimes you need to train a team, share a patient's story, or help donors understand where their money goes.",
              ctas=[('contact.html', 'Tell Us About Your Project', True), ('reel', 'Watch the reel', False)]),
    body=lambda: ''.join([
        copy_sec('SC 01', None,
                 "That's corporate video—and it's work we take seriously. We've produced training modules for hospital systems, testimonial campaigns for nonprofits, recruitment videos for universities, and internal communications for organizations that want their employees to watch.",
                 ["Our approach comes from documentary filmmaking. We let real people tell real stories. We set up interviews that feel like conversations, not depositions. We capture b-roll that shows your organization as it is, not a stock-photo version of it.",
                  "We've worked with Johns Hopkins, the Maryland State Department of Education, healthcare systems, and dozens of nonprofits and foundations across the Mid-Atlantic. If you need video that doesn't feel like a commercial, <a href=\"contact.html\">we should talk</a>."]),
        scene('SC 02', 'Infinite Legacy', [
            dict(img='Joe-ILF.webp', w=2500, h=1406, pos='40% 32%', id='p-joe',
                 alt='A man in silhouette against an evening sky, his head resting in his hand.',
                 client='Client: Infinite Legacy', title='Infinite Legacy', sub='Joe', kind='Organ donation testimonials',
                 desc="These videos have been used at fundraising galas, in hospital partner communications, and across the organization's awareness campaigns.",
                 play='vimeo:836987067', ptitle='Infinite Legacy - Joe'),
            dict(img='chelsea-ilf.webp', w=1920, h=1080, pos='50% 24%', id='p-chelsea',
                 alt='A mother holds her baby close, cheek to cheek, in warm light.',
                 client='Client: Infinite Legacy', title='Infinite Legacy', sub='Chelsea', kind='Organ donation testimonials',
                 desc='We let people share their stories in their own words, on their own timeline.',
                 play='vimeo:836990393', ptitle='Infinite Legacy - Chelsea')]),
        scene('SC 03', 'Johns Hopkins Advanced Academic Programs', [
            dict(img='residency.webp', w=1920, h=1080, pos='50% 30%', hold=True, id='p-residency',
                 alt='A woman looks up in a wood-paneled library.',
                 client='Client: Johns Hopkins Advanced Academic Programs', title='Teaching Writing', sub='2018 Residency',
                 play='youtube:gSCIClcxpMw', ptitle='Johns Hopkins AAP Teaching Writing - 2018 Residency'),
            dict(img='Screen-Shot-2019-12-11-at-3.34.02-PM-copy.webp', w=1920, h=1080, pos='62% 30%', **{'for': 'p-residency'},
                 alt='Two hikers with backpacks look out at mountains in Cuba.',
                 quote=('They go the extra mile to create the best content and offer helpful input on ways to create the most appealing video for our audience.', 'Patrick Moody', 'Director of Marketing, Johns Hopkins AAP'))]),
        sheet_sec('SC 04', 'Selected Work', 'Recruitment, training, and brand films for organizations across the Mid-Atlantic.',
                  works('eng', 'cuba', 'quality', 'finding', 'tidewater', 'pearlstone', 'risingtide', 'packard', 'cdspg', 'odom', 'ashley', 'sydney'),
                  endcta=('Have a project in mind?', 'Tell Us About Your Project')),
        strip_sec('SC 05', 'Behind the Scenes', '', 'corporate', [
            ('01-studio-teleprompter.webp', 'Woman filmed in studio with lighting rig, teleprompter and monitors'),
            ('02-white-studio.webp', 'Wide view of a white studio set up for an interview'),
            ('03-monitor-interview.webp', 'Camera crew with a monitor showing a woman being interviewed'),
            ('04-narrow-room-interview.webp', 'Woman seated for an interview with camera and lights in a narrow room'),
            ('05-studio-interview.webp', 'Woman standing for interview shoot in front of green screen'),
            ('06-ballroom-interview.webp', 'Multi-camera interview setup with a woman seated in a hotel ballroom'),
        ]),
        related('SC 06', 'corporate-video-production'),
        closing('SC 07', 'wellpoint_md_2022--1068---140101.webp', 2500, 1668,
                'A woman on a living room couch with a laptop, framed on the monitor in the foreground.', pos='55% 40%'),
    ])))

# ---------------------------------------------------------------- film
FILM_ROWS = [
    ('Feature films', [
        ('Lotus Eyes', '2016', 'Director: Joshua Land', 'lotus-eyes.webp', 1920, 1080, 'youtube:D4CIiTOL16c', 'Lotus Eyes (feature film, 2016)'),
        ('I Like Me', '2018', 'Director: Joshua Land', 'i-like-me.webp', 1200, 675, 'link:https://www.amazon.com/dp/b07v5qtljq', 'I Like Me (feature film, 2018)'),
        ('Bad Witch', '2018', 'Directors: <span class="nw">Joshua Land &amp; Victor Fink</span>', 'bad-witch.webp', 1920, 1081, 'youtube:ecRv4nLSXaE', 'Bad Witch (feature film, 2018)'),
        ('Ape Canyon', '2019', 'Directors: <span class="nw">Joshua Land &amp; Victor Fink</span>', 'ape-canyon.webp', 1842, 1036, 'link:https://www.amazon.com/gp/video/detail/B091SXZYT8', 'Ape Canyon (feature film, 2019)'),
        ('Incubation', '', 'Directors: <span class="nw">Joshua Land &amp; Victor Fink</span>', None, 0, 0, None, 'Incubation'),
    ]),
    ('Short films', [
        ('The Farmhouse', '2023', 'Director: <span class="nw">Josh Land &amp; Victor Fink</span>', None, 0, 0, 'youtube:8oQABz68coc', 'The Farmhouse (short film, 2023)'),
        ("Don't Go Hiking", '2019', 'Director: <span class="nw">Josh Land &amp; Victor Fink</span>', None, 0, 0, 'vimeo:567645681', "Don't Go Hiking (short film, 2019)"),
    ]),
    ('Music videos', [
        ('Ghost Light', '', 'Juliet Lloyd &middot; Director: <span class="nw">Josh Land &amp; Victor Fink,</span> <span class="nw">DP: Ryan Celli</span>', 'ghost-light-thumbnail.webp', 2500, 1250, 'youtube:lxHxaH-awBM', 'Juliet Lloyd - Ghost Light'),
        ('Call Your Wife', '', 'Juliet Lloyd &middot; Director: <span class="nw">Josh Land &amp; Victor Fink</span>', 'vimeo-1937932446.webp', 640, 360, 'vimeo:1019535308', 'Juliet Lloyd - Call Your Wife'),
        ('Lovers in Lullaby', '', 'FIVES &middot; Production/Post: MindInMotion', 'fives-lovers.webp', 2179, 1226, 'youtube:95TjgxYdpVo', 'FIVES - Lovers in Lullaby'),
        ('Heart &amp; Thunder', '', 'FIVES', 'fives-heart-thunder.webp', 1280, 720, 'youtube:R_O5CnzEmoY', 'FIVES - Heart &amp; Thunder'),
    ]),
]


def films_list():
    groups, mons, i = [], [], 0
    for gname, rows in FILM_ROWS:
        lis = []
        for t, yr, meta, img, w, h, play, ptitle in rows:
            sup = '<sup>%s</sup>' % yr if yr else ''
            if img:
                thumb = '<img class="thumb" src="%s%s" width="%d" height="%d" loading="lazy" alt="">' % (A, img, w, h)
                mons.append('<img%s src="%s%s" width="%d" height="%d" loading="lazy" alt="">' % (' class="on"' if i == 0 else '', A, img, w, h))
            else:
                thumb = '<span class="thumb card small" aria-hidden="true"><span class="disp">%s</span></span>' % t
                mons.append('<div class="card"><span class="disp">%s</span></div>' % t)
            if play is None:
                act = ''
            elif play.startswith('link:'):
                act = '<a class="act icon-btn" href="%s" aria-label="%s on Prime Video">%s</a>' % (play[5:], ptitle, ARR)
            else:
                act = '<button class="act icon-btn" type="button" %s data-title="%s" aria-label="Play %s">%s</button>' % (play_attrs(play), ptitle, ptitle, TRI)
            lis.append('''
            <li class="film" data-i="%d">
              <div class="film-row">
                %s
                <p class="film-t disp">%s%s</p>
                <p class="film-meta">%s</p>
                %s
              </div>
            </li>''' % (i, thumb, t, sup, meta, act))
            i += 1
        groups.append('''
        <div class="film-group">
          <h3 class="wide">%s</h3>
          <ol>%s
          </ol>
        </div>''' % (gname, ''.join(lis)))
    return f'''
  <section class="films-sec" id="films" aria-labelledby="films-title">
    <div class="inter" style="padding-inline:0">
      <div class="inter-grid wrap">
        <p class="reel mono"><b aria-hidden="true">Reel 1</b><span>SC 02</span></p>
        <h2 id="films-title" class="disp rv">Our feature films</h2>
        <div class="inter-side rv">
          <p>Victor shot "Lotus Eyes" and "I Like Me" while Josh directed. Now we co-direct.</p>
        </div>
      </div>
    </div>
    <div class="wrap films-grid">
      <div class="film-list">{''.join(groups)}
      </div>
      <div class="mon-col">
        <div class="monitor" aria-hidden="true">
          <div class="mon-frame vf">
            {chr(10).join(mons)}
          </div>
        </div>
      </div>
    </div>
  </section>
'''


PAGES.append(dict(
    slug='film-production',
    title='Film Production Company in Baltimore | MindInMotion',
    desc='Feature films, documentaries & narrative projects from Baltimore filmmakers. Our features have screened at festivals and are on major VOD platforms.',
    crumbs=[('Home', ''), ('Services', None), ('Film', 'film-production')],
    service='Film production',
    hero=dict(img='lotus-eyes.webp', w=1920, h=1080, pos='50% 35%',
              alt='From Lotus Eyes: a woman and a boy at a window in soft side light.',
              h1='Film Production',
              sub='Production and post-production support for features, shorts, documentaries, and music videos.',
              ctas=[('contact.html', 'Tell Us About Your Project', True), ('reel', 'Watch the reel', False)]),
    body=lambda: ''.join([
        copy_sec('SC 01', None,
                 'MindInMotion is a full-service film production company in Baltimore, Maryland. We produce and finish shorts and feature films, and have made five features of our own that screened at festivals across the globe and are on major VOD platforms.',
                 ["Making a film is rarely simple. We've been there, on film projects of every size, and we know how to make the process more manageable.",
                  "We aim to be one of the best film production companies in Baltimore and on the east coast. We'll be upfront about every step, and help you work out what's possible for your budget. If you need help getting a film off the ground, or need to fill specific production roles, fill out the <a href=\"contact.html\">contact form</a>."],
                 black=True),
        films_list(),
        pull('Not only are Josh and Victor an amazing creative team with a TON of knowledge on every facet of filmmaking, they&#39;re just great people.', 'Chris Perillo', 'Director'),
        strip_sec('SC 03', 'Behind the Scenes', '', 'film', [
            ('06-tunnel-scene.webp', 'Crew filming a scene in a graffiti-covered tunnel'),
            ('07-guitar-field.webp', 'Crew filming a woman playing guitar in a grassy field'),
            ('08-car-scene.webp', 'Camera monitor framing actors gathered behind an open car hatch'),
            ('09-teal-set.webp', 'Crew filming with camera rig in a teal-lit bathroom set'),
            ('10-festival-stage.webp', 'Joshua Land and Victor Fink on stage at a festival screening'),
            ('11-hillside-camera.webp', 'Camera operator filming from a foggy hillside'),
            ('12-lakeside-camera.webp', 'Two filmmakers checking a shot beside a lake'),
            ('13-river-valley.webp', 'Camera operator setting up on a riverbank in a pine valley'),
            ('14-cabin-scene.webp', 'Crew filming outside a weathered wooden cabin'),
            ('15-forest-camera.webp', 'Two crew members checking a camera rig at the edge of a forest'),
            ('16-woods-camera.webp', 'Camera operator and crew member in the woods between takes'),
            ('17-night-shoot.webp', 'Two camera operators on a night shoot under a large light'),
        ]),
        related('SC 04', 'film-production'),
        closing('SC 05', 'bts/film/12-lakeside-camera.webp', 2000, 1325,
                'Two filmmakers check a shot on a camera rig beside a lake.', pos='50% 40%'),
    ])))

# ---------------------------------------------------------------- post
PAGES.append(dict(
    slug='post-production',
    title='Post-Production Services in Baltimore | MindInMotion',
    desc='Video editing, color grading & VFX in DaVinci Resolve, Premiere & Final Cut Pro. Post-production services in Baltimore. Get a quote.',
    crumbs=[('Home', ''), ('Services', None), ('Post-Production', 'post-production')],
    service='Video post-production',
    hero=dict(img='011A5550.webp', w=2500, h=1667, pos='50% 45%',
              alt='A colorist at a grading desk in a dark edit suite, three monitors glowing in front of him.',
              h1='Post-Production',
              sub='Post-production is where everything comes together.',
              ctas=[('contact.html', 'Get a Quote', True), ('#h-work', 'See Our Work', False)]),
    body=lambda: ''.join([
        svc_block('SC 01', 'Our Services',
                  'Based in Baltimore, we’ve built our editing and color capabilities over a decade of feature films and commercial work. Whether you need a full post workflow or help with a specific piece—color, VFX—we can help.', [
                      ('Editing', "Story-driven editing from editors who've cut features, commercials, and everything in between. We work in DaVinci Resolve, Final Cut Pro, Premiere, and Avid."),
                      ('Color Grading', 'Professional color work in DaVinci Resolve. From technical corrections to establishing a cinematic look, we handle everything from LOG footage to final delivery.'),
                      ('VFX &amp; Motion Graphics', 'Compositing, cleanup, and motion graphics. We partner with trusted specialists for complex VFX work while handling standard effects in-house.'),
                      ('Delivery &amp; Mastering', "Final files in any format—broadcast specs, streaming platforms, social media, or theatrical DCPs."),
                      ('Project Rescue', 'Stalled project? Previous editor unavailable? We regularly take over in-progress work and get it to the finish line.'),
                  ], fig=('011A1266.webp', 2500, 1264, 'A color grading panel and monitors in a dark edit suite.'), hid='h-post', black=True),
        sheet_sec('SC 02', 'Finished In-House', 'Every project on this site was edited, colored, and finished by us. A few pieces that show the range.',
                  [dict(W['goodmom'], title='Maryland Excels "Good Mom"', label='Commercial spot'),
                   W['ghost'],
                   dict(W['cuba'], title='Cuba Field Course', label='Documentary'),
                   dict(W['checklist'], label='PSA campaign')], hid='h-work', cols=2),
        copy_sec('SC 03', 'Collaboration Is the Point',
                 "Our post-production process is built around collaboration. You'll have direct access to your editor, and we share cuts early and often.",
                 ['Whether you’re in Baltimore or across the country, you can watch cuts, leave timestamped notes, and approve versions through secure remote review.'],
                 cast=[('Tools We Work With', "DaVinci Resolve, Final Cut Pro, Premiere Pro, Avid Media Composer, After Effects, Fusion, Frame.io")]),
        related('SC 04', 'post-production'),
        closing('SC 05', '011A1266.webp', 2500, 1264, 'A color grading panel and monitors in a dark edit suite.', pos='50% 50%',
                h2='Need Post‑Production Help?',
                lede="Tell us about your project. Whether you need a full post workflow or just help with one piece of it, we can take it on.",
                btn='Get in Touch'),
    ])))

# ---------------------------------------------------------------- about
POSTERS = [('still-lotus-eyes.webp', 1280, 720, 'Lotus Eyes feature film — two leads against an industrial skyline', 'Lotus Eyes', 'Feature'),
           ('poster-i-like-me.webp', 608, 900, 'I Like Me feature film poster', 'I Like Me', 'Feature'),
           ('poster-ape-canyon.webp', 600, 900, 'Ape Canyon feature film poster', 'Ape Canyon', 'Feature'),
           ('still-bad-witch.webp', 1280, 720, 'Bad Witch feature film — profile of a bloodied young man at dusk', 'Bad Witch', 'Co-Directed'),
           ('poster-incubation.webp', 600, 900, 'Incubation feature film poster', 'Incubation', 'In Post')]
ABOUT_FILMS = '''
  <section class="copy-sec black" aria-labelledby="h-features">
    <div class="wrap">
      <p class="sec-slate mono" aria-hidden="true"><b>SC 04</b><span>The Films</span></p>
      <div class="sec-head">
        <h2 id="h-features" class="sec-h disp rv">Our Feature Films</h2>
        <p>Five features and counting—available on all major VOD platforms</p>
      </div>
      <ul class="posters">%s
      </ul>
      <p class="posters-note"><a href="film-production.html#films">Plus shorts, music videos, and commercials</a></p>
    </div>
  </section>
''' % ''.join('''
        <li><figure><div class="poster"><img src="%sfilms/%s" width="%d" height="%d" loading="lazy" alt="%s"></div><figcaption><h3 class="disp">%s</h3><p class="mono">%s</p></figcaption></figure></li>''' % (A, f, w, h, e(alt), t, k) for f, w, h, alt, t, k in POSTERS)

PAGES.append(dict(
    slug='about',
    title='About MindInMotion | Baltimore Video Production',
    desc='Meet Josh & Victor—film school friends turned production partners since 2012. Five feature films, and clients including Johns Hopkins.',
    crumbs=[('Home', ''), ('About', 'about')],
    hero=dict(img='11698893_10205059638871667_6520616449341988197_o-1.webp', w=2048, h=1712, pos='50% 55%',
              alt='A small crew films two actors in a graffiti-covered tunnel, a boom pole overhead.',
              h1='Film School Friends. Business Partners.',
              sub="We met in a 16mm filmmaking class at Johns Hopkins. Five feature films later, we're still making movies and videos for clients.",
              ctas=[('contact.html', 'Start a Conversation', True), ('portfolio.html', 'View Our Work', False)]),
    body=lambda: ''.join([
        copy_sec('SC 01', 'Our Story',
                 'Joshua Land and Victor Fink met in a 16mm filmmaking class at Johns Hopkins University and have been collaborating ever since. Josh grew up in Baltimore; Victor in Boston. Together they co-founded MindInMotion, a video production company based in Baltimore.',
                 ['Over the past decade-plus, they’ve produced features, shorts, music videos, and commercials together. Their narrative work includes "Lotus Eyes" and "I Like Me"—Victor shooting, Josh directing—before they stepped into co-directing with "Ape Canyon" and "Bad Witch." "Incubation" is their latest feature as a directing team.',
                  'The company has grown beyond their personal film projects to serve a wide range of clients. Their work spans documentary and fiction, and has taken them everywhere from Baltimore and Washington DC to the mountains of Washington state and the rainforests of Cuba.',
                  'Their feature films have screened at festivals across the world and are available on all major VOD platforms. When they’re not working for clients, they’re working on their own projects—"Incubation" is currently screening at festivals.'],
                 figs='''<figure style="margin:0">
            <div class="fr" style="overflow:hidden"><img src="%sJoshua-and-Victor-on-stage-1.webp" width="1200" height="798" loading="lazy" alt="Josh and Victor on stage at a screening Q&amp;A, one holding a microphone, both wearing lanyards." style="aspect-ratio:3/2;object-fit:cover;width:100%%"></div>
            <figcaption class="about-cap"><span class="wide">Since 2012</span><span>Josh and Victor</span></figcaption>
          </figure>''' % A),
        svc_block('SC 02', 'How We Think About Work', '', [
            ('Story First', "Every video—whether it's a 30-second spot or a feature film—tells a story, even when the subject is a police recruitment drive or a graduate program."),
            ('Collaboration', "We don't just take orders. We ask questions, offer ideas, and push back when something could be better."),
            ('Craft Matters', 'The right lens, the right color grade, a music cue that lands. The details are what people remember.'),
        ], fig=('crew-hike-bw.webp', 576, 322, 'Black-and-white photo of a small crew hiking up a foggy hillside with a camera and a boom pole.'), hid='h-how', black=True),
        f'''
  <section class="copy-sec" aria-labelledby="h-team">
    <div class="wrap">
      <p class="sec-slate mono" aria-hidden="true"><b>SC 03</b><span>The Team</span></p>
      <div class="sec-head">
        <h2 id="h-team" class="sec-h disp rv">Meet Josh &amp; Victor</h2>
      </div>
      <div class="team">
        <article class="bio">
          <h3 class="disp">Joshua Land</h3>
          <p class="role wide">Co-Founder / Director / Editor</p>
          <p>Josh grew up in Baltimore and studied Film &amp; Media Studies at Johns Hopkins. He's directed features that have screened at festivals worldwide and stream on major VOD platforms, first on his own and now co-directing with Victor.</p>
          <p>As lead editor and colorist, Josh brings a meticulous post-production eye to every project.</p>
          <a class="link-arrow" href="https://www.imdb.com/name/nm4644677/">IMDb {ARR}</a>
        </article>
        <article class="bio">
          <h3 class="disp">Victor Fink</h3>
          <p class="role wide">Co-Founder / Cinematographer / Producer</p>
          <p>Victor grew up in Boston and met Josh in that 16mm filmmaking class at Johns Hopkins—they've been collaborating ever since. As cinematographer, his visual style has defined the look of MindInMotion's features and dozens of commercial and corporate projects.</p>
          <p>He shot their early features while Josh directed, and they now co-direct. He and Josh share production logistics and client relationships, keeping shoots running smoothly whether they're in Baltimore or Cuba.</p>
          <a class="link-arrow" href="https://www.imdb.com/name/nm5227903/">IMDb {ARR}</a>
        </article>
      </div>
    </div>
  </section>
''' + ABOUT_FILMS,
        '''
  <section class="clients-sec" aria-labelledby="says-title">
    <div class="wrap">
      <p class="sec-slate mono" aria-hidden="true"><b>SC 05</b></p>
      <h2 id="says-title" class="roll-h disp rv">In their words</h2>
      <div class="says">
        <figure class="say">
          <blockquote><p>They go the extra mile to create the best content and offer helpful input on ways to create the most appealing video for our audience.</p></blockquote>
          <figcaption><span class="wide">Patrick Moody</span> <span class="wide role">Director of Marketing, Johns Hopkins AAP</span></figcaption>
        </figure>
        <figure class="say">
          <blockquote><p>Not only are Josh and Victor an amazing creative team with a TON of knowledge on every facet of filmmaking, they're just great people.</p></blockquote>
          <figcaption><span class="wide">Chris Perillo</span> <span class="wide role">Director</span></figcaption>
        </figure>
        <figure class="say">
          <blockquote><p>MindInMotion are terrifically talented. Easy to work with. And really care about the quality of their work.</p></blockquote>
          <figcaption><span class="wide">Matthew White</span> <span class="wide role">FIVES</span></figcaption>
        </figure>
        <figure class="say">
          <blockquote><p>Super professional, a lot of fun to work with and always on schedule. Would recommend them for virtually any project!</p></blockquote>
          <figcaption><span class="wide">Nate Lanzino</span> <span class="wide role">Entrepreneur</span></figcaption>
        </figure>
      </div>
      <dl class="credits trusted">
        <div>
          <dt class="wide">Clients include</dt>
          <dd>Johns Hopkins</dd>
          <dd>MD State Education</dd>
          <dd>American Lung Assoc.</dd>
          <dd>InterPublic</dd>
          <dd>Anne Arundel PD</dd>
          <dd>Infinite Legacy</dd>
          <dd>Packard Center</dd>
        </div>
      </dl>
    </div>
  </section>
''',
        closing('SC 06', 'wellpoint_md_2022--932---140101.webp', 2500, 1668,
                "Two crew members laugh over a printout, seen through the doorway of a child's bedroom set."),
    ])))

# ---------------------------------------------------------------- portfolio
CASES = [
    dict(n='01', client='Maryland State Department of Education', title='Maryland Excels Campaign', img='checklist.webp', w=2500, h=1406, pos='50% 38%',
         alt='From Because Quality Matters: preschoolers laugh and shape clay at a classroom table.',
         play='vimeo:1021087594?h=2c0add4aa6', ptitle='Because Quality Matters',
         text=['The Maryland State Department of Education needed videos that would reach parents across the state and convince them to choose licensed, quality childcare. The challenge: government messaging that doesn\'t feel like government messaging.',
               'We took a documentary approach. Instead of actors, we filmed real families at real childcare centers throughout Maryland. We followed parents through their actual routines, and captured kids being kids. The result was a multi-video campaign that aired statewide and drove traffic to the Maryland Excels program.'],
         deliv='TV spots, digital campaign, social cuts'),
    dict(n='02', client='Infinite Legacy', title='Organ Donation Testimonials', img='chelsea-ilf.webp', w=1920, h=1080, pos='50% 24%',
         alt='From Infinite Legacy: a mother holds her baby close, cheek to cheek, in warm light.',
         play='vimeo:836990393', ptitle='Infinite Legacy - Chelsea',
         text=['How do you tell stories about loss, grief, and hope without exploiting any of it? That was the question when Infinite Legacy asked us to create testimonial videos featuring donor families and organ recipients.',
               "We approached each interview like a conversation, not a production. Small crew, intimate setups, no rush. We let people share their stories in their own words, on their own timeline. The editing focused on honoring those stories rather than manipulating emotion. These videos have been used at fundraising galas, in hospital partner communications, and across the organization's awareness campaigns."],
         deliv='Testimonial series, gala content, awareness campaign'),
    dict(n='03', client='Johns Hopkins SAIS', title='Cuba Field Course Documentary', img='child-horse-cuba.webp', w=1200, h=675, pos='50% 40%',
         alt='From the Cuba field course film: a boy in a yellow shirt on a horse beside a thatched hut, under a storm sky.',
         play='vimeo:376001457', ptitle='Cuba, The Field Course Experience',
         text=['Johns Hopkins School of Advanced International Studies needed to capture their Cuba field course for program recruitment. The logistics were complicated: international travel, limited crew, working around academic schedules, and navigating Cuban filming restrictions.',
               'We embedded with the students for the duration of the course. A small crew meant we could move fast—classroom discussions, street interviews, cultural experiences—without disrupting the academic program. The final documentary has been used by Hopkins for years to recruit students into their international studies programs.'],
         deliv='Documentary, recruitment content, program materials'),
    dict(n='04', client='American Lung Association', title='Lung Cancer Patient Stories', img='ala-ashley-dr-reed.webp', w=1920, h=1080, pos='50% 22%',
         alt='From the Ashley and Dr. Reed film: Dr. Reed and Ashley talk across a small round table in his office.',
         play='youtube:dxUx8L3rQos', ptitle='Ashley & Dr. Reed - Patient-Provider Story',
         text=['The American Lung Association asked us to tell the stories of lung cancer patients and their healthcare providers, and to explain biomarker testing along the way.',
               "We worked closely with patients and doctors. Sydney's story shows how biomarker testing changed her prognosis. Ashley and Dr. Reed's video explores the patient-provider relationship during diagnosis. The campaign has been used nationally by the American Lung Association for patient education and advocacy."],
         deliv='Patient testimonial series, provider education content, advocacy campaign'),
]


def cases():
    out = []
    for c in CASES:
        if c.get('card'):
            lines = '<span style="display:block;font-weight:500;font-size:clamp(24px,2.6vw,40px);line-height:1.2;letter-spacing:-.02em;max-width:22em">%s</span>' % c['card'][0]
            if len(c['card']) > 1:
                lines += '<span style="display:block;margin-top:14px;color:var(--bone-2);font-size:clamp(16px,1.3vw,20px)">%s</span>' % c['card'][1]
            fr = '<button class="case-frame card-frame" type="button" %s data-title="%s" aria-label="Play %s"><span class="intertitle">%s</span><span class="tile-cue mono">%sPlay</span></button>' % (
                play_attrs(c['play']), e(c['ptitle']), e(c['ptitle']), lines, TRI)
        else:
            fr = '<button class="case-frame" type="button" %s data-title="%s" aria-label="Play %s"><img src="%s%s" width="%d" height="%d" loading="lazy" style="object-position:%s" alt="%s"><span class="tile-cue mono">%sPlay</span></button>' % (
                play_attrs(c['play']), e(c['ptitle']), e(c['ptitle']), A, c['img'], c['w'], c['h'], c['pos'], e(c['alt']), TRI)
        out.append(f'''
        <article class="case" aria-labelledby="case-{c['n']}">
          <p class="case-slate mono"><span><b aria-hidden="true">Case {c['n']}</b></span><span>{c['client']}</span></p>
          {fr}
          <div class="case-body">
            <div class="cr-main"><p class="cr-client wide">{c['client']}</p><h3 id="case-{c['n']}" class="cr-title disp">{c['title']}</h3></div>
            <div class="case-text">
              {''.join('<p>%s</p>' % e(t, quote=False) for t in c['text'])}
              <dl class="ec-credits"><div><dt class="wide">Deliverables</dt><dd>{c['deliv']}</dd></div></dl>
            </div>
          </div>
        </article>''')
    return f'''
  <section class="sheet-sec" aria-labelledby="h-cases">
    <div class="wrap">
      <p class="sec-slate mono" aria-hidden="true"><b>SC 01</b></p>
      <div class="sec-head">
        <h2 id="h-cases" class="sec-h disp rv">Featured Projects</h2>
      </div>
      <div class="cases">{''.join(out)}
      </div>
    </div>
  </section>
'''


ALL = ['reel', 'playground', 'goodmom', 'ghost', 'cyw', 'joe', 'checklist', 'eng', 'illegal', 'lotus', 'cuba', 'pearlstone',
       'cdspg', 'residency', 'layne', 'packard', 'sydney', 'ashley', 'lungforce', 'ape', 'quality', 'aacpd', 'farmhouse',
       'chelsea', 'wouldnt', 'finding', 'wellpoint', 'ilikeme', 'hiking', 'odom', 'tidewater', 'badwitch', 'lovers',
       'thunder', 'risingtide', 'bennetts']

PAGES.append(dict(
    slug='portfolio',
    title='Our Work | MindInMotion Video Production',
    desc='Watch our commercials, corporate videos & films. Work for Johns Hopkins, MSDE & more. See what we can create for you.',
    crumbs=[('Home', ''), ('Portfolio', 'portfolio')],
    hero=dict(img='ghost-light-thumbnail.webp', w=2500, h=1250, pos='50% 40%', short=True,
              alt='From Juliet Lloyd "Ghost Light": a singer at a grand piano in gold stage light and haze.',
              h1='Our Work',
              sub='Commercials, corporate videos, documentaries and feature films: our video production work for clients in Baltimore, Maryland and beyond. Tap any frame to watch.',
              ctas=[('reel', 'Watch the reel', False), ('contact.html', 'Tell Us About Your Project', True)]),
    body=lambda: ''.join([
        cases(),
        sheet_sec('SC 02', 'All Work', '', works(*ALL), black=False, filters=True, hid='h-all'),
        closing('SC 03', 'wellpoint_md_2022--1179---140101.webp', 2500, 1668,
                'Two actors read through papers on a couch, a monitor blurred in the foreground.', pos='50% 40%'),
    ])))

# ---------------------------------------------------------------- contact
FAQ = [
    ('How long does a typical project take?', 'Timeline varies by scope. A simple testimonial video might be delivered in 1-2 weeks, while a full commercial campaign typically takes 4-8 weeks from kickoff to final delivery.'),
    ('Do you travel for productions?', "Yes. We're based in Baltimore, and we regularly travel throughout the Mid-Atlantic, Southeast, and beyond. Travel costs are included in project quotes."),
    ("What's included in the quoted price?", "Our quotes include pre-production planning, equipment, crew, production, editing, color grading, motion graphics, and final delivery. We'll clearly outline any additional costs upfront."),
    ('How do revisions work?', "Each project includes a set number of revision rounds. We present rough cuts for feedback and refine until you're happy with the result. Additional revisions can be added if needed."),
    ('Can you match our existing brand guidelines?', 'Yes. We work with your brand assets, color palettes, fonts, and style guides so the videos match the rest of your marketing.'),
]


def opt(pairs, placeholder):
    return '<option value="" disabled selected>%s</option>' % placeholder + ''.join('<option value="%s">%s</option>' % (v, e(l)) for v, l in pairs)


CONTACT_BODY = lambda: f'''
  <section class="form-sec" aria-labelledby="h-form">
    <div class="wrap">
      <p class="sec-slate mono" aria-hidden="true"><b>SC 01</b></p>
      <div class="form-grid">
        <div>
          <h2 id="h-form" class="sec-h disp" style="margin-bottom:clamp(24px,3vw,40px)">Get a Quote</h2>
          <form class="form" name="contact" method="POST" action="thank-you" data-netlify="true" netlify-honeypot="bot-field">
            <input type="hidden" name="form-name" value="contact">
            <p class="hp"><label>Don't fill this out: <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
            <div class="field"><label for="f-name">Your Name *</label><input id="f-name" name="name" autocomplete="name" required placeholder="John Smith"></div>
            <div class="field"><label for="f-org">Company / Organization</label><input id="f-org" name="company" autocomplete="organization" placeholder="Acme Corp"></div>
            <div class="field"><label for="f-email">Email Address *</label><input id="f-email" name="email" type="email" autocomplete="email" required placeholder="john@company.com"></div>
            <div class="field"><label for="f-phone">Phone Number</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" placeholder="(555) 123-4567"></div>
            <div class="field"><label for="f-type">Project Type *</label><select id="f-type" name="project-type" required>{opt([('commercial', 'Commercial / Advertising'), ('corporate', 'Corporate Video'), ('recruitment', 'Recruitment / HR Video'), ('testimonial', 'Testimonial / Case Study'), ('documentary', 'Documentary'), ('film', 'Film / Narrative'), ('music-video', 'Music Video'), ('post-production', 'Post-Production Only'), ('other', 'Other')], 'Select a project type')}</select></div>
            <div class="field"><label for="f-budget">Budget Range *</label><select id="f-budget" name="budget" required>{opt([('under-2.5k', 'Under $2,500'), ('2.5-5k', '$2,500 - $5,000'), ('5-10k', '$5,000 - $10,000'), ('10-20k', '$10,000 - $20,000'), ('20k+', '$20,000+'), ('not-sure', 'Not sure yet')], 'Select your budget')}</select></div>
            <div class="field"><label for="f-when">Timeline</label><select id="f-when" name="timeline">{opt([('asap', 'As soon as possible'), ('1-month', 'Within 1 month'), ('1-3-months', '1-3 months'), ('3-6-months', '3-6 months'), ('flexible', 'Flexible / Not urgent')], 'When do you need this?')}</select></div>
            <div class="field"><label for="f-how">How did you hear about us?</label><select id="f-how" name="how-found">{opt([('google', 'Google Search'), ('referral', 'Referral'), ('social', 'Social Media'), ('vimeo', 'Vimeo'), ('previous-client', 'Previous Client'), ('other', 'Other')], 'Select an option')}</select></div>
            <div class="field full"><label for="f-msg">Tell Us About Your Project *</label><textarea id="f-msg" name="message" required placeholder="What are you making, who is it for, and when do you need it?"></textarea></div>
            <p class="note full">By submitting this form, you agree that MindInMotion may use the information you provide to respond to your inquiry. Read our <a href="https://mindinmotion.tv/privacy-policy">Privacy Policy</a>.</p>
            <button class="btn btn-solid full" type="submit">Send {ARR}</button>
            <p class="form-status full mono" role="status" tabindex="-1" hidden></p>
          </form>
        </div>
        <aside class="side-card" aria-labelledby="h-touch">
          <h2 id="h-touch" class="disp">Get In Touch</h2>
          <dl class="ec-credits">
            <div><dt class="wide">Baltimore HQ</dt><dd>3617 Chestnut Ave<br>Baltimore, MD 21211<br><span style="color:var(--bone-3)">Serving Maryland, DC &amp; the <span class="nw">Mid-Atlantic</span></span></dd></div>
            <div><dt class="wide">Phone</dt><dd><a href="tel:+14435275181">(443) 527-5181</a></dd></div>
            <div><dt class="wide">Email</dt><dd><a href="mailto:mindinmotionpro@gmail.com">mindinmotionpro@gmail.com</a></dd></div>
          </dl>
          <p class="mono" style="color:var(--bone-3)">We respond within 24 hours</p>
          <div>
            <h2 class="disp">What happens next?</h2>
            <ol class="steps" style="margin-top:16px">
              <li>We'll review your project details and set up a call</li>
              <li>We'll discuss your goals, timeline, and budget to understand the scope</li>
              <li>You'll receive a custom quote with clear deliverables and pricing</li>
            </ol>
          </div>
        </aside>
      </div>
    </div>
  </section>

  <section class="copy-sec" aria-labelledby="h-faq">
    <div class="wrap">
      <p class="sec-slate mono" aria-hidden="true"><b>SC 02</b></p>
      <div class="copy">
        <h2 id="h-faq" class="sec-h disp rv">Common Questions</h2>
        <div class="faq">
          {''.join('<details><summary>%s</summary><div class="faq-a">%s</div></details>' % (e(q), a) for q, a in FAQ)}
        </div>
      </div>
    </div>
  </section>
'''

PAGES.append(dict(
    slug='contact',
    title='Contact Us | MindInMotion Video Production',
    desc='Contact MindInMotion for a free video production quote. We serve Baltimore and the Mid-Atlantic region. Get a response within 24 hours.',
    crumbs=[('Home', ''), ('Contact', 'contact')],
    faq=FAQ,
    hero=dict(img='wellpoint_md_2022--612---131231.webp', w=1199, h=800, pos='50% 45%', short=True,
              alt='A crew sets up a scene in a leafy park, lights and a camera among the trees.',
              h1='Contact Us',
              sub="Tell us about your project and we'll get back to you with a quote.",
              ctas=[('#h-form', 'Get a free quote', True), ('tel:+14435275181', '(443) 527-5181', False)]),
    body=CONTACT_BODY))


# ---------------------------------------------------------------- write everything
def main():
    (SITE / 'd.css').write_text('/* Copied from ../index.html by _build/build.py. Edit index.html, then rebuild. */\n' + '\n'.join(styles))
    (SITE / 'd.js').write_text('/* Copied from ../index.html by _build/build.py. Edit index.html, then rebuild. */\n' + SCRIPT)
    (SITE / 'pages.css').write_text((HERE / 'pages.css').read_text())
    (SITE / 'pages.js').write_text((HERE / 'pages.js').read_text())
    (SITE / 'index.html').write_text(relink(SRC))
    # The monitor hero (REC button) is still a candidate, so it gets its own homepage for comparison.
    (SITE / 'home-monitor.html').write_text(relink((D / 'hero-monitor.html').read_text()))
    for p in PAGES:
        (SITE / (p['slug'] + '.html')).write_text(page_html(p, p['body']()))
    print('built', 1 + len(PAGES), 'pages into', SITE)


if __name__ == '__main__':
    main()
