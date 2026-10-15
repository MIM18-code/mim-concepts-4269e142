# Live site vs. Squarespace vs. Concept D: an honest side-by-side

Written 2026-10-15 for the refined demo in this folder, and checked against the demo's code after the evening's changes. Ten of the 11 small fixes Joshua approved that night are in, and are marked below. He chose to keep the Play mark on hover.

## Sources

- **Live site**: mindinmotion.tv (React and Tailwind) after today's live fixes. Those fixes put in the right founder photos and every film on the homepage, and took the neon cyan off everything except the M logo. Every page was rendered at 1440px and 390px wide. The screenshots are in the project files under `refined-site-2026-10-15/compare/live/` and are cited as "live index-1440-p0", which is the file `index_html-1440-p0.jpg`.
- **Squarespace**: Joshua's current published Squarespace site, grasshopper-dandelion-xzmb.squarespace.com, captured on 2026-10-15 at 1440px and 390px. The captures are in `refined-site-2026-10-15/squarespace-live/`: `chunks/` holds the screenshots and `content/` each page's text, videos and images. They are cited as "sq home-1440-p0". Text, video IDs and slideshow settings also come from the December 2025 Squarespace export. Wayback Machine snapshots are older versions of the site and are not used.
- **Concept D**: the title-sequence concept on the review site. The screenshots are in `refined-site-2026-10-15/compare/conceptd/` and are cited as "D index-1440-p0".
- **The demo**: described from its current code (`_build/build.py`, `site.css` and `site.js`). The demo screenshots in `compare/demo/` are older than tonight's changes, so they are not cited.

## The short version

1. The live site has the right content in the right order for clients. What lets it down is the dressing: pill buttons, rounded cards with badges, the stats row, icon cards, uppercase eyebrow labels and a carousel with dots. Those are the tells of a Tailwind template.
2. Joshua's Squarespace site looked better because it showed the work bigger and did less around it. It had two large stills a row, a play mark on the video stills, heavy headings on black, bold testimonials, slideshows that ran by themselves and a contact form right on the page. Its weak spots were the slogans, stock rounded buttons and grey form boxes, untitled stills that sent people off to Vimeo, and stale facts.
3. Concept D has the right look: monochrome, square corners, real stills and a Play mark you can always see. Its scroll-cinema structure (slates, timecode, scene numbers) asks more of a client than a plain page does, so that part stays out.
4. The demo keeps the live site's layout and wording, takes its look from Concept D, and has removed everything that read as template. It brings back what Squarespace did better, apart from the six bigger changes listed at the end for Joshua's call.

## What the live site does well (kept)

- **The navigation**: Portfolio, Services (four pages), About, Contact, the phone number and Get a Quote (live index-1440-p0).
- **The homepage order**: the reel hero, the client logos straight after it, featured work with filters, the four services, a behind-the-scenes slideshow, About with the founders' photo, the four testimonials, a closing contact section and a full footer (live index-1440-p0 to p3). A client finds what they need in that order, and the demo keeps it.
- **The Portfolio page**: two large 16:9 stills a row with a title and a grey credit line, and Featured Projects that give the client, a short write-up and the deliverables (live portfolio-1440-p1). Squarespace never gave clients that context.
- **Service pages that get to the work**: the H1, the intro and one button, then the work, with a title on every still. Films play on the page instead of sending people to Vimeo (live commercial-video-production-1440-p0).
- **The wording.** The demo uses the live wording word for word, including the homepage's "We are MindInMotion" and the line under it. The exceptions are Orlando, the brags, the slogans and trivia Joshua cut on Oct 14, and his renamed headings (see COPY-REVIEW.md). Page addresses, titles, meta descriptions and tracking stay (see SEO-CHANGES.md).
- The client logo wall, the real testimonials and the FAQ on the contact page.

## What makes the live site read as a template (removed)

