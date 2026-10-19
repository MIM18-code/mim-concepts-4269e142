#!/usr/bin/env python3
"""Build the refined current site into refined-current-site/.

The layout follows the current mindinmotion.tv site (and the old Squarespace one): a normal top menu,
a reel hero, client logos, a work grid, services, a behind-the-scenes slideshow, testimonials and a
contact close. The look is concept D's monochrome. The copy and the work list come from concept D's
build (concept-d-title-sequence/site/_build/build.py), which went through Joshua's copy passes; every
change on top of that is logged in COPY-REVIEW.md.

No framework: this script writes plain HTML that uses site.css and site.js.

    python3 refined-current-site/_build/build.py       (from the repo root)
"""
import html
import json
import os
import re
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
REPO = OUT.parent
ASSETS = REPO / 'assets' / 'img'
A = '../assets/img/'          # shared images, relative to the built pages
L = 'img/'                    # images that only this site uses
LIVE = 'https://mindinmotion.tv'
e = html.escape

SERVICES = [
    ('commercial-video-production', 'Commercial'),
    ('corporate-video-production', 'Corporate'),
    ('film-production', 'Film'),
    ('post-production', 'Post-Production'),
]
SERVICE_SLUGS = [s for s, _ in SERVICES]


# ---------------------------------------------------------------- images
_dims = {}


def dims(src):
    """Width and height of an image we reference, read from disk."""
    if src in _dims:
        return _dims[src]
    if src.startswith(A):
        p = ASSETS / src[len(A):]
    elif src.startswith(L):
        p = OUT / src
    else:
        return (1280, 720)
    with Image.open(p) as im:
        _dims[src] = im.size
    return _dims[src]


def img(src, alt, cls='', lazy=True, pos=None, sizes=None, extra=''):
    w, h = dims(src)
    a = ['src="%s"' % e(src), 'width="%d"' % w, 'height="%d"' % h, 'alt="%s"' % e(alt)]
    if lazy:
        a.append('loading="lazy" decoding="async"')
    if cls:
        a.append('class="%s"' % cls)
    if pos:
        a.append('style="object-position:%s"' % pos)
    if extra:
        a.append(extra)
    return '<img %s>' % ' '.join(a)


def yt_thumb(vid):
    """A local copy of a YouTube thumbnail if we have one, otherwise YouTube's own (as the live site does)."""
    for ext in ('jpg', 'webp'):
        if (OUT / 'img' / 'thumbs' / ('%s.%s' % (vid, ext))).exists():
            return '%sthumbs/%s.%s' % (L, vid, ext)
    return 'https://img.youtube.com/vi/%s/maxresdefault.jpg' % vid


# ---------------------------------------------------------------- client logos (no links)
# Each logo is turned into a one-color white version so the row reads as one set. Files Joshua's Mac
# fetched from the organizations' own sites go in img/logos-src/ and are picked up when present.
BONE = (255, 255, 255)  # logo colour: plain white, same as the text
CLIENTS = [
    # (key, name, source file, mode, display height). Sources: ../assets/img/ for the logos the live site
    # already had; img/logos-src/ for ones fetched from each organization's own site (see SOURCES.md there).
    ('johns-hopkins', 'Johns Hopkins University', A + 'logo-johns-hopkins.png', 'sil', 32),
    ('usm', 'University System of Maryland', L + 'logos-src/usm.png', 'sil', 36),
    ('msde', 'Maryland State Department of Education', L + 'logos-src/msde.png', 'lum', 36),
    ('american-lung', 'American Lung Association', A + 'logo-american-lung.png', 'sil', 40),
    ('interpublic', 'Interpublic Group', A + 'logo-interpublic.png', 'sil', 30),
    ('aacpd', 'Anne Arundel County Police Department', A + 'logo-aacpd.png', 'badge', 60),
    ('infinite-legacy', 'Infinite Legacy', A + 'logo-infinite-legacy.png', 'sil', 44),
    ('packard', 'The Packard Center for ALS Research', A + 'logo-packard-center.png', 'sil', 44),
    ('pearlstone', 'Pearlstone', L + 'logos-src/pearlstone.png', 'sil', 40),
    ('rising-tide', 'Rising Tide Innovation Center', L + 'logos-src/rising-tide.png', 'sil', 36),
]


def make_logo(key, src, mode):
    """Write img/logos/<key>.png in bone, trimmed. Returns the path or None if the source is missing."""
    p = ASSETS / src[len(A):] if src.startswith(A) else OUT / src
    if not p.exists():
        return None
    out = OUT / 'img' / 'logos' / ('%s.png' % key)
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists() and out.stat().st_mtime >= p.stat().st_mtime and out.stat().st_mtime >= Path(__file__).stat().st_mtime:
        return L + 'logos/%s.png' % key
    im = Image.open(p).convert('RGBA')
    px = im.load()
    W, H = im.size
    res = Image.new('RGBA', (W, H), BONE + (0,))
    rp = res.load()
    if mode == 'badge':
        # a round seal on a white ground: keep only the disc, and draw its light parts in bone
        # so the dark ring falls away into the page and the lettering and badge stay readable
        ground = Image.new('L', (W, H), 0)
        gp = ground.load()
        for y in range(H):
            for x in range(W):
                rr, gg, bb, aa = px[x, y]
                if not (rr > 240 and gg > 240 and bb > 240):
                    gp[x, y] = 255
        x0, y0, x1, y1 = ground.getbbox()
        cx, cy, r = (x0 + x1) / 2, (y0 + y1) / 2, min(x1 - x0, y1 - y0) / 2 - 1
    for y in range(H):
        for x in range(W):
            rr, gg, bb, aa = px[x, y]
            lum = (0.2126 * rr + 0.7152 * gg + 0.0722 * bb) / 255
            if mode == 'sil':
                rp[x, y] = BONE + (aa,)
            elif mode == 'lum':
                rp[x, y] = BONE + (int(aa * min(1.0, (1 - lum) * 1.7)),)
            else:
                if (x - cx) ** 2 + (y - cy) ** 2 > r * r:
                    continue
                rp[x, y] = BONE + (int(255 * min(1.0, max(0.0, (lum - 0.12) / 0.75)) ** 1.1),)
    bbox = res.getbbox()
    if bbox:
        res = res.crop(bbox)
    res.save(out, optimize=True)
    return L + 'logos/%s.png' % key


def logo_row():
    items = []
    for key, name, src, mode, h in CLIENTS:
        path = make_logo(key, src, mode)
        if path:
            items.append('<li style="--lh:%dpx">%s</li>' % (h, img(path, name, lazy=False)))
        else:
            items.append('<li><span class="word">%s</span></li>' % e(name))
    return '''
  <section class="clients" aria-labelledby="h-clients">
    <div class="wrap">
      <h2 id="h-clients" class="clients-h">Trusted by industry leaders</h2>
      <ul class="logo-row">
        %s
      </ul>
    </div>
  </section>''' % '\n        '.join(items)


