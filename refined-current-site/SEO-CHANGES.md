# Search and tracking changes in the redesign

For Joshua's SEO consultant, to review before anything launches. Nothing here is live: this is the review demo of the redesigned mindinmotion.tv. It is compared with the live site as it stands on 2026-10-15 (the live repo's `main` at `184e528`). Anything not listed stays exactly as it is now.

The wording on the pages is the live site's, with a short list of exceptions. The full line-by-line list is in [COPY-REVIEW.md](COPY-REVIEW.md).

## What stays the same

- **Page addresses.** All eight stay: `/`, `/commercial-video-production`, `/corporate-video-production`, `/film-production`, `/post-production`, `/about`, `/portfolio`, `/contact`. The canonical tags are unchanged. So are `/thank-you`, `/privacy-policy` and the 404 page.
- **Redirects.** The `.html` to clean-address 301s in `netlify.toml` and the old Squarespace 301s in `_redirects` stay. The Orlando ones change (see below).
- **Tracking.** GA4 (`G-QKX4700C3T`), Google Ads (`AW-11297450275`) and the CallRail number swap go back on every page, unchanged. The demo leaves them out on purpose so test visits stay out of the real data.
- **Contact form and conversion.** Same Netlify form name (`contact`), the same fields and the same option values. It still posts to `/thank-you`, which fires the Ads conversion.
- **Page titles.** Six of the eight are word for word the same. The other two only lose "& Orlando" (see below).

## The one address change: the Orlando page

Joshua dropped Orlando on 2026-10-07, so `/orlando-commercial-video-production` goes away. At launch:

- 301 `/orlando-commercial-video-production` (and its `.html`) to `/commercial-video-production`.
- Point the four old Orlando redirects (`/orlando`, `/orlando/`, `/orlando-video-production`, `/orlando-video-production/`) straight at `/commercial-video-production`, so there are no redirect chains.
- Take it out of `sitemap.xml` (9 addresses become 8).
- Take Orlando out of `llms.txt` (it mentions Orlando 7 times).
- The (407) 584-8891 number and the Kissimmee address come off the header, footer, contact page and structured data.
- He'll know whether anything else points at Orlando: a Google Business Profile for the Kissimmee address, listings that cite it, a CallRail number for 407, or Ads targeting.

## Titles and descriptions

Only Orlando, the film and client counts, and a few slogan endings come out. Everything else is word for word.

| Page | Title | Meta description | Social (og) title and description |
|---|---|---|---|
| Home | "Video Production Baltimore & Orlando \| MindInMotion" becomes "Video Production Baltimore \| MindInMotion" | Drops "& Orlando" | Both drop Orlando |
| Commercial | Same | Drops "that convert" and "& Orlando" | Description drops Orlando and "Cinematic storytelling that moves audiences." |
| Corporate | Same | Drops "& Orlando" | Description drops Orlando and "Elevate your brand." |
| Film | "Film Production Baltimore & Orlando \| MindInMotion" becomes "Film Production Baltimore \| MindInMotion" | "6 features screened at festivals worldwide" becomes "Our features have screened at festivals worldwide"; drops "& Orlando" | Title as the page title; description "6 feature films" becomes "Feature films" |
| Post-Production | Same | Drops "& Orlando" | Description drops "Where the magic actually happens." |
| About | Same | "6 feature films, 100+ clients including Johns Hopkins. Let's create together." becomes "Feature films and clients including Johns Hopkins." | Title drops "& Orlando" |
| Portfolio | Same | Drops "See what we can create for you." | Same |
| Contact | Same | Drops "Orlando," | Same |

"Award-winning" stays wherever the live site has it.

## Headings

**H1s.** Three change. Joshua renamed these on 2026-10-14 because they were slogans. If any of them were the SEO consultant's call, tell Joshua and they go back.

| Page | Live H1 | New H1 |
|---|---|---|
| About | Film School Friends. Business Partners. | About MindInMotion |
| Post-Production | Where the Magic Actually Happens | Post-Production |
| Contact | Let's Create Something Amazing | Contact Us |

