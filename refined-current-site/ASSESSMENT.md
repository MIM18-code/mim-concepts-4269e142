# Live site vs. Squarespace vs. Concept D: an honest side-by-side

Written 2026-10-15 for the refined demo in this folder. The three sources were:

- **Live site**: mindinmotion.tv as it stands (React and Tailwind). I read the code in MIM18-code/mimwebsite and rendered every page at 1440px and 390px wide.
- **Squarespace**: the 2023 to 2025 site. I looked at it on the Wayback Machine (the January 2024 home page rendered properly; the December 2024 snapshot lost its CSS) and read its full text and structure in the Squarespace export from Joshua's Mac.
- **Concept D**: the title-sequence concept on the review site, which Joshua picked as the design base.

## The short version

1. The live site has the right content in the right order for clients. What lets it down is the dressing: the neon cyan, pill buttons, rounded cards with badges, the stats row, icon cards and fade-in animations. Those are the tells of a Tailwind template.
2. Squarespace looked better because it did less. It used a black page, big stills with a plain title underneath, a full-width slideshow that ran by itself, and the same simple shape on every service page. It never had cards, icons, stats or badges.
3. Concept D has the right look (monochrome and filmic, with square hairline buttons and real stills). Its scroll-cinema structure (slates, timecode, scene numbers) asks more of a client than a plain page does.
4. The demo keeps the live site's layout and copy and takes the look from Concept D. From Squarespace it brings back the big plain stills, slideshows that advance on their own, and the simple service-page shape. Everything that read as template is gone.

## What the live site does well (kept)

- The navigation: Portfolio, Services (four pages), About, Contact, the phone number, and Get a quote.
- The homepage order: reel hero, client logos, selected work with filters, services, behind the scenes, about, testimonials and contact. A client finds what they need in that order.
- The service pages and their URLs, page titles, H1s and meta descriptions, which carry the search ranking.
- The logo wall (Johns Hopkins, MSDE, American Lung Association, IPG, Anne Arundel County Police, Infinite Legacy, Packard Center).
- The real testimonials, the FAQ on the contact page, and a big still for every project.

## What makes the live site read as a template (removed)

| Live site | Why it reads as template | In the demo |
|---|---|---|
| Neon cyan on section labels, icons, quote marks and the Demo Reel badge | It's a Tailwind palette color, not a film company's, and Joshua called it an eyesore | Monochrome: ink, bone and greys. The footage carries the color. The M logo stays cyan, which Joshua chose in the live-fixes thread. |
| Stats row: "100+ Clients Served / 2012 Founded / 1.8M+ Video Views / 5 Feature Films" with icons | The stock SaaS-landing-page block, and Joshua named it as a brag | Cut. The client logos and the work make the case. |
| Pill buttons ("Watch Our Reel", "Get a Quote in 24 Hours", "Get Your Free Quote") and pill filter tabs | The default Tailwind/shadcn look | Square hairline buttons, at most two per screen. Filters are plain text with an underline on the active one. |
| Rounded cards with "Case Study" and "Featured" badges and client chips on the thumbnails | The card-and-badge grid every template ships with | Plain stills with the title and credit underneath, as on Squarespace. |
| Hover lift, image zoom, play-button glow and staggered fade-ups as you scroll | Motion added for its own sake | A slight brighten on hover and a "Play" label. Nothing fades in. |
| Four rounded icon cards under "Full-Service Production" with "Learn More →" | Icon cards are the clearest template tell of all | Four services, each with a real still from our work and the approved copy. |
| Testimonials in rounded cards with big cyan quote marks | Template testimonial block | Set as plain type with a hairline, words unchanged. |
| "Ready to Bring Your Vision to Life?", "Let's Create Something Amazing Together", "Trusted by industry leaders" | Template slogans | Gone. The closing section uses the approved "Tell us about your project". |
| Each logo links to a portfolio filter | It makes the logos look like buttons | No links, as Joshua asked. |
| Blurred glass header | Common template default | A solid header (transparent over the home hero until you scroll). |

## What Squarespace did better (brought back)

- **Big stills with a plain title underneath.** The work grid had no boxes, borders, badges or chips, just the image and its name. The demo does the same.
- **Slideshows that run by themselves.** Each service page had a full-width behind-the-scenes gallery that changed slides on its own (Film had 17 slides, Commercial 14, Corporate 6). The demo uses those same sets, full width, advancing every 5 seconds. Each one pauses on hover or keyboard focus, when it's off screen or the tab is hidden, and for visitors who set their device to reduce motion. There's a pause button, and swiping works on phones. Nothing makes the visitor click to see the next slide.
- **One simple shape for every service page**: header image, H1, a short intro, the work, the slideshow, then contact. That repetition is what made it easy for clients, so the demo uses it on all four service pages.
- **A black page and confident type.** Squarespace's large headings on black looked like a film company's site. The demo uses Concept D's ink and bone colors with larger headings.
- **All nine films on the Film page** (The Farmhouse, Call Your Wife, Ghost Light, I Like Me, Lotus Eyes, Don't Go Hiking, Bad Witch, Lovers in Lullaby, Ape Canyon). The live homepage Film tab showed two of them. The demo's Film page groups them as features, shorts and music videos, and the homepage "Film & music videos" filter shows all of them, plus Incubation and Heart & Thunder.
- **Nonprofit work as its own category.** Squarespace had a Nonprofit page. The demo adds a Nonprofit filter to the work grids, since most of the clients are nonprofits.

## What was worse on Squarespace (not brought back)

- Thick, rounded, italic all-caps buttons.
- The rotating "we are..." slogan lines on the homepage.
- The Film page as one very long single column of videos.
- Untouched template placeholder pages (About, Our Team, Press).
- Poppins as the body font.
- "Let's create something amazing together".

## What Concept D contributes, and what it doesn't

- **Taken:** the monochrome palette (ink #0d0c0a, bone #ece6da, greys), Schibsted Grotesk for headings and labels with Newsreader for reading text, square hairline buttons, real stills, and all the copy Joshua has approved over the last three passes (titles, meta descriptions, service copy, FAQ, credits, the homepage H1 "Film and video production in Baltimore").
- **Left out:** the scroll-cinema structure (SC slates, shot counters, timecode, the monitor). It's the part that makes D distinctive, and also the part a client has to learn before they can find the corporate videos.

## Facts corrected along the way

These follow the confirmed fixes from the "Fix live site errors" thread:

- The crew photo of a woman labeled as Josh ("Hannah") is gone. Josh's photo is the on-stage one with the microphone, and Victor's is the on-set one with the monitor, as Joshua confirmed. The homepage photo is the one where Josh is really on the left.
- The Film tab now has all the films, with the same video IDs the live fix uses.
- "Five feature films" is gone everywhere: the homepage About, the Film page intro, the About page hero, the About meta description and the posters heading. See COPY-REVIEW.md.

## Still open

- **USM logo**: shown as the name in type until the official logo file comes in from the Mac.
- **Orlando** stays off, per Joshua on 2026-10-07.
- **Incubation's status**: the live About page says "screening at festivals" in the text but "In Post" under the poster. The demo uses "Screening at festivals" in both places.
- The contact form on the demo checks the fields but doesn't send. The Privacy link goes to the live policy.