# ---------------------------------------------------------------- the work
# Titles, credit lines, stills and video IDs as on the live portfolio (via concept D's build).
DIR = 'Director: Josh Land & Victor Fink'
MSDE = 'Client: Maryland State Department of Education'
JHAAP = 'Client: Johns Hopkins Advanced Academic Programs'
ALA = 'Client: American Lung Association'
W = {
    'reel': dict(cats='', label='Reel', title='Demo Reel', cr='MindInMotion', img=A + 'reel-tile.webp', play='vimeo:851026180', alt='The MindInMotion wordmark over blurred city lights.'),
    'playground': dict(cats='commercial nonprofit', label='Commercial', title='Maryland Excels - Moms at the Playground', cr=DIR + ', DP: John Grove', img=A + 'Screen-Shot-2022-06-24-at-5.18.24-PM.webp', play='vimeo:723874620', alt='A girl in a yellow dress runs past two mothers sitting on a playground bench.'),
    'goodmom': dict(cats='commercial nonprofit', label='Commercial', title='Good Mom MD Excels TV PSA', cr=DIR + ', DP: Alex Guckert', img=A + 'Screen-Shot-2022-06-24-at-6.14.31-PM-2.webp', play='vimeo:794207449', alt='A woman stands in a dark bathroom at night, lit by cold blue light.'),
    'ghost': dict(cats='music', label='Music video', title='Juliet Lloyd - Ghost Light', cr=DIR + ', DP: Ryan Celli', img=A + 'ghost-light-thumbnail.webp', play='youtube:lxHxaH-awBM', alt='A singer at a grand piano in gold stage light and haze.'),
    'cyw': dict(cats='music', label='Music video', title='Juliet Lloyd - Call Your Wife', cr=DIR, img=A + 'call-your-wife-masks.webp', play='vimeo:1019535308', alt='A singer at a vintage microphone between two men in white masks, red-lit fog behind.'),
    'joe': dict(cats='nonprofit corporate', label='Nonprofit', title='Infinite Legacy - Joe', cr='Client: Infinite Legacy', img=A + 'Joe-ILF.webp', pos='40% 32%', play='vimeo:836987067', alt='A man in silhouette against an evening sky, his head resting in his hand.'),
    'checklist': dict(cats='commercial nonprofit', label='Commercial', title='Maryland Excels - Checklist Moments', cr=MSDE, img=A + 'vimeo-1784674291.webp', play='vimeo:904194910', alt="A small child with curly hair holds a parent's hand."),
    'eng': dict(cats='corporate', label='Corporate', title='Johns Hopkins Master of Science in Engineering Management', cr='Client: Johns Hopkins', img=A + 'eng-lab.webp', play='vimeo:953655351', alt='A man in blue gloves shows a 3D-printed part to a student beside an orange 3D-printer cover.'),
    'illegal': dict(cats='commercial nonprofit', label='Commercial', title='Maryland State Department of Education - Illegal Childcare', cr=DIR + ', DP: Alex Guckert', img=A + 'Screenshot-2024-01-18-at-2.33.57-PM.webp', play='vimeo:794249489', alt='A couple sits on a living room couch, one of them working on a laptop.'),
    'cuba': dict(cats='corporate', label='Corporate', title='Cuba, The Field Course Experience', cr=JHAAP, img=A + 'child-horse-cuba.webp', play='vimeo:376001457', alt='A boy in a yellow shirt sits on a horse beside a thatched hut under a storm sky.'),
    'pearlstone': dict(cats='nonprofit', label='Nonprofit', title='Pearlstone', cr='Client: Pearlstone', img=A + 'vimeo-1458914655.webp', play='vimeo:724562331', alt='Kids in life jackets wave from a canoe on a lake.'),
    'cdspg': dict(cats='nonprofit', label='Nonprofit', title='Chesapeake Down Syndrome Parent Group - Building Friendships', cr='Client: Chesapeake Down Syndrome Parent Group', img=A + 'cdspg-building-friendships.webp', play='youtube:G42RJGRNlGY', alt='Two boys hug on a front lawn. One wears glasses and a red sweater.'),
    'residency': dict(cats='corporate', label='Corporate', title='Johns Hopkins AAP Teaching Writing - 2018 Residency', cr=JHAAP, img=A + 'residency.webp', play='youtube:gSCIClcxpMw', alt='A woman looks up in a wood-paneled library.'),
    'layne': dict(cats='corporate', label='Corporate', title='Johns Hopkins AAP Teaching Writing - Precious Layne', cr=JHAAP, img=A + 'precious-layne.webp', play='youtube:juCJhFbIsXs', alt='A young woman with braids smiles during an interview in a classroom.'),
    'packard': dict(cats='nonprofit corporate', label='Nonprofit', title='The Packard Center for ALS Research', cr='Client: The Packard Center', img=A + 'Screen-Shot-2019-12-09-at-2.15.52-PM-2-1.webp', play='vimeo:378347545?h=65f9bfe1c5', alt='Researchers at laptops in a meeting room, shot with shallow focus.'),
    'sydney': dict(cats='nonprofit', label='Nonprofit', title='Sydney B. - Biomarker Testing Story', cr=ALA, yt='MkNrUkNgVfA', play='youtube:MkNrUkNgVfA', alt='A smiling couple lying on a beach towel, looking up at the camera.'),
    'ashley': dict(cats='nonprofit', label='Nonprofit', title='Ashley & Dr. Reed - Patient-Provider Story', cr=ALA, img=A + 'ala-ashley-dr-reed.webp', pos='50% 22%', play='youtube:dxUx8L3rQos', alt='Dr. Reed and Ashley talk across a small round table in his office.'),
    'lungforce': dict(cats='nonprofit', label='Nonprofit', title='LUNG FORCE Advocacy Day 2025', cr=ALA, yt='kaDZAOgjiR8', play='youtube:kaDZAOgjiR8', alt='The video\'s title card: the American Lung Association line "When you can\'t breathe, nothing else matters" over a hazy view of Washington, DC.'),
    'ape': dict(cats='film', label='Feature film', title='Ape Canyon (feature film, 2021)', cr='Directors: Joshua Land & Victor Fink', img=A + 'ape-canyon.webp', link='https://www.amazon.com/gp/video/detail/B091SXZYT8', alt='Two young people lie in tall grass, alarmed.'),
    'quality': dict(cats='commercial nonprofit', label='Commercial', title='Because Quality Matters', cr=MSDE, img=A + 'checklist.webp', pos='50% 38%', play='vimeo:1021087594?h=2c0add4aa6', alt='Preschoolers laugh and shape clay at a classroom table.'),
    'aacpd': dict(cats='commercial', label='Commercial', title='AACPD Recruitment', cr=DIR + ', DP: Alex Guckert', img=A + 'Screen-Shot-2022-06-24-at-5.40.56-PM.webp', play='vimeo:723880294', alt='A young woman at night, rim-lit, with red and blue police lights blurred behind her.'),
    'farmhouse': dict(cats='film', label='Short film', title='The Farmhouse (short film, 2023)', cr=DIR, img=A + 'farmhouse-thumbnail.webp', play='youtube:8oQABz68coc', alt='A young woman with a smear of blood on her cheek looks past an older man in a hat.'),
    'chelsea': dict(cats='nonprofit corporate', label='Nonprofit', title='Infinite Legacy - Chelsea', cr='Client: Infinite Legacy', img=A + 'chelsea-ilf.webp', pos='50% 24%', play='vimeo:836990393', alt='A mother holds her baby close, cheek to cheek, in warm light.'),
    'wouldnt': dict(cats='commercial nonprofit', label='Commercial', title="Maryland State Department of Education - You Wouldn't", cr=MSDE, img=A + 'Screen-Shot-2023-01-30-at-2.23.33-PM.webp', play='vimeo:794227360', alt="Seen from inside a patient's mouth: a man in a surgical mask and magnifying loupes raises a drill."),
    'finding': dict(cats='commercial nonprofit', label='Commercial', title='Maryland Excels - Finding Childcare', cr=DIR + ', DP: Alex Guckert', img=A + 'Screenshot-2024-01-18-at-2.36.22-PM.webp', play='vimeo:723892095?h=bef550ce0c', alt='A woman presents an on-screen graphic for the Maryland Excels program directory.'),
    'wellpoint': dict(cats='commercial', label='Commercial', title='WellPoint', cr='Client: InterPublic', img=A + 'Screen-Shot-2022-10-19-at-3.10.25-PM.webp', play='vimeo:762000615', alt='A mother and daughter read together on a bedroom floor.'),
    'ilikeme': dict(cats='film', label='Feature film', title='I Like Me (feature film, 2018)', cr='Director: Joshua Land', img=A + 'i-like-me.webp', play='youtube:RB5mmpYvsdo', alt='Two women laugh on the grass on a summer day.'),
    'hiking': dict(cats='film', label='Short film', title="Don't Go Hiking (short film, 2019)", cr=DIR, img=A + 'Screen-Shot-2022-06-24-at-6.17.35-PM-2.webp', play='vimeo:567645681', alt='A frightened young man in a backpack peers through autumn brush.'),
    'odom': dict(cats='corporate', label='Corporate', title='Teaching Writing Profile - Mike Odom', cr=JHAAP, img=A + 'mike-odom.webp', play='youtube:FTm7CsQ0ug0', alt='A man in glasses looks off camera, trees soft behind him.'),
    'tidewater': dict(cats='corporate', label='Corporate', title='Tidewater Direct', cr='Client: Tidewater Direct', img=A + 'Screenshot-2024-09-10-at-2.02.32-PM.webp', play='vimeo:967087552', alt='The Tidewater Direct warehouse, a blue building across a green lawn.'),
    'badwitch': dict(cats='film', label='Feature film', title='Bad Witch (feature film, 2021)', cr='Directors: Joshua Land & Victor Fink', img=A + 'bad-witch.webp', play='youtube:ecRv4nLSXaE', alt='A young man at dusk, lit by hard orange light against a dark forest.'),
    'lotus': dict(cats='film', label='Feature film', title='Lotus Eyes (feature film, 2016)', cr='Director: Joshua Land', img=A + 'lotus-eyes.webp', play='youtube:D4CIiTOL16c', alt='A woman and a boy at a window in soft side light.'),
    'incubation': dict(cats='film', label='Feature film', title='Incubation (teaser)', cr='Directors: Joshua Land & Victor Fink', img=A + 'incubation-teaser.webp', play='youtube:nHacNsApMkU', alt='A frame from the teaser for Incubation.'),
    'lovers': dict(cats='music', label='Music video', title='FIVES - Lovers in Lullaby', cr='Production/Post: MindInMotion', img=A + 'fives-lovers.webp', play='youtube:95TjgxYdpVo', alt='Two women at a lit makeup mirror, one in a red dress.'),
    'thunder': dict(cats='music', label='Music video', title='FIVES - Heart & Thunder', cr='Client: FIVES', img=L + 'fives-heart-thunder-169.webp', play='youtube:R_O5CnzEmoY', alt='A drummer and a singer in blue light against a red wall.'),
    'risingtide': dict(cats='corporate', label='Corporate', title='Rising Tide Innovation Center, St. Petersburg FL', cr='Client: Rising Tide Innovation Center', img=A + 'rising-tide-tile.webp', play='vimeo:436161742', alt='A bright open office with a wave mural, a long wood table and lounge seating.'),
    'bennetts': dict(cats='commercial', label='Commercial', title="Bennett's Curse St. Patrick's Day", cr="Client: Bennett's Curse", img=L + 'bennetts-curse-st-patricks-day.webp', play='vimeo:1019980973?h=63b47d2669', alt='A rotting, green-lit zombie face in close-up.'),
}

TRI = '<svg class="tri" viewBox="0 0 10 12" aria-hidden="true"><path d="M0 0v12l10-6z"/></svg>'


def play_attrs(w):
    if w.get('link'):
        return None
    kind, ref = w['play'].split(':', 1)
    return 'data-%s="%s" data-title="%s"' % (kind, e(ref), e(w['title']))


def still(w):
    if w.get('img'):
        return w['img']
    if w.get('yt'):
        return yt_thumb(w['yt'])
    return None


def frame(w, cls='tile-frame', eager=False):
    """The clickable picture: opens the player, or the film's page on Prime Video."""
    pic = img(still(w), w['alt'], lazy=not eager, pos=w.get('pos'))
    if w.get('link'):
        return '<a class="%s" href="%s" target="_blank" rel="noopener">%s<span class="cue cue-txt">Prime Video</span><span class="vh"> (opens in a new tab)</span></a>' % (
            cls, e(w['link']), pic)
    return '<button class="%s" type="button" %s aria-label="Play %s">%s<span class="cue" aria-hidden="true">%s</span></button>' % (
        cls, play_attrs(w), e(w['title']), pic, TRI)


def tile(key, all_set=None, meta=True, title=None, cr=None):
    w = dict(W[key], title=title) if title else W[key]
    if cr:
        w = dict(w, cr=cr)
    cats = w['cats']
    attrs = ' data-cats="%s"' % cats
    if all_set is not None:
        if key in all_set:
            attrs += ' data-all'
        else:
            attrs += ' hidden'
    m = '\n            <p class="meta">%s</p>' % e(w['cr']) if meta else ''
    return '''
        <li class="tile"%s>
          %s
          <div class="tile-cap">
            <h3 class="tile-t">%s</h3>%s
          </div>
        </li>''' % (attrs, frame(w), e(w['title']), m)


def work_grid(keys, gid, all_keys=None, filters=None, cols='', foot=None, meta=True, titles=None):
    """A grid of work. With filters, every tile is in the page and the buttons show and hide them."""
    bar = ''
    if filters:
        btns = ''.join('<button type="button" data-cat="%s" aria-pressed="%s">%s</button>' % (c, 'true' if c == 'all' else 'false', t)
                       for c, t in filters)
        bar = '<div class="filters ui" data-filters="%s" role="group" aria-label="Filter the work">%s</div><p class="vh filter-status" role="status"></p>' % (gid, btns)
    tiles = ''.join(tile(k, all_set=set(all_keys) if all_keys else None, meta=meta, title=(titles or {}).get(k)) for k in keys)
    f = '<div class="grid-foot">%s</div>' % foot if foot else ''
    return '%s<ul class="grid%s" id="%s">%s\n      </ul>%s' % (bar, ' ' + cols if cols else '', gid, tiles, f)