The H1s on Home ("We are MindInMotion"), Commercial, Corporate, Film and Portfolio don't change.

**H2s and H3s.**

- Home: "Film School Friends. Production Partners." becomes "About MindInMotion". The closing "Ready to Bring Your Vision to Life?" becomes "Tell us about your project".
- About: "How We Think About Work" becomes "How We Work", and its three H3s ("Story First", "Collaboration", "Craft Matters") become "Documentary Interviews", "Working With Josh and Victor" and "In-House Post-Production". New H2s are "Our Story" and "What Our Clients Say" (the homepage testimonials, shown here too). The closing "Let's Make Something Together" becomes "Tell us about your project".
- Post-Production: "Collaboration Is the Point" becomes "Working With Your Editor". The "Tools We Work With" label stays, with the same tool names, but is no longer a heading.
- Portfolio: the closing "Ready to Create Something Amazing?" becomes "Tell us about your project", and "All Work" is added over the full grid.
- Film: the films are grouped under the new H2 "Feature films, shorts and music videos", with H3s "Feature films", "Short films" and "Music videos". The film titles become H4s.
- Commercial, Corporate and Film gain a closing section with the H2 "Tell us about your project", the quote button and the phone number. Live, these pages end after Behind the Scenes.
- Contact: "Get Your Free Quote" and "What happens next?" move up from H3 to H2. The five FAQ questions are still on the page but are no longer headings. They are now marked up as FAQ structured data instead.
- Video titles in each work grid are H3s. On the homepage, every project is in the page and the "Featured" filter shows the same eight as live.
- The homepage and About gain a client logo wall. Its heading, "Clients include", is visually hidden and is read out to screen readers only. Each logo's alt text is the client's name.
- Footer labels ("Services", "Baltimore", "Follow") are plain text, not headings, as on the live site.

## Body text

- **Service-page intros.** The intros on Commercial, Corporate, Film and Post-Production are the shorter versions Joshua approved on 2026-10-14, with the slogan lines cut. Each page keeps its main phrase ("commercial video production", "corporate video", "film production company in Baltimore, Maryland", "post-production") in its title, description, H1 and intro. A few repeat mentions went with the cut sentences. If the consultant wrote the longer intros, they can go back word for word.
- **Removed site-wide.** Orlando, the stats row (100+ clients, 1.8M+ video views, 6 feature films) and the feature-film counts.
- **Added.** The client logo wall, a client testimonial on Commercial, Corporate, Film and About (verbatim from the homepage), and the phone number in every closing section, where CallRail can swap it.

## How the pages are built

The live pages are a JavaScript app. Before the script runs, crawlers see a separate, simpler copy of each page. On the homepage, for example, that copy has an "Award-Winning Video Production Company" heading and a "Featured Clients" paragraph. The new pages are plain HTML, so every crawler sees the same text visitors see, and the simpler copy goes away.

On the new homepage, "award-winning video production company" appears in the description, social description and structured data rather than in a heading. The client names it listed are now the logo wall.

## Structured data (JSON-LD)

- **Business.** Same name, Baltimore address, phone, email and founding year. The Kissimmee address, the 407 number and the Orlando and Florida service areas are removed. Added: map link, map coordinates, and both founders with their IMDb pages. The type is LocalBusiness and ProfessionalService.
- **Every page.** A WebPage entry and breadcrumbs. Breadcrumbs exist only in the structured data and are not shown on the page.
- **Service pages.** A Service entry.
- **Contact.** FAQPage for the five questions.
- **Portfolio.** The list of videos, as on live.
- **About.** The founders as Person entries. The live About page has no structured data.

## Demo-only settings that change at launch

- The demo tells search engines not to index it (`noindex, nofollow, noarchive`). That comes off at launch.
- Links on the demo point to `.html` files because it is hosted on GitHub Pages. At launch they use the clean addresses, so internal links don't go through a 301.
- The form posts to `thank-you` on the demo. At launch that is `/thank-you`, as now.
- Tracking tags go back on as above.