| Live site | Why it reads as template | In the demo |
|---|---|---|
| A "Baltimore · Orlando" chip with a pin icon, a scroll-down chevron, and uppercase tracked labels over sections ("TRUSTED BY INDUSTRY LEADERS", "OUR WORK", "SERVICES", "TESTIMONIALS") (live index-1440-p0 to p3) | Stock landing-page furniture | Gone. Headings stand on their own. |
| A stats row with icons: 100+ Clients Served, 2012 Founded, 1.8M+ Video Views and a feature-film count (live index-1440-p0) | The stock SaaS landing-page block, and Joshua named it a brag | Cut. The logos and the work make the case. |
| Pill buttons with icons ("Watch Our Reel" with a play circle, "Get a Quote in 24 Hours" with an arrow) and pill filter tabs (live index-1440-p0, portfolio-1440-p1) | The default Tailwind look | The same labels on square buttons with a thin border, one of them filled, and no icons. Filters are plain words with a line under the active one. |
| Rounded cards with "Case Study", "Featured" and "Demo Reel" badges, client chips, and a round play button on every still (live index-1440-p0, commercial-video-production-1440-p0) | The card-and-badge grid every template ships with | Plain stills with the title underneath and a small square "Play" mark that appears on hover on a computer and stays visible on phones. |
| Four rounded icon cards under "Full-Service Production", each with "Learn More" (live index-1440-p1) | Icon cards are the clearest tell of all | Four services, each a real still with its name and the live description. |
| A slideshow with round arrow buttons and a row of 17 dots (live index-1440-p2) | Carousel kit | Two small arrows in the corner. No dots, counter or pause button. |
| Testimonials in rounded cards with quote marks (live index-1440-p3) | The template testimonial block | Bold type, two a row, words unchanged. |
| Section bands that alternate between black and near-black (live index-1440-p1, p3) | Template sectioning | One black ground. |
| Image zoom on hover and a blurred-glass header once you scroll (`src/app.jsx`) | Effects for their own sake | No zoom. A solid black header, clear over the home hero until you scroll. |
| "Ready to Bring Your Vision to Life?" and similar closing slogans (live index-1440-p3) | Template slogans | "Tell us about your project", with the quote button and the phone number. |
| A pause button on the banner video and on slideshows | Not on Squarespace, and Joshua found it ugly | None. The banner video stays a still, and slideshows stand still, for visitors who ask for reduced motion. |
| Each logo links to a portfolio filter | It makes the logos look like buttons | No links, as Joshua asked. |

## What Squarespace did better

### Brought back

- **Big stills, two a row.** Squarespace showed the work two to a row, each still about 645px wide at 1440, on Home, Portfolio, Film, Commercial and Corporate (sq home-1440-p2, portfolio-1440-p0, commercial-video-production-1440-p0). That is the main reason it felt like a film company's site. The demo shows every work grid two a row, about 600px per still at 1440, and one a row on phones. Every still has a title under it, and Portfolio also shows the credit line.
- **Heavy headings and few sizes.** What made Squarespace look confident was large, heavy, tightly spaced headings against lighter body text, with only a few sizes on a page (sq home-1440-p1, portfolio-1440-p0). The live site sets its type light (live index-1440-p1). The demo uses Libre Franklin 400 and 700, which Joshua picked, in Squarespace's proportions: six sizes in all, bold tight headings, and nothing under 16px. Its section headings stop at 56px, where Squarespace's are about 64px; see the changes below.
- **Bold testimonials.** Squarespace set its four quotes in large bold type with the name underneath and no cards (sq home-1440-p2, p3). The demo does the same with the same four quotes, two a row.
- **Slideshows that run by themselves, with nothing but the pictures.** Commercial, Corporate and Film each ended with a full-width behind-the-scenes slideshow with thin arrows and no captions (sq commercial-video-production-1440-p1). The demo uses the same photo sets: 14 on Commercial, 6 on Corporate and 17 on Film. They advance every 5 seconds and pause on hover or keyboard focus, when off screen, and when the tab is hidden. Nothing makes the visitor click.
- **Service pages that get to the work.** Squarespace opened with a header and the H1, then the intro, one "Tell Us About Your Project" button, the grid and the slideshow (sq commercial-video-production-1440-p0, p1). The demo follows that order. It adds one client testimonial before the slideshow and the live homepage's closing section after it.
- **All the films on the Film page.** Squarespace showed nine films as large stills with plain titles (sq film-production-1440-p0, p1). The demo has the same nine plus the Incubation teaser and Heart & Thunder, grouped as feature films, short films and music videos.
- **Square, quiet controls.** The demo has square buttons and dark form fields with a thin border, without Squarespace's white rounded buttons and grey boxes.

### Brought back on 2026-10-15 (the small fixes)