# The live Commercial and Corporate pages caption their grids with these shorter names.
SVC_TITLES = {
    'goodmom': 'Maryland Excels: Good Mom TV PSA', 'wouldnt': "Maryland Excels: You Wouldn't PSA",
    'checklist': 'Maryland Excels: Checklist Moments', 'wellpoint': 'WellPoint commercial',
    'playground': 'Maryland Excels: Moms at the Playground', 'illegal': 'MSDE: Illegal Childcare PSA',
    'eng': 'Johns Hopkins Engineering Management', 'chelsea': 'Infinite Legacy: Chelsea',
    'quality': 'Maryland Excels: Because Quality Matters', 'finding': 'Maryland Excels: Finding Childcare',
    'cuba': 'Johns Hopkins: Cuba Field Course', 'joe': 'Infinite Legacy: Joe', 'risingtide': 'Rising Tide Innovation Center',
    'packard': 'Packard Center for ALS Research', 'cdspg': 'CDSPG: Building Friendships', 'residency': 'Johns Hopkins Residency',
    'odom': 'Johns Hopkins: Teaching Writing',
}
GRIDFOOT = '<p class="grid-cta">%s</p><a class="btn" href="contact.html">Tell Us About Your Project</a>'
FILTERS = [('all', 'All'), ('commercial', 'Commercial'), ('corporate', 'Corporate'), ('film', 'Film'), ('music', 'Music Video'), ('nonprofit', 'Nonprofit')]


# ---------------------------------------------------------------- shared pieces
BUSINESS = {
    '@type': ['LocalBusiness', 'ProfessionalService'],
    '@id': LIVE + '/#business',
    'name': 'MindInMotion',
    'url': LIVE + '/',
    'logo': LIVE + '/images/mindinmotion-logo.png',
    'image': LIVE + '/images/og-share.jpg',
    'description': 'Award-winning video production company creating commercials, corporate videos, and films.',
    'telephone': '+1-443-527-5181',
    'email': 'mindinmotionpro@gmail.com',
    'foundingDate': '2012',
    'founder': [{'@type': 'Person', 'name': 'Joshua Land', 'sameAs': 'https://www.imdb.com/name/nm4644677/'},
                {'@type': 'Person', 'name': 'Victor Fink', 'sameAs': 'https://www.imdb.com/name/nm5227903/'}],
    'address': {'@type': 'PostalAddress', 'streetAddress': '3617 Chestnut Ave', 'addressLocality': 'Baltimore',
                'addressRegion': 'MD', 'postalCode': '21211', 'addressCountry': 'US'},
    'geo': {'@type': 'GeoCoordinates', 'latitude': 39.3317084, 'longitude': -76.6293025},
    'areaServed': ['Baltimore', 'Maryland', 'Washington, DC', 'Mid-Atlantic'],
    'hasMap': 'https://g.page/r/Cebm122V_KOAEAE',
    'priceRange': '$$',
    'knowsAbout': ['Video Production', 'Commercial Production', 'Corporate Video', 'Film Production', 'Post-Production'],
    'sameAs': ['https://www.instagram.com/mindinmotionpro', 'https://vimeo.com/mindinmotionpro',
               'https://www.youtube.com/@mindinmotionpro', 'https://www.facebook.com/mindinmotionpro',
               'https://www.linkedin.com/company/mindinmotion'],
}
# The live Portfolio's video list for search (VideoObject), carried over as it is on mindinmotion.tv.
PORTFOLIO_VIDEOS = json.loads((HERE / 'portfolio-videos.json').read_text())


def ld(page):
    slug = page['slug']
    url = LIVE + ('/' + slug if slug != 'index' else '/')
    graph = [BUSINESS,
             {'@type': 'WebPage', '@id': url + '#page', 'url': url, 'name': page['title'],
              'description': page['desc'], 'about': {'@id': LIVE + '/#business'}}]
    if page.get('crumbs'):
        linked = [(n, s) for n, s in page['crumbs'] if s is not None]
        graph.append({'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': LIVE + ('/' + s if s else '/')}
            for i, (n, s) in enumerate(linked)]})
    if page.get('service'):
        graph.append({'@type': 'Service', 'serviceType': page['service'], 'provider': {'@id': LIVE + '/#business'},
                      'areaServed': BUSINESS['areaServed'], 'url': url})
    if page.get('videos'):
        graph.append(page['videos'])
    if page.get('faq'):
        graph.append({'@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': re.sub('<[^>]+>', '', a)}}
            for q, a in page['faq']]})
    return json.dumps({'@context': 'https://schema.org', '@graph': graph}, indent=1, ensure_ascii=False)


CHEV = '<svg viewBox="0 0 10 10" aria-hidden="true"><path d="M1 3l4 4 4-4"/></svg>'


def header(slug, over=False):
    def cur(s):
        return ' aria-current="page"' if s == slug else ''
    svc_cur = ' class="cur"' if slug in SERVICE_SLUGS else ''
    dd = ''.join('<li><a href="%s.html"%s>%s</a></li>' % (s, cur(s), t if t != 'Post-Production' else 'Post-Production') for s, t in SERVICES)
    msub = ''.join('<li class="sub"><a href="%s.html"%s>%s</a></li>' % (s, cur(s), t) for s, t in SERVICES)
    return f'''<header class="hdr{' over' if over else ''}">
  <div class="wrap">
    <a class="brand" href="index.html"{cur('index')}><img src="{A}mindinmotion-logo.png" width="30" height="30" alt="">MindInMotion</a>
    <nav aria-label="Main">
      <ul class="nav">
        <li><a href="portfolio.html"{cur('portfolio')}>Portfolio</a></li>
        <li{svc_cur}><button class="dd-btn" type="button" aria-expanded="false" aria-controls="dd-svc">Services {CHEV}</button>
          <ul class="dd-menu" id="dd-svc">{dd}</ul></li>
        <li><a href="about.html"{cur('about')}>About</a></li>
        <li><a href="contact.html"{cur('contact')}>Contact</a></li>
      </ul>
    </nav>
    <a class="hdr-tel" href="tel:+14435275181">(443) 527-5181</a>
    <a class="btn" href="contact.html">Get a Quote</a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="mnav">Menu</button>
  </div>
</header>
<div class="mnav" id="mnav" role="dialog" aria-modal="true" aria-label="Menu">
  <div class="mnav-top">
    <a class="brand" href="index.html"><img src="{A}mindinmotion-logo.png" width="30" height="30" alt="">MindInMotion</a>
    <button class="mnav-close" type="button">Close</button>
  </div>
  <ul>
    <li><a href="index.html"{cur('index')}>Home</a></li>
    <li><a href="portfolio.html"{cur('portfolio')}>Portfolio</a></li>
    <li class="mnav-label">Services</li>
    {msub}
    <li><a href="about.html"{cur('about')}>About</a></li>
    <li><a href="contact.html"{cur('contact')}>Contact</a></li>
  </ul>
  <div class="mnav-foot">
    <a class="btn btn-solid" href="contact.html">Get a Quote</a>
    <a class="tel" href="tel:+14435275181">(443) 527-5181</a>
  </div>
</div>'''


FOOTER = f'''<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="brand" href="index.html"><img src="{A}mindinmotion-logo.png" width="30" height="30" alt="">MindInMotion</a>
        <p class="foot-tag">Creative Production &amp; Post</p>
      </div>
      <div>
        <p class="foot-h">Services</p>
        <ul>{''.join('<li><a href="%s.html">%s</a></li>' % (s, t) for s, t in SERVICES)}</ul>
      </div>
      <div>
        <p class="foot-h">Baltimore</p>
        <address><a href="https://g.page/r/Cebm122V_KOAEAE" target="_blank" rel="noopener">3617 Chestnut Ave<br>Baltimore, MD 21211</a><br>
        <a href="tel:+14435275181">(443) 527-5181</a><br>
        <a href="mailto:mindinmotionpro@gmail.com">mindinmotionpro@gmail.com</a></address>
      </div>
      <div>
        <p class="foot-h">Follow</p>
        <ul>
          <li><a href="https://vimeo.com/mindinmotionpro" target="_blank" rel="noopener">Vimeo</a></li>
          <li><a href="https://www.youtube.com/@mindinmotionpro" target="_blank" rel="noopener">YouTube</a></li>
          <li><a href="https://www.instagram.com/mindinmotionpro" target="_blank" rel="noopener">Instagram</a></li>
          <li><a href="https://www.facebook.com/mindinmotionpro" target="_blank" rel="noopener">Facebook</a></li>
          <li><a href="https://www.linkedin.com/company/mindinmotion" target="_blank" rel="noopener">LinkedIn</a></li>
          <li><a href="https://www.imdb.com/name/nm4644677/" target="_blank" rel="noopener">IMDb</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-base">
      <p>&copy; 2026 MindInMotion. All rights reserved.</p>
      <p><a href="{LIVE}/privacy-policy">Privacy</a></p>
    </div>
  </div>
</footer>'''

PLAYER = '''<dialog class="player" id="player" aria-labelledby="player-title">
  <div class="player-head"><p class="player-title ui" id="player-title" style="font-size:16px;letter-spacing:0;font-weight:700">Video</p><button class="player-close" type="button">Close</button></div>
  <div class="player-frame"></div>
</dialog>'''

FONTS = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Libre+Franklin:wght@400;700&display=swap" rel="stylesheet">'''


def page_html(page, body):
    slug = page['slug']
    canon = LIVE + ('/' if slug == 'index' else '/' + slug)
    preload = ''
    if page.get('preload'):
        preload = '<link rel="preload" as="image" href="%s"%s fetchpriority="high">' % (
            page['preload'], ' imagesrcset="%s" imagesizes="100vw"' % page['preload_srcset'] if page.get('preload_srcset') else '')
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- Review copy: hidden from search engines. At launch, drop this line; the live pages use index, follow. -->
<meta name="robots" content="noindex, nofollow, noarchive">
<title>{e(page['title'])}</title>
<meta name="description" content="{e(page['desc'])}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="MindInMotion">
<meta property="og:title" content="{e(page.get('og_title', page['title']))}">
<meta property="og:description" content="{e(page.get('og_desc', page['desc']))}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{LIVE}/images/og-share.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:type" content="image/jpeg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(page.get('og_title', page['title']))}">
<meta name="twitter:description" content="{e(page.get('og_desc', page['desc']))}">
<meta name="twitter:image" content="{LIVE}/images/og-share.jpg">
<meta name="theme-color" content="#000000">
<link rel="icon" type="image/png" href="{A}mindinmotion-logo.png">
{FONTS}
{preload}
<link rel="stylesheet" href="site.css">
<script type="application/ld+json">
{ld(page)}
</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header(slug, over=(slug == 'index'))}
<main id="main">
{body}
</main>
{FOOTER}
{PLAYER}
<script src="site.js"></script>
</body>
</html>
'''


# ---------------------------------------------------------------- building blocks
# Banner reels for the service pages (Victor, 2026-10-15: every service but Post). Put a Vimeo ID here and
# the banner plays it muted and looped behind the heading, as the homepage hero does; until then the still shows.
SVC_REELS = {
    'commercial-video-production': None,
    'corporate-video-production': None,
    'film-production': None,
}
# The running timecode, the one idea kept from concept D: the viewer's time of day at 24 frames a second, in grey.
TC = '<p class="tc" aria-hidden="true"><span class="tc-lbl">TC</span> <span class="tc-val">00:00:00:00</span></p>'


def phero(img_src, alt, h1, sub, ctas, crumbs=None, short=False, pos=None, bare=False):
    """Inner-page hero. Breadcrumbs are not drawn; the page's crumbs still go out as BreadcrumbList JSON-LD.
    bare=True opens straight on the heading with no picture or buttons, as Squarespace's Portfolio and Contact did."""
    if bare:
        return f'''
  <section class="phero bare">
    <div class="wrap">
      <h1>{h1}</h1>
      <p class="lede">{sub}</p>
    </div>
  </section>'''
    b = ''.join('<a class="btn%s" href="%s"%s>%s</a>' % (' btn-solid' if solid else '', href, extra, t) for href, t, solid, extra in [
        (c[0], c[1], c[2], c[3] if len(c) > 3 else '') for c in ctas])
    svc = bool(crumbs) and len(crumbs) > 2 and crumbs[1][0] == 'Services'
    pic = img(img_src, alt, lazy=False, pos=pos, extra='fetchpriority="high"')
    reel = SVC_REELS.get(crumbs[-1][1]) if svc else None
    media = '<div class="hero-media" data-bg="%s">%s</div>' % (reel, pic) if reel else pic
    return f'''
  <section class="phero{' short' if short else ''}">
    {media}
    <div class="wrap">
      <h1>{h1}</h1>
      <p class="lede">{sub}</p>
      <div class="btns">{b}</div>
    </div>{TC if svc else ''}
  </section>'''


def reel_btn(text='Watch Our Reel', solid=False):
    return '<button class="btn%s" type="button" data-vimeo="851026180" data-title="MindInMotion demo reel">%s</button>' % (' btn-solid' if solid else '', text)


def copy_split(h2, lede, paras, side, hid, alt=False, rev=False):
    if not h2:
        # Service-page intros: plain paragraphs in one column, read as running text (Victor, 2026-10-16:
        # the big first line beside smaller text "seems weird").
        ps = ''.join('<p>%s</p>' % p for p in ([lede] if lede else []) + paras)
        return f'''
  <section class="sec">
    <div class="wrap intro-text">
      <div class="prose">{ps}</div>
      <div class="intro-side">{side}</div>
    </div>
  </section>'''
    h = '<h2 id="%s" class="h2">%s</h2>' % (hid, h2) if h2 else ''
    ps = ''.join('<p>%s</p>' % p for p in paras)
    ld_ = '<p class="lede intro-lede">%s</p>' % lede if lede else ''
    return f'''
  <section class="sec"{' aria-labelledby="%s"' % hid if h2 else ''}>
    <div class="wrap split intro{' rev' if rev else ''}">
      <div>
        {h}
        {ld_}
      </div>
      <div>
        <div class="prose">{ps}</div>
        <div class="intro-side">{side}</div>
      </div>
    </div>
  </section>'''


def feature(w_key, client, title, sub=None, kind=None, desc=None, alt_override=None, body=None, deliv=None, eager=False):
    w = dict(W[w_key])
    if alt_override:
        w['alt'] = alt_override
    t = e(title) + (' &ndash; %s' % e(sub) if sub else '')
    k = '<p class="meta">%s</p>' % (kind or e(client)) if (kind or client) else ''
    dsc = '<p class="d">%s</p>' % desc if desc else ''
    bd = '<div class="prose">%s</div>' % ''.join('<p>%s</p>' % p for p in body) if body else ''
    dl = '<dl><dt>Deliverables</dt><dd>%s</dd></dl>' % deliv if deliv else ''
    return f'''
      <article class="feat">
        <div>{frame(w, eager=eager)}</div>
        <div class="feat-body">
          <h3>{t}</h3>
          {k}{dsc}{bd}{dl}
        </div>
      </article>'''


def feature_sec(h2, hid, items, alt=False, lede=None):
    ld_ = '<p class="lede">%s</p>' % lede if lede else ''
    return f'''
  <section class="sec{' alt' if alt else ''}" aria-labelledby="{hid}">
    <div class="wrap">
      <div class="sec-head{' solo' if not lede else ''}"><h2 id="{hid}" class="h2">{h2}</h2>{ld_}</div>
      {''.join(items)}
    </div>
  </section>'''


def quote_block(q, who, role, alt=False):
    return f'''
  <section class="sec{' alt' if alt else ''}" aria-label="What a client said">
    <div class="wrap">
      <figure class="quote solo">
        <blockquote><p>{q}</p></blockquote>
        <figcaption><b>{who}</b><span>{role}</span></figcaption>
      </figure>
    </div>
  </section>'''


TESTIMONIALS = [
    ('Not only are Josh and Victor an amazing creative team with a TON of knowledge on every facet of filmmaking, they&#39;re just great people.', 'Chris Perillo', 'Director'),
    ('MindInMotion are terrifically talented. Easy to work with. And really care about the quality of their work.', 'Matthew White', 'FIVES'),
    ('They go the extra mile to create the best content and offer helpful input on ways to create the most appealing video for our audience.', 'Patrick Moody', 'Director of Marketing, Johns Hopkins AAP'),
    ('Super professional, a lot of fun to work with and always on schedule. Would recommend them for virtually any project!', 'Nate Lanzino', 'Entrepreneur'),
]


# Newest Google reviews, word for word (Joshua picked them 2026-10-16; full text from Google Maps 2026-10-19). Long ones run across both columns.
NEW_REVIEWS = [
    ("We've had the pleasure of working with Victor and Josh at MindInMotion for the past several years on multiple projects requiring different needs. They make thoughtful recommendations and we can always count on them to provide the highest quality service. Outside of their technical expertise, they are professional, punctual and responsive. We highly recommend them for any video production needs and look forward to collaborating with them for years to come.", 'Infinite Legacy', 'Google review'),
    ("It's always a pleasure to work with Josh, Victor, and the Mind in Motion team. Our organization has partnered with them on roughly 10 video projects over the past five to six years, and they have delivered exceptional work on every one. I'm continually impressed by their ability to transform our initial ideas into compelling, engaging stories. Their professionalism is evident at every stage of the process, from listening carefully to our goals and putting video subjects at ease to coordinating every detail of production and thoughtfully refining the final product until it's exactly what we envisioned - and often even better.", 'Cara McCandless', 'Google review'),
    ("Victor and the MindInMotion team are top notch. Not only are they technically gifted videographers, but they're also great communicators and project managers. We have hired them for several projects now to tell the stories of our science grantees, and we're always very satisfied with their work.", 'Gabe Medina', 'Schmidt Sciences, Google review'),
]


def quotes_sec(alt=False, hid='h-words'):
    qs = ''.join('''
        <figure class="quote long">
          <blockquote><p>%s</p></blockquote>
          <figcaption><b>%s</b><span>%s</span></figcaption>
        </figure>''' % (e(q), w, r) for q, w, r in NEW_REVIEWS)
    qs += ''.join('''
        <figure class="quote">
          <blockquote><p>%s</p></blockquote>
          <figcaption><b>%s</b><span>%s</span></figcaption>
        </figure>''' % t for t in TESTIMONIALS)
    return f'''
  <section class="sec{' alt' if alt else ''}" aria-labelledby="{hid}">
    <div class="wrap">
      <div class="sec-head solo"><h2 id="{hid}" class="h2">What Our Clients Say</h2></div>
      <div class="quotes">{qs}
      </div>
    </div>
  </section>'''


def slideshow(hid, title, folder_or_list, intro=None, interval=3500):
    """Behind-the-scenes photos that advance on their own. Pauses on hover, keyboard focus, when off screen,
    and for visitors who ask for reduced motion. The first two load straight away, the rest one step ahead."""
    figs = []
    for k, (src, alt) in enumerate(folder_or_list):
        w, h = dims(src)
        if k < 2:
            im = '<img src="%s" width="%d" height="%d" alt="%s" decoding="async"%s>' % (src, w, h, e(alt), '' if k == 0 else ' loading="lazy"')
        else:
            im = '<img data-src="%s" width="%d" height="%d" alt="%s" decoding="async">' % (src, w, h, e(alt))
        cls = ' '.join(c for c in ('on' if k == 0 else '', 'tall' if h > w else '') if c)
        figs.append('<figure%s>%s</figure>' % (' class="%s"' % cls if cls else '', im))
    head = ''
    if title:
        it = '<p class="lede">%s</p>' % intro if intro else ''
        head = f'''
    <div class="wrap show-head">
      <div class="sec-head{' solo' if not intro else ''}" style="margin-bottom:0"><h2 id="{hid}" class="h2">{title}</h2>{it}</div>
    </div>'''
    return f'''
  <section aria-labelledby="{hid}" class="show-sec">{head}
    <div class="wrap"><div class="show" data-interval="{interval}" role="region" aria-roledescription="carousel" aria-label="{e(title or 'Behind the scenes')} photos">
      <div class="show-stage">
        {''.join(figs)}
      </div>
      <div class="show-bar">
        <div class="show-ctl">
          <button class="prev" type="button" aria-label="Previous photo"><svg viewBox="0 0 14 14" aria-hidden="true"><path d="M9 2L4 7l5 5"/></svg></button>
          <button class="next" type="button" aria-label="Next photo"><svg viewBox="0 0 14 14" aria-hidden="true"><path d="M5 2l5 5-5 5"/></svg></button>
        </div>
      </div>
    </div></div>
  </section>'''


def bts(folder, items):
    return [(A + 'bts/%s/%s' % (folder, f), alt) for f, alt in items]


BTS_COMMERCIAL = bts('commercial', [
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
])
BTS_CORPORATE = bts('corporate', [
    ('01-studio-teleprompter.webp', 'Woman filmed in studio with lighting rig, teleprompter and monitors'),
    ('02-white-studio.webp', 'Wide view of a white studio set up for an interview'),
    ('03-monitor-interview.webp', 'Camera crew with a monitor showing a woman being interviewed'),
    ('04-narrow-room-interview.webp', 'Woman seated for an interview with camera and lights in a narrow room'),
    ('05-studio-interview.webp', 'Woman standing for interview shoot in front of green screen'),
    ('06-ballroom-interview.webp', 'Multi-camera interview setup with a woman seated in a hotel ballroom'),
])
BTS_FILM = bts('film', [
    ('01-gravel-road-scene.webp', 'Crew filming an actor with stage blood on a gravel road'),
    ('02-forest-scene.webp', 'Camera operator filming two actors sitting in a palmetto forest'),
    ('03-palmetto-forest.webp', 'Crew holding reflector and camera rig in palmetto forest location'),
    ('04-forest-floor.webp', 'Actors in a scene on a forest floor with crew behind them'),
    ('05-monitor-closeup.webp', 'On-camera monitor showing an actor on the forest floor'),
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
])
# The homepage uses the 17 photos the live site and Squarespace show there, in the live order.
BTS_HOME = bts('home', [
    ('01-crew-monitor-outdoors.webp', 'Crew gathered around a camera monitor during an outdoor shoot'),
    ('02-dolly-track.webp', 'Camera operator on dolly track filming alongside lighting setup outdoors'),
    ('03-hillside-boom.webp', 'Film crew hiking foggy hillside with boom mic in black-and-white'),
    ('04-living-room-monitor.webp', 'Video monitor showing family scene being filmed in a living room'),
    ('05-living-room-crew.webp', 'Film crew shooting family scene on couch in living room set'),
    ('06-teal-set.webp', 'Crew filming with camera rig in a teal-lit bathroom set'),
    ('07-bedroom-monitor.webp', "Two crew members smiling behind camera monitor in a child's bedroom"),
    ('08-house-porch.webp', 'Film crew with boom mic capturing scene on a house porch'),
    ('09-studio-teleprompter.webp', 'Woman filmed in studio with lighting rig, teleprompter and monitors'),
    ('10-studio-interview.webp', 'Woman standing for interview shoot in front of green screen'),
    ('11-forest-camera.webp', 'Two crew members checking a camera rig at the edge of a forest'),
    ('12-color-suite.webp', 'Close-up of color grading control panel and monitors in edit suite'),
    ('13-hotel-interview.webp', 'Woman seated for on-camera interview in a conference room setup'),
    ('14-field-interview.webp', 'Interview set up with lights and camera in an open field'),
    ('15-palmetto-forest.webp', 'Crew holding reflector and camera rig in palmetto forest location'),
    ('16-wooded-set-boom.webp', 'Boom operator and crew filming an actor outdoors on a wooded set'),
    ('17-gravel-road-scene.webp', 'Crew filming an actor with stage blood on a gravel road'),
])

SVC_COPY = {
    'commercial-video-production': ('Commercial', 'TV spots, social media ads, and branded content. We&#39;ve created campaigns for clients like Maryland State Department of Education that reach millions of viewers across broadcast and digital.', A + 'Screen-Shot-2022-06-24-at-6.14.31-PM-2.webp', 'A woman in a dark bathroom at night, from the Maryland Excels "Good Mom" spot.'),
    'corporate-video-production': ('Corporate', 'Recruitment videos, training content, testimonials, and internal communications. Trusted by Johns Hopkins, Anne Arundel County Police, and InterPublic.', A + 'residency.webp', 'A woman looks up in a wood-paneled library, from a Johns Hopkins AAP film.'),
    'film-production': ('Film', 'Feature films, documentaries, music videos, and narrative projects. Our films "I Like Me" and "Bad Witch" have screened at festivals worldwide and stream on major VOD platforms.', A + 'bad-witch.webp', 'A young man at dusk in hard orange light, from Bad Witch.'),
    'post-production': ('Post-Production', 'Expert editing, color grading, and VFX using Final Cut Pro, Premiere, Avid, and DaVinci Resolve.', A + '011A1257-2.webp', 'A color grading panel and keyboard on a wooden desk, seen from above.'),
}


def services_sec(alt=False, exclude=None, h2='Full-Service Production', lede=None, hid='h-svc'):
    cards = []
    for s, _ in SERVICES:
        if s == exclude:
            continue
        t, d, im, alt_ = SVC_COPY[s]
        cards.append(f'''
        <li class="svc">
          <a class="svc-img" href="{s}.html" tabindex="-1" aria-hidden="true">{img(im, '')}</a>
          <h3><a href="{s}.html">{t}</a></h3>
          <p>{d}</p>
        </li>''')
    ld_ = '<p class="lede">%s</p>' % lede if lede else ''
    return f'''
  <section class="sec{' alt' if alt else ''}" aria-labelledby="{hid}">
    <div class="wrap">
      <div class="sec-head{' solo' if not lede else ''}"><h2 id="{hid}" class="h2">{h2}</h2>{ld_}</div>
      <ul class="svcs">{''.join(cards)}
      </ul>
    </div>
  </section>'''


def related(this):
    links = []
    for s, t in SERVICES:
        if s == this:
            continue
        links.append('<a href="%s.html"><b>%s</b><span>%s</span></a>' % (s, t, SVC_COPY[s][1]))
    return f'''
  <section class="sec" aria-labelledby="h-related">
    <div class="wrap">
      <div class="sec-head solo"><h2 id="h-related" class="h2">Production and post</h2></div>
      <nav class="related" aria-labelledby="h-related">{''.join(links)}</nav>
    </div>
  </section>'''


def closing(h2='Tell us about your project', lede='Get a custom quote within 24 hours.', btn='Get Your Free Quote', alt=True, second=None):
    two = second or '<a class="btn" href="tel:+14435275181">(443) 527-5181</a>'
    return f'''
  <section class="sec" aria-labelledby="h-close">
    <div class="wrap">
      <div class="close-sec">
        <h2 id="h-close">{h2}</h2>
        <p class="lede">{lede}</p>
        <div class="btns"><a class="btn btn-solid" href="contact.html">{btn}</a>{two}</div>
      </div>
    </div>
  </section>'''


def closing_form():
    """The homepage ends with a short quote form beside the closing heading, as Squarespace's did.
    It is its own Netlify form (contact-home) and posts to the same thank-you page as the Contact form."""
    return f'''
  <section class="sec" aria-labelledby="h-close">
    <div class="wrap close-form">
      <div class="close-sec">
        <h2 id="h-close">Tell us about your project</h2>
        <p class="lede">Get a custom quote within 24 hours.</p>
        <div class="btns"><a class="btn" href="tel:+14435275181">(443) 527-5181</a></div>
      </div>
      <form class="form form-short" name="contact-home" method="POST" action="thank-you" data-netlify="true" netlify-honeypot="bot-field">
        <input type="hidden" name="form-name" value="contact-home">
        <p class="hp"><label>Don't fill this out: <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
        <div class="field full"><label for="q-name">Your Name *</label><input id="q-name" name="name" autocomplete="name" required></div>
        <div class="field"><label for="q-email">Email Address *</label><input id="q-email" name="email" type="email" autocomplete="email" required></div>
        <div class="field"><label for="q-phone">Phone Number</label><input id="q-phone" name="phone" type="tel" autocomplete="tel"></div>
        <div class="field full"><label for="q-msg">Tell Us About Your Project *</label><textarea id="q-msg" name="message" required placeholder="What are you making, who is it for, and when do you need it?"></textarea></div>
        <p class="note full">By submitting this form, you agree that MindInMotion may use the information you provide to respond to your inquiry. Read our <a href="{LIVE}/privacy-policy">Privacy Policy</a>.</p>
        <button class="btn btn-solid full" type="submit">Get My Free Quote</button>
        <p class="form-status full" role="status" tabindex="-1" hidden></p>
      </form>
    </div>
  </section>'''


def grid_sec(h2, hid, lede, grid_html, alt=False):
    ld_ = '<p class="lede">%s</p>' % lede if lede else ''
    return f'''
  <section class="sec{' alt' if alt else ''}" aria-labelledby="{hid}">
    <div class="wrap">
      <div class="sec-head{' solo' if not lede else ''}"><h2 id="{hid}" class="h2">{h2}</h2>{ld_}</div>
      {grid_html}
    </div>
  </section>'''


# ================================================================ PAGES
PAGES = []
ALL_WORK = ['quality', 'joe', 'cuba', 'ashley', 'aacpd', 'wellpoint', 'eng', 'packard', 'chelsea',
            'goodmom', 'wouldnt', 'checklist', 'playground', 'illegal', 'bennetts',
            'residency', 'layne', 'odom', 'tidewater', 'risingtide',
            'sydney', 'lungforce', 'pearlstone', 'cdspg', 'finding',
            'lotus', 'ilikeme', 'badwitch', 'ape', 'incubation', 'farmhouse', 'hiking',
            'ghost', 'cyw', 'lovers', 'thunder']
# Portfolio's All Work opens as Squarespace's did; the four Featured Projects come after the client work.
PORTFOLIO_OPEN = ['reel', 'goodmom', 'playground', 'aacpd', 'ghost', 'farmhouse']
PORTFOLIO_FEATURED = ['quality', 'chelsea', 'cuba', 'ashley']
_rest = [k for k in ALL_WORK if k not in PORTFOLIO_OPEN + PORTFOLIO_FEATURED]
PORTFOLIO_ORDER = PORTFOLIO_OPEN + _rest[:_rest.index('lotus')] + PORTFOLIO_FEATURED + _rest[_rest.index('lotus'):]
# The live homepage's featured eight, in its order (its ninth tile, the reel, is the hero button here).
HOME_ALL = ['eng', 'cuba', 'checklist', 'aacpd', 'ashley', 'joe', 'chelsea', 'packard']
HOME_SKIP = ['bennetts']   # Victor, 2026-10-16: not homepage material (still on Commercial and Portfolio)
HOME_TITLES = {'eng': 'Johns Hopkins Engineering Management', 'cuba': 'Cuba Field Course Experience'}

# ---------------------------------------------------------------- home
HOME_BODY = f'''
  <section class="hero" aria-labelledby="h-hero">
    <div class="hero-media" data-bg="848454220">
      <img src="{L}hero-poster-1920.webp" srcset="{L}hero-poster-960.webp 960w, {L}hero-poster-1920.webp 1920w" sizes="100vw" width="1920" height="1080" alt="" fetchpriority="high">
    </div>
    <div class="wrap hero-body">
      <h1 id="h-hero">We are MindInMotion</h1>
      <p class="lede">We Create, Produce, Direct, Film, and Edit. Let&#39;s Create Something Amazing Together.</p>
      <div class="btns">{reel_btn(solid=True)}<a class="btn" href="contact.html">Get a Quote in 24 Hours</a></div>
    </div>
  </section>
{logo_row()}
{grid_sec('Featured Projects', 'h-work', None,
          work_grid(HOME_ALL + [k for k in ALL_WORK if k not in HOME_ALL + HOME_SKIP], 'home-grid', all_keys=HOME_ALL, filters=[('all', 'Featured')] + FILTERS[1:4], meta=False, titles=HOME_TITLES,
                    foot='<a class="text-link" href="portfolio.html">View All Projects</a>'))}
{services_sec()}
{slideshow('h-bts', 'Behind the Scenes', BTS_HOME)}
  <section class="sec" aria-labelledby="h-about">
    <div class="wrap">
      <div class="sec-head solo"><h2 id="h-about" class="h2">About MindInMotion</h2></div>
      <div class="split pair">
      <div>
        <div class="prose">
          <p>MindInMotion was founded by Baltimore native Joshua Land and Boston transplant Victor Fink in 2012. We met in a 16mm filmmaking class in college.</p>
          <p>Since then we've made our own feature films together and grown a company that makes film and video for clients. We've shot documentary and fiction in Baltimore, Washington DC, the mountains of Washington state and the rainforests of Cuba.</p>
          <p>Our feature films "I Like Me" and "Bad Witch" have screened at festivals across the world and are available to view on all major VOD platforms. Our new feature film, "Incubation", is now screening at festivals.</p>
        </div>
        <p style="margin-top:24px"><a class="text-link" href="about.html">Read Our Full Story</a></p>
      </div>
      <figure>
        {img(A + 'DSCF2928.webp', 'Josh, left, and Victor on a wooded set. Victor holds a cinema camera with a monitor on top.')}
        <figcaption class="meta cap">Josh (left) and Victor on set</figcaption>
      </figure>
      </div>
    </div>
  </section>
{quotes_sec()}
{closing_form()}'''

PAGES.append(dict(
    slug='index',
    title='Video Production Baltimore | MindInMotion',
    desc='Award-winning video production in Baltimore. Commercials, corporate videos & films since 2012. Get a free quote within 24 hours.',
    og_title='MindInMotion - Video Production Baltimore',
    og_desc='Award-winning video production company creating commercials, corporate videos, and films. Serving Baltimore and the Mid-Atlantic since 2012.',
    preload=L + 'hero-poster-1920.webp',
    preload_srcset=L + 'hero-poster-960.webp 960w, ' + L + 'hero-poster-1920.webp 1920w',
    body=HOME_BODY))

# ---------------------------------------------------------------- commercial
PAGES.append(dict(
    slug='commercial-video-production',
    title='Commercial Video Production | MindInMotion',
    desc='TV commercials, digital ads & brand videos. Award-winning commercial video production in Baltimore. Request a free quote today.',
    og_desc='TV commercials, digital ads, and brand videos in Baltimore.',
    crumbs=[('Home', ''), ('Services', None), ('Commercial', 'commercial-video-production')],
    service='Commercial video production',
    preload=A + 'Screenshot-2024-01-18-at-2.56.49-PM.webp',
    body=''.join([
        # Header stills are frames that aren't in the page's own grid, as Squarespace's header footage wasn't.
        phero(A + 'Screenshot-2024-01-18-at-2.56.49-PM.webp', 'Two young girls play in a purple and yellow toy car outdoors.',
              'Commercial Video Production', 'TV spots, PSAs, recruitment ads and social cuts.',
              [('contact.html', 'Tell Us About Your Project', True)],
              crumbs=[('Home', ''), ('Services', None), ('Commercial', 'commercial-video-production')], pos='50% 40%'),
        copy_split(None,
                   "MindInMotion handles commercial video production in Baltimore for broadcast TV, streaming platforms, YouTube pre-roll and social feeds. Some spots come through ad agencies, like our WellPoint spot for InterPublic. Others we make directly for the client, like the Maryland Excels PSAs for the Maryland State Department of Education.",
                   ["Josh and Victor also direct feature films. They plan the lighting, camera moves and performances in a 15-second social cut or a 60-second broadcast spot the same way they do on their features.",
                    "The same team plans, shoots, edits and colors your spot, from script to delivery. If you have a campaign coming up, <a href=\"contact.html\">tell us about it</a>."],
                   '<div class="btns">%s</div>' % reel_btn(), 'h-intro'),
        grid_sec('Selected Work', 'h-work', 'A few of the commercials we’ve produced.',
                 work_grid(['goodmom', 'aacpd', 'wouldnt', 'checklist', 'wellpoint', 'playground', 'illegal', 'bennetts'], 'work-grid', meta=False,
                           titles=SVC_TITLES, foot=GRIDFOOT % 'Have a campaign in mind?')),
        quote_block('Super professional, a lot of fun to work with and always on schedule. Would recommend them for virtually any project!', 'Nate Lanzino', 'Entrepreneur'),
        slideshow('h-bts', 'Behind the Scenes', BTS_COMMERCIAL),
        closing(),
    ])))

# ---------------------------------------------------------------- corporate
PAGES.append(dict(
    slug='corporate-video-production',
    title='Corporate Video Production | MindInMotion',
    desc='Training videos, testimonials & internal communications. Corporate video production in Baltimore trusted by Johns Hopkins. Get a free quote.',
    og_desc='Training videos, testimonials, and corporate communications in Baltimore.',
    crumbs=[('Home', ''), ('Services', None), ('Corporate', 'corporate-video-production')],
    service='Corporate and nonprofit video production',
    preload=A + 'Screen-Shot-2019-12-11-at-3.34.02-PM-copy.webp',
    body=''.join([
        phero(A + 'Screen-Shot-2019-12-11-at-3.34.02-PM-copy.webp', 'From the Cuba field course film: two hikers with backpacks below green mountains.',
              'Corporate Video Production', "Videos to train a team, tell a patient's story, or show donors where their money goes.",
              [('contact.html', 'Tell Us About Your Project', True)],
              crumbs=[('Home', ''), ('Services', None), ('Corporate', 'corporate-video-production')], pos='62% 30%'),
        copy_split(None,
                   "Our corporate video production work includes training modules for hospital systems, testimonial campaigns for nonprofits, recruitment videos for universities, and internal communications for organizations that want their employees to watch.",
                   ["Our approach comes from documentary filmmaking. We interview the people involved with a small crew, and film b-roll at your own locations.",
                    "We've worked with Johns Hopkins, the Maryland State Department of Education, healthcare systems, and dozens of nonprofits and foundations across the Mid-Atlantic. <a href=\"contact.html\">Tell us what you're working on</a>."],
                   '<div class="btns">%s</div>' % reel_btn(), 'h-intro'),
        grid_sec('Selected Work', 'h-work', 'Recruitment, training, and brand films for organizations across the Mid-Atlantic.',
                 work_grid(['eng', 'chelsea', 'quality', 'finding', 'tidewater', 'cuba', 'joe', 'pearlstone', 'risingtide', 'packard', 'cdspg', 'residency', 'odom', 'ashley', 'sydney'], 'work-grid', meta=False,
                           titles=SVC_TITLES, foot=GRIDFOOT % 'Have a project in mind?')),
        quote_block('They go the extra mile to create the best content and offer helpful input on ways to create the most appealing video for our audience.', 'Patrick Moody', 'Director of Marketing, Johns Hopkins AAP'),
        slideshow('h-bts', 'Behind the Scenes', BTS_CORPORATE),
        closing(),
    ])))

# ---------------------------------------------------------------- film
FILM_GROUPS = [
    ('Feature films', [('lotus', 'Lotus Eyes'), ('ilikeme', 'I Like Me'), ('badwitch', 'Bad Witch'),
                       ('ape', 'Ape Canyon'), ('incubation', 'Incubation (teaser)')]),
    ('Short films', [('farmhouse', 'The Farmhouse'), ('hiking', "Don't Go Hiking")]),
    ('Music videos', [('ghost', 'Juliet Lloyd - Ghost Light'), ('cyw', 'Juliet Lloyd - Call Your Wife'),
                      ('lovers', 'Fives - Lovers in Lullaby'), ('thunder', 'FIVES - Heart &amp; Thunder')]),
]


def films_sec(hid='h-films', h2='Feature films, shorts and music videos', alt=False):
    groups = []
    for gname, rows in FILM_GROUPS:
        tiles = []
        for key, t in rows:
            w = W[key]
            tiles.append('''
          <li class="tile">
            %s
            <div class="tile-cap">
              <h4 class="tile-t">%s</h4>
            </div>
          </li>''' % (frame(w), t))
        groups.append('''
      <div class="film-group">
        <h3>%s</h3>
        <ul class="grid">%s
        </ul>
      </div>''' % (gname, ''.join(tiles)))
    return f'''
  <section class="sec{' alt' if alt else ''}" id="films" aria-labelledby="{hid}">
    <div class="wrap">
      <div class="sec-head solo"><h2 id="{hid}" class="h2">{h2}</h2></div>
      {''.join(groups)}
    </div>
  </section>'''


PAGES.append(dict(
    slug='film-production',
    title='Film Production Baltimore | MindInMotion',
    desc='Feature films, documentaries & narrative projects from award-winning filmmakers. Our features have screened at festivals worldwide. Baltimore production.',
    og_desc='Full service film production. Feature films, shorts, and documentaries screened at festivals worldwide.',
    crumbs=[('Home', ''), ('Services', None), ('Film', 'film-production')],
    service='Film production',
    preload=A + 'heart-thunder-fog.webp',
    body=''.join([
        phero(A + 'heart-thunder-fog.webp', 'From the FIVES video Heart & Thunder: a drummer mid-hit, backlit in blue haze.',
              'Film Production', 'Production and post-production support for features, shorts, documentaries, and music videos.',
              [('contact.html', 'Tell Us About Your Project', True)],
              crumbs=[('Home', ''), ('Services', None), ('Film', 'film-production')], pos='50% 40%'),
        copy_split(None,
                   'MindInMotion is a full-service film production company in Baltimore, Maryland. We produce and finish shorts and feature films, and our own features have screened at festivals across the globe; most are on major VOD platforms.',
                   ["We can produce a whole film or join your crew for part of it, on productions in Baltimore and up and down the east coast.",
                    "We'll walk you through each step and tell you what your budget can cover. If you need help getting a film off the ground, or need to fill specific production roles, fill out the <a href=\"contact.html\">contact form</a>."],
                   '<div class="btns">%s</div>' % reel_btn(), 'h-intro'),
        films_sec(),
        quote_block('Not only are Josh and Victor an amazing creative team with a TON of knowledge on every facet of filmmaking, they&#39;re just great people.', 'Chris Perillo', 'Director'),
        slideshow('h-bts', 'Behind the Scenes', BTS_FILM),
        closing(),
    ])))

# ---------------------------------------------------------------- post
POST_ROWS = [
    ('Editing', "Our editors have cut feature films, commercials, documentaries and corporate videos. We work in DaVinci Resolve, Final Cut Pro, Premiere, and Avid."),
    ('Color Grading', 'Color correction and grading in DaVinci Resolve. We work from LOG camera footage through to the graded master.'),
    ('Sound Mixing', 'We work with sound-mixing partners for the final mix.'),
    ('VFX &amp; Motion Graphics', 'Compositing, cleanup, and motion graphics. We do standard effects in-house and bring in VFX specialists for complex shots.'),
    ('Delivery &amp; Mastering', "Final files to broadcast specs, for streaming platforms and social media, or as theatrical DCPs."),
    ('Project Rescue', 'We take over projects that have stalled or lost their editor, and finish them.'),
]
PAGES.append(dict(
    slug='post-production',
    title='Post-Production Services | MindInMotion',
    desc='Video editing, color grading & VFX in DaVinci Resolve, Premiere & Final Cut Pro. Post-production services in Baltimore. Get a quote.',
    og_desc='Editing, color grading, motion graphics, and VFX in Baltimore.',
    crumbs=[('Home', ''), ('Services', None), ('Post-Production', 'post-production')],
    service='Video post-production',
    preload=A + '011A5550.webp',
    body=''.join([
        phero(A + '011A5550.webp', 'A colorist at a grading desk in a dark edit suite, three monitors glowing in front of him.',
              'Post-Production', 'Editing, color grading, VFX and motion graphics for films, commercials and corporate video.',
              [('contact.html', 'Get a Quote', True), ('#h-work', 'See Our Work', False)],
              crumbs=[('Home', ''), ('Services', None), ('Post-Production', 'post-production')], pos='50% 45%'),
        f'''
  <section class="sec" aria-labelledby="h-post">
    <div class="wrap split">
      <div>
        <h2 id="h-post" class="h2">Our Services</h2>
        <p class="lede" style="margin-bottom:32px">We're based in Baltimore and have edited and colored feature films and commercials for more than a decade. We can run the full post workflow or take on one piece of it, like color or VFX.</p>
      </div>
      <figure>{img(A + '011A1266.webp', 'A color grading panel and monitors in a dark edit suite.')}</figure>
    </div>
    <div class="wrap" style="margin-top:clamp(32px,4vw,56px)">
      <ul class="rows">{''.join('<li><h3>%s</h3><p>%s</p></li>' % r for r in POST_ROWS)}</ul>
    </div>
  </section>''',
        grid_sec('Edited and Colored In-House', 'h-work', 'We edited and colored every project on this site. Here are four.',
                 '<ul class="grid" id="post-grid">%s</ul>' % ''.join([
                     tile('goodmom', title='Maryland Excels "Good Mom"', cr='Commercial spot'),
                     tile('ghost', title='Ghost Light', cr='Music video'),
                     tile('cuba', title='Cuba Field Course', cr='Documentary'),
                     tile('checklist', title='Maryland Excels PSA', cr='PSA campaign')])),
        f'''
  <section class="sec" aria-labelledby="h-editor">
    <div class="wrap split">
      <div>
        <h2 id="h-editor" class="h2">Working With Your Editor</h2>
        <p class="lede" style="margin-bottom:1em">You'll talk to your editor directly, and we share rough cuts early in the edit.</p>
        <div class="prose"><p>Whether you’re in Baltimore or across the country, you can watch cuts, leave timestamped notes, and approve versions through secure remote review.</p></div>
      </div>
      <dl class="contact-list" style="align-self:end">
        <div><dt>Tools We Work With</dt><dd>DaVinci Resolve, Final Cut Pro, Premiere Pro, Avid Media Composer, After Effects, Fusion, Frame.io</dd></div>
      </dl>
    </div>
  </section>''',
        closing(h2='Need Post‑Production Help?', lede='Tell us about your project. Whether you need a full post workflow or just help with one piece of it, we can take it on.', btn='Get in Touch', second=''),
    ])))

# ---------------------------------------------------------------- about
# Five features in release order. The Summer Before counts but isn't shown (Joshua, 2026-10-15).
ABOUT_FILMS = [('lotus', 'Lotus Eyes', '2016'), ('ilikeme', 'I Like Me', '2018'), ('badwitch', 'Bad Witch', '2021'),
               ('ape', 'Ape Canyon', '2021'), ('incubation', 'Incubation', 'Now screening at festivals')]
POSTERS = [('still-lotus-eyes.webp', 'Lotus Eyes feature film — two leads against an industrial skyline', 'Lotus Eyes', 'Feature'),
           ('poster-i-like-me.webp', 'I Like Me feature film poster', 'I Like Me', 'Feature'),
           ('poster-ape-canyon.webp', 'Ape Canyon feature film poster', 'Ape Canyon', 'Feature'),
           ('still-bad-witch.webp', 'Bad Witch feature film — profile of a bloodied young man at dusk', 'Bad Witch', 'Feature'),
           ('poster-incubation.webp', 'Incubation feature film poster', 'Incubation', 'At Festivals')]

ABOUT_BODY = ''.join([
    phero(A + '11698893_10205059638871667_6520616449341988197_o-1.webp', 'A small crew films two actors in a graffiti-covered tunnel, a boom pole overhead.',
          'About MindInMotion', "We met in a 16mm filmmaking class at Johns Hopkins. Fourteen years later, we're still making movies and videos for clients.",
          [],
          crumbs=[('Home', ''), ('About', 'about')], pos='50% 18%'),
    f'''
  <section class="sec" aria-labelledby="h-story">
    <div class="wrap">
      <div class="sec-head solo"><h2 id="h-story" class="h2">Our Story</h2></div>
      <div class="split pair">
      <div>
        <div class="prose">
          <p>Joshua Land and Victor Fink met in a 16mm filmmaking class at Johns Hopkins University and have been collaborating ever since. Josh grew up in Baltimore; Victor in Boston. Together they co-founded MindInMotion, a video production company based in Baltimore.</p>
          <p>Over the past decade-plus, they’ve produced features, shorts, music videos, and commercials together. Their features include "Lotus Eyes," "I Like Me," "Bad Witch," "Ape Canyon" and their latest, "Incubation."</p>
          <p>Alongside their own films, they make video for nonprofits, universities, public agencies and brands. They've shot documentary and fiction in Baltimore, Washington DC, the mountains of Washington state and the rainforests of Cuba.</p>
          <p>Their feature films have screened at festivals across the world, and most are available on all major VOD platforms. "Incubation" is currently screening at festivals.</p>
        </div>
      </div>
      <figure>
        {img(A + 'Joshua-and-Victor-on-stage-1.webp', 'Josh, holding a microphone, and Victor on stage at a screening Q&A, both wearing festival lanyards.')}
        <figcaption class="meta cap">Josh (with the microphone) and Victor at a screening Q&amp;A</figcaption>
      </figure>
      </div>
    </div>
  </section>
  <section class="sec" aria-labelledby="h-how">
    <div class="wrap">
      <div class="sec-head solo"><h2 id="h-how" class="h2">How We Work</h2></div>
      <div class="split pair">
      <div>
        <ul class="rows">
          <li style="grid-template-columns:minmax(0,1fr)"><h3>Documentary Interviews</h3><p>Much of our client work is documentary. We interview the people involved and build the edit around what they say.</p></li>
          <li style="grid-template-columns:minmax(0,1fr)"><h3>Working With Josh and Victor</h3><p>You talk to us directly. We ask questions, offer ideas, and say so when we think something could be better.</p></li>
          <li style="grid-template-columns:minmax(0,1fr)"><h3>Post-Production</h3><p>We edit and color grade what we shoot, and work with sound-mixing partners for the final mix.</p></li>
        </ul>
      </div>
      <figure>{img(A + 'crew-hike-bw.webp', 'Black-and-white photo of a small crew hiking up a foggy hillside with a camera and a boom pole.')}</figure>
      </div>
    </div>
  </section>
  <section class="sec" aria-labelledby="h-team">
    <div class="wrap">
      <div class="sec-head solo"><h2 id="h-team" class="h2">Meet Josh &amp; Victor</h2></div>
      <div class="team">
        <article class="bio">
          <div class="bio-photo">{img(L + 'team-joshua-land.webp', 'Joshua Land speaking into a microphone at a screening.')}</div>
          <h3>Joshua Land</h3>
          <p class="label">Co-Founder / Director / Cinematographer / Editor</p>
          <p>Josh grew up in Baltimore and studied Film &amp; Media Studies at Johns Hopkins. He's directed features that have screened at festivals worldwide and stream on major VOD platforms.</p>
          <p>He runs post-production as MindInMotion's lead editor and colorist.</p>
          <a class="text-link" href="https://www.imdb.com/name/nm4644677/" target="_blank" rel="noopener">IMDb<span class="vh"> (Joshua Land)</span></a>
        </article>
        <article class="bio">
          <div class="bio-photo">{img(L + 'team-victor-fink.webp', 'Victor Fink on set, looking down at a camera monitor.')}</div>
          <h3>Victor Fink</h3>
          <p class="label">Co-Founder / Cinematographer / Producer</p>
          <p>Victor grew up in Boston and met Josh in that 16mm filmmaking class at Johns Hopkins. He shoots MindInMotion's features with Josh, along with dozens of commercial and corporate projects.</p>
          <a class="text-link" href="https://www.imdb.com/name/nm5227903/" target="_blank" rel="noopener">IMDb<span class="vh"> (Victor Fink)</span></a>
        </article>
      </div>
    </div>
  </section>
  <section class="sec" aria-labelledby="h-features">
    <div class="wrap">
      <div class="sec-head"><h2 id="h-features" class="h2">Our Feature Films</h2><p class="lede">Most are available on all major VOD platforms.</p></div>
      <ul class="grid g3">{''.join('<li class="tile">%s<div class="tile-cap"><h3 class="tile-t">%s</h3><p class="meta">%s</p></div></li>' % (frame(W[k]), t, y) for k, t, y in ABOUT_FILMS)}
      </ul>
      <p style="margin-top:32px"><a class="text-link" href="film-production.html#films">Plus shorts, music videos, and commercials</a></p>
    </div>
  </section>''',
    quotes_sec(),
    logo_row().replace('h-clients', 'h-clients-about'),
    closing(lede="Get in touch and let's see if we're a good fit.", btn='Get in Touch', second='<a class="btn" href="portfolio.html">View Our Work</a>'),
])
PAGES.append(dict(
    slug='about',
    title='About MindInMotion | Baltimore Video Production',
    desc='Meet Josh & Victor—film school friends turned production partners since 2012. Feature films and clients including Johns Hopkins.',
    og_title='About MindInMotion | Baltimore Video Production',
    og_desc='Meet Joshua Land and Victor Fink, the filmmakers behind MindInMotion. Founded in 2012.',
    crumbs=[('Home', ''), ('About', 'about')],
    preload=A + '11698893_10205059638871667_6520616449341988197_o-1.webp',
    body=ABOUT_BODY))

# ---------------------------------------------------------------- portfolio
CASES = [
    dict(key='quality', client='Maryland State Department of Education', title='Maryland Excels Campaign',
         alt='From Because Quality Matters: preschoolers laugh and shape clay at a classroom table.',
         text=['The Maryland State Department of Education needed videos that would reach parents across the state and convince them to choose licensed, quality childcare, without sounding like government ads.',
               'We took a documentary approach and filmed families at childcare centers around Maryland instead of casting actors. We followed parents through their daily routines. The result was a multi-video campaign that aired statewide and drove traffic to the Maryland Excels program.'],
         deliv='TV spots, digital campaign, social cuts'),
    dict(key='chelsea', client='Infinite Legacy', title='Organ Donation Testimonials',
         alt='From Infinite Legacy: a mother holds her baby close, cheek to cheek, in warm light.',
         text=['Infinite Legacy asked us to film donor families and organ recipients talking about loss, grief and hope, without exploiting their stories.',
               "We filmed each interview with a small crew and no time limit. These videos have been used at fundraising galas, in hospital partner communications, and across the organization's awareness campaigns."],
         deliv='Testimonial series, gala content, awareness campaign'),
    dict(key='cuba', client='Johns Hopkins Advanced Academic Programs', title='Cuba Field Course Documentary',
         alt='From the Cuba field course film: a boy in a yellow shirt on a horse beside a thatched hut, under a storm sky.',
         text=['Johns Hopkins Advanced Academic Programs needed to capture their Cuba field course for program recruitment. The logistics were complicated: international travel, limited crew, working around academic schedules, and navigating Cuban filming restrictions.',
               'We traveled with the students for the whole course. With a small crew we could film classroom discussions and street interviews without disrupting the program. Hopkins has used the documentary for years to recruit students into its international programs.'],
         deliv='Documentary, recruitment content, program materials'),
    dict(key='ashley', client='American Lung Association', title='Lung Cancer Patient Stories',
         alt='From the Ashley and Dr. Reed film: Dr. Reed and Ashley talk across a small round table in his office.',
         text=['The American Lung Association asked us to tell the stories of lung cancer patients and their healthcare providers, and to explain biomarker testing along the way.',
               "Sydney's story shows how biomarker testing changed her prognosis. Ashley and Dr. Reed talk about the patient-provider relationship during diagnosis. The American Lung Association has used the series nationally for patient education and advocacy."],
         deliv='Patient testimonial series, provider education content, advocacy campaign'),
]
PAGES.append(dict(
    slug='portfolio',
    title='Our Work | MindInMotion Video Production',
    desc='Watch our award-winning commercials, corporate videos & films. Work for Johns Hopkins, MSDE & more.',
    og_desc='Watch our portfolio of commercials, corporate videos, films, and documentaries.',
    crumbs=[('Home', ''), ('Portfolio', 'portfolio')],
    videos=PORTFOLIO_VIDEOS,
    body=''.join([
        phero(None, None,
              'Our Work', 'Our video production work: commercials, corporate videos and documentaries for clients in Baltimore, Maryland and elsewhere, plus our own feature films. Tap any frame to watch.',
              [], bare=True),
        feature_sec('Featured Projects', 'h-cases', [
            feature(c['key'], c['client'], c['title'], alt_override=c['alt'], body=c['text'], deliv=c['deliv'], eager=(i == 0))
            for i, c in enumerate(CASES)]),
        grid_sec('All Work', 'h-all', None,
                 work_grid(PORTFOLIO_ORDER, 'all-grid', all_keys=PORTFOLIO_ORDER, filters=FILTERS)),
        closing(btn='Start Your Project'),
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


# Laid out like Squarespace's Contact page: heading and details on the left, the form on the right,
# so the form is in the first screen. Same form name, fields and option values as the live form.
CONTACT_BODY = ''.join([
    f'''
  <section class="contact-top" aria-labelledby="h-page">
    <div class="wrap contact-grid">
      <div class="contact-intro">
        <h1 id="h-page">Contact Us</h1>
        <p class="lede">Tell us about your project and we&#39;ll get back to you within 24 hours with a custom quote.</p>
      </div>
      <div class="contact-form">
        <h2 id="h-form" class="form-h">Get Your Free Quote</h2>
        <form class="form" name="contact" method="POST" action="thank-you" data-netlify="true" netlify-honeypot="bot-field">
          <input type="hidden" name="form-name" value="contact">
          <p class="hp"><label>Don't fill this out: <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
          <div class="field"><label for="f-name">Your Name *</label><input id="f-name" name="name" autocomplete="name" required></div>
          <div class="field"><label for="f-org">Company / Organization</label><input id="f-org" name="company" autocomplete="organization"></div>
          <div class="field"><label for="f-email">Email Address *</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
          <div class="field"><label for="f-phone">Phone Number</label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
          <div class="field"><label for="f-type">Project Type *</label><select id="f-type" name="project-type" required>{opt([('commercial', 'Commercial / Advertising'), ('corporate', 'Corporate Video'), ('recruitment', 'Recruitment / HR Video'), ('testimonial', 'Testimonial'), ('documentary', 'Documentary'), ('film', 'Film / Narrative'), ('music-video', 'Music Video'), ('post-production', 'Post-Production Only'), ('other', 'Other')], 'Select a project type')}</select></div>
          <div class="field"><label for="f-budget">Budget Range *</label><select id="f-budget" name="budget" required>{opt([('under-2.5k', 'Under $2,500'), ('2.5-5k', '$2,500 - $5,000'), ('5-10k', '$5,000 - $10,000'), ('10-20k', '$10,000 - $20,000'), ('20k+', '$20,000+'), ('not-sure', 'Not sure yet')], 'Select your budget')}</select></div>
          <div class="field"><label for="f-when">Timeline</label><select id="f-when" name="timeline">{opt([('asap', 'As soon as possible'), ('1-month', 'Within 1 month'), ('1-3-months', '1-3 months'), ('3-6-months', '3-6 months'), ('flexible', 'Flexible / Not urgent')], 'When do you need this?')}</select></div>
          <div class="field"><label for="f-how">How did you hear about us?</label><select id="f-how" name="how-found">{opt([('google', 'Google Search'), ('referral', 'Referral'), ('social', 'Social Media'), ('vimeo', 'Vimeo'), ('previous-client', 'Previous Client'), ('other', 'Other')], 'Select an option')}</select></div>
          <div class="field full"><label for="f-msg">Tell Us About Your Project *</label><textarea id="f-msg" name="message" required placeholder="What are you making, who is it for, and when do you need it?"></textarea></div>
          <p class="note full">By submitting this form, you agree that MindInMotion may use the information you provide to respond to your inquiry. Read our <a href="{LIVE}/privacy-policy">Privacy Policy</a>.</p>
          <button class="btn btn-solid full" type="submit">Get My Free Quote</button>
          <p class="note full">We respond within 24 hours.</p>
          <p class="form-status full" role="status" tabindex="-1" hidden></p>
        </form>
      </div>
      <aside class="side" aria-labelledby="h-touch">
        <h2 id="h-touch">Get In Touch</h2>
        <dl class="contact-list">
          <div><dt>Baltimore</dt><dd>3617 Chestnut Ave<br>Baltimore, MD 21211<br><span style="color:var(--bone-3)">Serving Maryland, DC &amp; the <span class="nw">Mid-Atlantic</span></span></dd></div>
          <div><dt>Phone</dt><dd><a href="tel:+14435275181">(443) 527-5181</a></dd></div>
          <div><dt>Email</dt><dd><a href="mailto:mindinmotionpro@gmail.com">mindinmotionpro@gmail.com</a></dd></div>
        </dl>
        <p class="note">We respond within 24 hours</p>
        <h2 style="margin-top:44px">What happens next?</h2>
        <ol class="steps">
          <li>We'll review your project details and set up a call</li>
          <li>We'll discuss your goals, timeline, and budget to understand the scope</li>
          <li>You'll receive a custom quote with clear deliverables and pricing</li>
        </ol>
      </aside>
    </div>
  </section>
  <section class="sec" aria-labelledby="h-faq">
    <div class="wrap">
      <div class="sec-head solo"><h2 id="h-faq" class="h2">Common Questions</h2></div>
      <div class="faq">
        {''.join('<details><summary>%s</summary><div class="a">%s</div></details>' % (e(q), a) for q, a in FAQ)}
      </div>
    </div>
  </section>''',
])
PAGES.append(dict(
    slug='contact',
    title='Contact Us | MindInMotion Video Production',
    desc='Contact MindInMotion for a free video production quote. We serve Baltimore and the Mid-Atlantic region. Get a response within 24 hours.',
    og_title='Contact MindInMotion | Get a Free Quote',
    og_desc='Get a free video production quote. We respond within 24 hours.',
    crumbs=[('Home', ''), ('Contact', 'contact')],
    faq=FAQ,
    body=CONTACT_BODY))


# ---------------------------------------------------------------- write everything
def main():
    for p in PAGES:
        name = 'index.html' if p['slug'] == 'index' else p['slug'] + '.html'
        doc = page_html(p, p['body'])
        doc = re.sub(r'\n{3,}', '\n\n', doc)
        (OUT / name).write_text(doc)
        print('wrote', name)


if __name__ == '__main__':
    main()