- **The homepage slideshow.** Squarespace and the live site use the same 17 behind-the-scenes photos (content/home.md). The demo's homepage now uses those 17 in the live order instead of a 12-photo mix from the service pages.
- **Slideshows on phones.** Squarespace's slideshow filled most of a phone screen (sq commercial-video-production-390-p0). The demo's is now 4:5 on phones, about 490px tall at 390, where it used to be a 16:9 strip about 220px tall.
- **Nonprofit work.** Squarespace had a "Nonprofit / Instructional Work" page with 12 videos, seven of them from the Maryland State Department of Education or Maryland Excels (sq nonprofit-1440-p0). Those seven are now tagged Nonprofit as well as Commercial, so Portfolio's Nonprofit filter shows 15 films.
- **The stills.** Call Your Wife now uses the masked-singer frame, as Squarespace and the live Film page do (sq film-production-1440-p0). Johns Hopkins Engineering Management now uses Squarespace's lab frame (sq portfolio-1440-p1) instead of an interview frame with a name card burned into it.
- **Portfolio's opening.** All Work now opens as Squarespace's did: the reel, Good Mom, Moms at the Playground, AACPD, Ghost Light and The Farmhouse (sq portfolio-1440-p0). The four Featured Projects come after the rest of the client work, so they don't repeat right under the write-ups.
- **The Film page.** Titles only, as on Squarespace and the live Film page, and two a row on phones (sq film-production-390-p0). Ape Canyon's mark reads "Prime Video" so it fits a half-width still.
- **Smaller fixes.** The client logos load straight away, since they sit right under the hero. The footer stays two columns on phones, with the address and Follow links running full width and the Follow links in one row, which takes it from about 900px to about 660px tall at 390. The Contact page's "Baltimore HQ" now reads "Baltimore".

### Not brought back yet

- **A contact form on the page.** Squarespace's Contact page had the heading and a short paragraph on the left and the form on the right, all in the first screen (sq contact-1440-p0). Its homepage ended with the same short form (sq home-1440-p3, home-390-p2). The demo's form sits below a full-width heading, and the homepage only links to Contact.
- **Heading size.** Squarespace's section headings were about 64px at 1440. The demo's are 56px.
- **Header pictures.** Squarespace's Commercial, Corporate and Film headers showed different footage from the grid. They were muted background videos (export: YouTube byswLHwqo2M, ybBa38EiM2Q and M0txpVj2JoA). Each demo header repeats a still from its own grid: Good Mom, Mike Odom and Lotus Eyes.
- **Sound mixing.** Squarespace's post page said MindInMotion works with sound-mixing partners (sq post-production-1440-p0). Neither the demo nor the live site mentions sound.

## What was worse on Squarespace (not brought back)

- **Slogans.** Under the hero, five stacked lines ("we are mindinmotion" through "we create films, commercials, marketing videos, ideas") were followed by a band of empty black. "Let's create something amazing together" came back above the homepage form and on the Contact page, and Post Services opened on "Make it stand out." (sq home-1440-p0, p1, p3, contact-1440-p0). The demo keeps only the live hero line, "We Create, Produce, Direct, Film, and Edit. Let's Create Something Amazing Together.", because Joshua asked for it.
- **Brags and stale lines**: "five feature films", "as of 2020", "For almost a decade", "our work isn't just watchable, it's memorable", and Incubation "currently in post-production" (sq home-1440-p1, film-production-1440-p0).
- **Stock Squarespace controls**: white rounded buttons with small regular-weight text, a rounded outlined phone box in the header with both the Baltimore and Orlando numbers, and light grey form boxes on black (sq home-1440-p0, contact-1440-p0).
- **Intros as walls of text.** The service intros ran across the full page width. Commercial's was all bold, and Film's three long paragraphs included the feature count and an Orlando link (sq commercial-video-production-1440-p0, film-production-1440-p0).
- **Stills with no titles.** The Commercial, Corporate and Nonprofit grids had no titles, and each still sent visitors off to Vimeo or YouTube (sq commercial-video-production-1440-p0, nonprofit-1440-p0). In the demo every still has a title and plays on the page.
- **Phone layouts.** Service-page stills shrank to small thumbnails, two a row (sq commercial-video-production-390-p0). Portfolio stacked the whole left column first, so Good Mom fell from second place to near the end (sq portfolio-390-p0, p2). On the homepage, "cinematographers" broke as "cinematographe / rs" (sq home-390-p0).
- **Sloppy captions**: a "." as the credit line under the reel and other tiles, "Victor FInk", a missing comma before "DP:", and cramped dashes such as "Maryland Excels-Moms at the Playground" (sq portfolio-1440-p0 to p2).
- **Orlando**: the Orlando number in the header and the Kissimmee address first in every footer (sq home-1440-p3).
- **An embedded grey Google map** on the Contact page (sq contact-1440-p0). The demo's footer address links to the map instead.
- **A second post page.** Post Services repeated Post Production's copy in bold, with a large empty band (sq post-services-1440-p0). The demo has one post page. The live site already redirects /post-services to /post-production.

## What Concept D contributes, and what it doesn't

- **Taken:** the monochrome approach (black, white and greys, with the footage carrying the color), square buttons with a thin border and one filled, the square "Play" mark (D portfolio-1440-p3), testimonials set as type rather than cards, hairline rows instead of icon cards, the plain "Tell us about your project" close (D index-1440-p7), and the copy cuts Joshua approved on Oct 14.
- **No longer taken:** Concept D's warm ink and cream colors (Joshua wants plain white text), its gold accent, and its fonts (Schibsted Grotesk and Newsreader).
- **Left out:** the scroll-cinema structure (slates, timecode, shot counters) and the hero stats list (D index-1440-p0). Also left out: the text-only client list, which the logo wall replaces (D index-1440-p7), the behind-the-scenes strip that only moves when clicked, and the project counts on the filters, which read as a tally (D portfolio-1440-p3).
- **Worth a later look:** setting the page title on black under the header picture instead of over it, which keeps the frame clean (D index-1440-p0).

## Facts corrected along the way

These follow the "Fix live site errors" thread and Joshua's answers on 2026-10-15.

- The crew photo of a woman labeled as Josh ("Hannah") is gone. Josh's photo is the on-stage one with the microphone, and Victor's is the on-set one.
- The Film page has every film, with the same video IDs as the live fix.
- Feature-film counts are gone everywhere: Squarespace's "five feature films", the live stats row and service copy, and Concept D's hero list.
- **Bad Witch** and **Ape Canyon** are both shown as 2021, their release year. Squarespace says 2018 and 2019.
- **Incubation** is screening at festivals. Squarespace still says "currently in post-production".
- **Josh and Victor are both cinematographers.** Josh's title reads Co-Founder / Director / Cinematographer / Editor, and Victor's reads Co-Founder / Cinematographer / Producer.
- **The Summer Before** is not named or highlighted.
- **Orlando** is dropped. The live site still shows it in the menu, the header, the hero chip and the footer.
- **Precious Layne**'s client is Johns Hopkins Advanced Academic Programs, as on the other Teaching Writing films.
- The live homepage's **Ashley & Dr. Reed** card shows a grey "Video Thumbnail" placeholder (live index-1440-p1). The demo uses a frame from the film.
- Matthew White's quote reads "MindInMotion", as on the live site. Squarespace had "MindinMotion".
- The **USM** logo is the official one, and every logo is plain white.
- The M logo stays cyan, which was Joshua's choice.

## Changes still worth making (Joshua's call)

Ten of the 11 small fixes are done (see "Brought back on 2026-10-15" above). Joshua chose to keep the Play mark on hover, unlike Squarespace's always-visible triangle (sq portfolio-1440-p0). These six need Joshua's say:

1. Lay the Contact page out like Squarespace's, with the heading and details on the left and the form on the right, so the form is in the first screen. The fields, form name and thank-you page stay the same.
2. End the homepage with a short form (name, email, phone, project) beside "Tell us about your project", as Squarespace did. It would be a second Netlify form posting to /thank-you, so the SEO consultant would need to know.
3. Raise section headings from 56px to Squarespace's 64px. I'd show them side by side first.
4. Take the single testimonial off Commercial, Corporate and Film. Squarespace's service pages had none, and the four quotes stay on Home and About.
5. Pick header stills for Commercial, Corporate and Film that aren't in the grid below. If you want moving headers like Squarespace's, each page needs a short clip on Vimeo.
6. Add a sound-mixing line to the post page, using the substance of the old Squarespace copy.

## Questions for Joshua

- The lines under the service-page H1s, such as "TV spots, PSAs, recruitment ads and social cuts.", read a little like taglines. Squarespace's headers had the H1 only. Keep them or cut them?
- The quote form requires Project Type and Budget Range, as the live form does. Squarespace asked only for a name, email, phone and message. Keep them required, make them optional, or drop them?
- Portfolio credit lines mix "Director: Josh Land & Victor Fink" and "Directors: Joshua Land & Victor Fink". Which form should they use?
- Squarespace had "Badging - Families" (Vimeo 952434464) on its Nonprofit page and two untitled Corporate films (Vimeo 442503640 and 378829912). Should any of them go in, and with what title and client?
- LUNG FORCE Advocacy Day 2025 uses the video's title card, which carries the American Lung Association's tagline. Can you send a real frame from the film?
- The demo says "Johns Hopkins Master of Science in Engineering Management". Squarespace and the live Portfolio say "Masters in Science and Engineering Management". Which is right?
- About mentions the 16mm class three times: in the hero line, in Our Story and in Victor's bio. These are live lines. Keep all three or trim to one?
- The footer is now a grey band like Squarespace's. Keep it, or go back to plain black?

## Review copy only

The demo's forms check their fields but don't send, and the Privacy link goes to the live policy. Tracking, the thank-you page and the redirects go in at launch as listed in SEO-CHANGES.md. The demo screenshots in `compare/demo/` need retaking before this goes to anyone else.
