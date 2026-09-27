# Peers: A24-adjacent studios, horror microsites, production companies

Research pass, 27 September 2026. I loaded every site below live with `_tools/shoot-url.js` (Chrome, 1440x900 desktop and 390x844 mobile) and read the screenshots. I didn't work from memory. Font names and colors come from the tool's computed-style output, plus a second script that measured the largest text styles on each page (size, family, weight, tracking, case). Pixel sizes are at a 1440px viewport. Where the size itself is the point I also give a vw figure.

All screenshots are in `research/shots/`. Several production-company sites lazy-load or hijack scrolling, so their full-page JPGs go blank below the fold. For those I added scroll-state frames (`*-scroll1.png` to `*-scroll3.png`) and hover frames (`annapurna-hover1.png`, `annapurna-hover2.png`).

A24's own sites aren't covered here. The `a24-*` files in `shots/` came from a separate pass.

## Dead, moved or broken

- **thebirthdaymurders.net** (Neon's in-universe Longlegs site, 2024). The domain no longer resolves. I shot the June 2024 Wayback capture instead: `birthdaymurders-2024-desk-fold.png`.
- **cuckoo.film**. The domain no longer resolves. Wayback capture from August 2024: `cuckoo-2024-desk-fold.png`.
- **immaculate.film**. The domain now belongs to an unrelated truck-driving school. The March 2024 Wayback capture renders blank (`immaculate-2024-*`).
- **themonkeyfilm.com**. The DOM loads (nav, "MOVIE PLATFORM © 2025 POWSTER", "© 2025 NEON") but nothing paints. It's a blank #0F0F0F page in headless Chrome and in a normal browser pane (`themonkey-*`).
- **longlegs.film**. Live, but now a thin post-release page rather than the 2024 campaign site. The July 2024 Wayback capture shows only the empty red/black split shell (`longlegs-2024-desk-fold.png`).
- **objectandanimal.com**. Certificate error. The company lives at objectanimal.com.
- **ifcmidnight.com**. Redirects to independentfilmco.com. IFC Films rebranded as Independent Film Company and its horror label no longer has a site of its own.
- **utopiadistribution.com**. Only the header and one headline rendered. The carousel and grid stayed empty.

## Index

| Site | Kind | URL | Shots (prefix in `research/shots/`) |
|---|---|---|---|
| Longlegs | Neon horror film site | longlegs.film | `longlegs-`, `longlegs-2024-` |
| The Birthday Murders | Neon ARG site (dead) | thebirthdaymurders.net | `birthdaymurders-`, `birthdaymurders-2024-` |
| Cuckoo | Neon horror film site (dead) | cuckoo.film | `cuckoo-`, `cuckoo-2024-` |
| Immaculate, The Monkey | Neon horror film sites (dead) | immaculate.film, themonkeyfilm.com | `immaculate-`, `immaculate-2024-`, `themonkey-` |
| Neon | Distributor | neonrated.com, /film/keeper | `neon-home-`, `neon-keeper-` |
| Blumhouse | Horror studio | blumhouse.com | `blumhouse-` |
| Shudder | Horror streamer | shudder.com | `shudder-` (+ `-scroll1..3`) |
| Mubi | Distributor/streamer | mubi.com/en/us, /en/notebook | `mubi-`, `mubi-notebook-` |
| Annapurna | Studio | annapurna.com | `annapurna-` (+ `-hover1..2`) |
| Searchlight | Distributor | searchlightpictures.com | `searchlight-` |
| Independent Film Company (IFC Films, IFC Midnight) | Distributor | independentfilmco.com | `ifc-`, `ifcmidnight-` |
| Utopia | Distributor | utopiadistribution.com | `utopia-` |
| Criterion | Label | criterion.com, /closet-picks | `criterion-`, `criterion-closet-` |
| Janus Films | Distributor | janusfilms.com | `janus-` |
| Pulse Films | Production company | pulsefilms.com | `pulse-` |
| Park Pictures | Production company | parkpictures.com | `parkpictures-` |
| Somesuch | Production company | somesuch.co | `somesuch-` |
| Smuggler | Production company | smugglersite.com | `smuggler-` (+ `-scroll1..3`) |
| Object & Animal | Production company | objectanimal.com, /film-and-tv | `objectanimal-`, `objectanimal-filmtv-` |
| Caviar | Production company | caviar.tv | `caviar-` (+ `-scroll1..3`) |
| Prettybird | Production company | prettybird.co | `prettybird-` (+ `-scroll1..3`) |
| Hungryman | Production company | hungryman.com | `hungryman-` (+ `-scroll1..3`) |
| Radio Silence | Small horror production outfit | hiradiosilence.com | `radiosilence-` |
| Divide/Conquer | Horror production company | divideconquer.us | `divideconquer-` |

Each prefix has `-desk-fold.png`, `-desk-full.jpg` and `-mob-fold.png` unless noted.

---

## Part 1. The horror campaign sites

The main finding surprised me. Neon's per-film sites run on one vendor template, Powster's "movie platform". Cuckoo and The Monkey carry the Powster footer credit, and the 2024 Longlegs and Immaculate captures share its proxima-nova, its "Title | Official Website | Date" page titles and its round icon-button shell. Each one is a split screen: key-art poster on the left (about 42% of the width), showtimes and ticketing on the right, round icon buttons for menu and close, and a Share link. A film gets its identity from three swaps: the poster, one display face, and one color pair. Everything else is proxima-nova and ticketing UI, and the sites go dark or vanish within two years of release.

So the "themed" feeling people remember is key art plus one typeface plus one color, carried by a shared template. A two-person company can afford that.

### Longlegs (live, post-release)

URL: https://www.longlegs.film. Shots: `longlegs-desk-fold.png`, `longlegs-desk-full.jpg`, `longlegs-mob-fold.png`. Archive shell: `longlegs-2024-desk-fold.png`.

- Type. Only system fonts, Arial and Georgia. The distressed red title is artwork. Section heads are Arial 52px uppercase with 5px tracking ("SYNOPSIS", "FILM DETAILS"). Body is Georgia 30px on a 48px line. The credit line "A FILM BY OSGOOD PERKINS" is Arial 12px uppercase with 7px tracking (0.58em). Nav is Arial 12px caps, 2px tracking, centered. Buttons are 11px caps with 2px tracking.
- Color. Hero is a radial glow, #25201C at the center falling to #060606 at the edges, like one bare bulb in a black room. Text #E8E3D8. Secondary text #BBB4A8 and #A79D90. The title is pure #FF0000. The credits section flips to a bone panel, #E3DFD4 with #151412 text. The closing band is #14100F.
- Layout. Single centered column. The hero is 100vh: red title about 780px wide, "WATCH NOW ON DEMAND" under it in the same red, the tracked credit line, then two square-cornered 1px outline buttons ("ENTER", "OFFICIAL NEON PAGE"). "SCROLL TO UNCOVER ↓" sits at the bottom in 11px tracked caps. The sections below sit in a column starting at x=220 (about 1000px wide). Each has a tiny tracked eyebrow ("THE FILM", "LONGLEGS · 2024") above the 52px head. Credits use a two-column grid of 11px tracked caps labels ("DIRECTED BY", "WRITTEN BY", "STARRING", "GENRE") over Georgia 20px values.
- Closing line. "Every clue leads closer to something that should never have been found." Georgia 54px, centered, on the #14100F band.
- Motion. None visible. "Scroll to uncover" does the suggesting.
- Copy tone. Terse and investigative ("The investigation", "Scroll to uncover").
- Why it matters. The whole page costs nothing. It's two system fonts, a radial gradient, square outline buttons and a bone panel for credits. The dread comes from the dark field, the wide tracking and one red.

### The Birthday Murders (archived, June 2024)

URL: https://thebirthdaymurders.net (dead). Shots: `birthdaymurders-2024-desk-fold.png`.

- A 1990s personal-homepage pastiche. It uses Times at browser defaults, gray #CFCFCF table cells with bevelled borders, a left nav column with yellow folder icons ("Home", "The Victims", "Contact"), and underlined blue links. Behind it all is a tiled black-and-white crime-scene photo. "LONGLEGS" is set in red Times bold, followed by "Tune back in Monday, June 24th!"
- Copy is in-world and deadpan: "this Satan-worshipping psycho has terrorized families throughout the Pacific Northwest."
- There are no effects. The period-correct HTML is the texture. It's also a marketing stunt tied to a release date, and the domain is already gone.

### Cuckoo (archived, August 2024)

URL: https://cuckoo.film (dead). Shots: `cuckoo-2024-desk-fold.png`.

- A Powster split. Full-height poster on the left. On the right, near-black green #031714 with an oxblood #6B1B1A showtimes bar, and a city search field ("Washington, D.C. showtimes") in a heavy display face. Round oxblood icon buttons (#821E1D) sit at top left. The tool reports Talisman as the film's display face, used for "Fear its call" and "NOW PLAYING" over the poster.
- The capture shows the template's error state ("Oh no! Looks like you encountered an error.") because archived API calls fail. That tells you how much of these sites is live ticketing data.

### Neon (neonrated.com and the Keeper film page)

URLs: https://www.neonrated.com, https://www.neonrated.com/film/keeper. Shots: `neon-home-desk-fold.png`, `neon-home-desk-full.jpg`, `neon-home-mob-fold.png`, `neon-keeper-desk-fold.png`, `neon-keeper-desk-full.jpg`, `neon-keeper-mob-fold.png`.

- Type. Girott for display and Focal for UI. The hero title "FJORD" is Girott 700 at 160px (11vw), uppercase, -4.8px tracking (-0.03em), line-height 0.9, sitting bottom-left over a full-bleed still. Section heads are Girott 41px uppercase with tight tracking ("IN THEATERS", "WATCH NOW", "AWARD WINNERS", "BEST SELLERS"). Tile titles are Focal about 15px uppercase, set below the image.
- Nav. A floating card about 350px wide, centered 35px from the top, holding the hamburger, wordmark and four icons (search, heart, account, cart). A black strip under it carries a thumbnail and "GET TICKETS →". On the Keeper page the card fills with the film's accent and the strip reads "WATCH NOW $5.99".
- Per-film theming. Keeper's accent is #02FBE8, a bright cyan. It fills the nav card, colors the title "KEEPER" (Girott, about 120px), the year, and the pager dots. The hero still behind it is a desaturated, shallow-focus close-up of a face. One color variable carries the whole film.
- Film page body. White, with three columns under hairlines. On the left, a trailer thumbnail (230x160, 6px radius, outline play triangle). In the middle, "SYNOPSIS" (Focal 13px bold caps label, hairline, then 20px body). On the right, "ADDITIONAL DETAILS" with "DIRECTED BY" and "STARRING" label-value pairs.
- Pull quotes. A full-bleed dark still, the quote in Girott about 40px white at the left ("An experience of true terror"), the source in small serif caps at the right ("FEDE ALVAREZ"), and accent-colored dots below.
- Rows. Horizontal carousels of 16:9 stills, four across at about 347px with 4px gutters and 6px radius. Tiny square arrow buttons sit beside each section head. An outlined text tag marks status: "IN THEATERS OCT 9, 2026".
- Newsletter. A full-bleed still in a rounded 1380px panel. The field placeholder "ENTER YOUR EMAIL ADDRESS" is set in Girott about 36px with a 1px white underline and a long arrow at the right end.
- Footer. Link groups in separate bordered, rounded boxes.
- Copy tone. Labels only, no taglines.
- For MindInMotion. Neon uses nearly the same cyan as MIM's #00E6F8 as the accent for a horror film, and it reads as cold and clinical. MIM doesn't need to trade the cyan for blood red to feel genre.

---

## Part 2. Studios, labels and distributors

### Blumhouse

URL: https://www.blumhouse.com. Shots: `blumhouse-desk-fold.png`, `blumhouse-desk-full.jpg`, `blumhouse-mob-fold.png`.

- Type. Lato for body and section heads (27px bold caps, 3px tracking: "NEW MERCH ALERT", "FILMS", "TV", "GAMES"). Pathway Gothic One 30px caps for "LEARN MORE" links. program-narrow 80px caps for hero slide titles.
- Color. Charcoal #1A1A1A page, white text, teal accent #00B0C2 on chevrons and the cookie bar.
- Hero. A 100vh slider of dark film stills with title art in the bottom-left ("OBSESSION", white letters with a red and blue chromatic fringe). Four hollow-circle dots mark the slides.
- Layout. The body is a stack of division rows: Films, TV, Games, plus a merch row. Each row is a two-column split, the image about 920px wide (two thirds) and text in the other third, alternating sides. Heading and one sentence sit at the top of the text column. "LEARN MORE" with a teal chevron is pinned to the bottom of the column, level with the image's bottom edge. A 1px gray rule closes each row, with a short vertical tick at its end.
- Copy tone. Dry, with a little bite: "From upcoming releases to those still living rent-free in your nightmares." "Whether you're into psychological thrillers, legal dramas, or people at their very worst." "It's time to play."
- For MindInMotion. This is the cleanest structure in the set for a company with two kinds of work: a Client work row, an Our films row, a Post-production row, one wry sentence each.

### Shudder

URL: https://www.shudder.com. Shots: `shudder-desk-fold.png`, `shudder-desk-full.jpg`, `shudder-mob-fold.png`, `shudder-scroll1.png` to `shudder-scroll3.png`.

- Hero. A wall of about 40 posters in columns tilted roughly 15 degrees, the columns staggered vertically. Every poster is tinted into one red duotone (#110101 in the shadows through #4B0700 to warm orange highlights). A pill button, "START YOUR FREE TRIAL", sits in #C80000. On mobile the wall sits behind the red wordmark and "SO GOOD, IT'S SCARY" in Archivo Black about 40px, white, centered, over "Horror. Thriller. Supernatural."
- Rows. Named shelves: "SEASON OF SCREAMS / Your Home for Horror", "TIMELESS TERRORS / Legendary classics that prove fear never fades", "HORROR MASTERPIECES / The gold standard of true terror". Each is a wide still washed with a color gradient (red from the left, or teal) and a row of seven posters, about 110x160, below it.
- Texture. One row uses a datamosh or pixel-sort effect: a man's face broken into displaced rectangular blocks with horizontal scanline banding.
- Type. Archivo Black for heads, Roboto and Inter for body.
- Why it matters. The single-hue duotone makes 40 unrelated posters read as one image. MIM has dozens of mismatched client stills (preschool tables, warehouses, labs), and the same treatment would make them sit together.

### Mubi

URLs: https://mubi.com/en/us, https://mubi.com/en/notebook. Shots: `mubi-desk-fold.png`, `mubi-desk-full.jpg`, `mubi-mob-fold.png`, `mubi-notebook-desk-full.jpg`.

- Riforma throughout. Headlines are uppercase, about 60px. The button is deep blue #001489.
- The landing page is a signup funnel. It stacks full-bleed film stills with caps statements. "ANY FILM. / ANY SCREEN. / ANY TIME. / ANY WHERE." is four stacked lines at about 32px. A statement block lists "EVERYWHERE'S BEST CINEMA. CURATED BY FILM LOVERS. BY HAND." in gray caps, one clause per line.
- Notebook is a conventional three-column magazine. Category tags are white 13px text in the image's top-left corner, with a byline and date row over a hairline.
- Not much here for MindInMotion beyond stacked caps statements.

### Annapurna

URL: https://www.annapurna.com. Shots: `annapurna-desk-fold.png`, `annapurna-hover1.png`, `annapurna-hover2.png`, `annapurna-mob-fold.png`. The full JPG is only 900px tall because the homepage is a single screen.

- Layout. The homepage is an index: a vertical list of about 14 project titles in Gerstner-Programm 35px, on a 72px pitch, left-aligned at x=40, white. Behind the list, a full-bleed video or still of the active project fills the screen. Hovering a title swaps the background to that project's footage, dims the hovered title to about 60% gray, and puts a bullet before it. A black gradient covers the left 45% so the list stays readable. Titles near the bottom of the screen fade out behind a mask.
- Each title carries a tiny superscript icon for its medium (film camera, game controller, TV, theater masks). The same icons sit top-right as filters.
- Chrome. The logo mark is at top-left. A marquee runs across the top ("CONTROL RESONANT OUT 9/24!! • SILENT HILL : TOWNFALL OUT 9/24!!") in 15px caps, gray. At bottom-right, a 1px outlined pill holds "ABOUT JOBS NEWS" in a typewriter-style face (the tool reports Yorick) at about 13px, tracked.
- Mobile keeps the list at about 28px over a darkened still.
- For MindInMotion. This is the cheapest cinematic homepage in the set: a list of titles and one still per title. MIM has 30-plus real stills and a list of film and client titles. The superscript tag can mark spot, feature, short or music video.

### Searchlight

URL: https://www.searchlightpictures.com. Shots: `searchlight-desk-fold.png`, `searchlight-desk-full.jpg`, `searchlight-mob-fold.png`.

- Type pairing. A condensed bold sans wordmark wrapped in Playfair italic: "Your favorite movie is a / SEARCHLIGHT / movie". Feature titles are Playfair at 48 to 64px, and each film's title gets its own color (Black Swan in #E6271D, a streaming partner in #1CE783). Body is Outfit 15px.
- Links. "WATCH TRAILER" and "WATCH NOW" are italic serif caps at about 20px, followed by a 1px hairline arrow between 40 and 190px long.
- Feature block. An inset 16:9 still about 700px wide on a black page, with "NOW STREAMING" in 15px caps and the italic serif title ("Ready or Not 2: Here I Come") to the right, overlapping the image's right edge. The synopsis is 15px, under the image.
- Why it matters. An italic serif with a hairline arrow makes a call to action read like a film credit instead of a SaaS button.

### Independent Film Company (formerly IFC Films; IFC Midnight redirects here)

URL: https://www.independentfilmco.com. Shots: `ifc-desk-fold.png`, `ifc-desk-full.jpg`, `ifc-mob-fold.png`, `ifcmidnight-desk-fold.png`.

- The hero autoplays a muted trailer and shows the player's state under the title: a pause glyph, the timecode "00:01 / 02:32", and a mute icon, all in yellow. The title "The Stunt Driver" is Montserrat bold, about 60px, yellow, bottom-left.
- Only the hero rendered in the full-page capture.
- Why it matters. Printing the timecode on a hero loop is a filmmaker's detail that costs one line of markup.

### Utopia

URL: https://utopiadistribution.com. Shots: `utopia-desk-fold.png`, `utopia-desk-full.jpg`, `utopia-mob-fold.png`.

- Partly rendered. A black page, "SUMMER TOUR" in Barlow heavy caps about 70px, a carousel reduced to one tiny thumbnail with a pause button, and a white rounded footer panel. The fonts are Barlow and Alternate Gothic No3. Nothing here I'd hand to a designer.

### The Criterion Collection

URLs: https://www.criterion.com, https://www.criterion.com/closet-picks. Shots: `criterion-desk-fold.png`, `criterion-desk-full.jpg`, `criterion-mob-fold.png`, `criterion-closet-desk-full.jpg`.

- The homepage is a stack of 100vh panels, each built from one release's key art. The top panel tints a misty forest photo to a single green (#007700 to #007F00), the title is condensed caps in the same green, and the button is a flat gray square ("WATCH NOW ON THE CHANNEL"). "THE CRITERION COLLECTION" runs vertically up the left edge in 10px tracked caps, with a vertical dot pager below it.
- Nav is Mercury Text serif at 19px, with "Current" in italic. Gotham Narrow handles caps labels. The accent is gold #B4841E.
- Closet Picks is a repeating format: the same room, the same framing, a different guest every time. The photo is about 705px wide and left-aligned. A white caption card overlaps its bottom edge, holding an italic serif kicker ("Watch & shop"), a bold tracked caps title ("DAKOTA FANNING'S CLOSET PICKS"), and a 150px black underline.

### Janus Films

URL: https://www.janusfilms.com. Shots: `janus-desk-fold.png`, `janus-desk-full.jpg`, `janus-mob-fold.png`.

- Type. Freight Neo for caps heads (48px, +2.4px tracking, "UNZIPPED"), Freight Text for body and the italic kicker ("Now Playing!" in taupe #A19890). Links and buttons are rust #A85B38.
- Hero. A black-and-white still with arrow buttons and a "1/5" counter inside a thin 50px circle. Below it is a #272727 band with the italic tab, the title, one sentence, and a round double-ring "VIEW" button outlined in rust.
- About. An archival black-and-white photo of a small cinema with an "Opening soon, foreign films" sign in the window, with the coin logo ghosted behind it at about 15% opacity, overlapping the photo's corner. The paragraph is set in Freight Text with director names as rust inline links, then a solid rust "BROWSE ALL FILMS" bar.
- For MindInMotion. An origin photo in black and white with the mark ghosted behind it. MIM already has one, `20150810_175223-2-1.webp` (black-and-white, crew hiking a foggy hillside with a boom pole).

---

## Part 3. Production companies (the structural references)

These matter most, because they sell the same thing MIM sells: people who make films for clients. Not one of the ten shows a stat counter, a service icon grid or a testimonial carousel. They credit the work in a single line (client, title, director) and let the frames carry the rest.

### Pulse Films

URL: https://pulsefilms.com. Shots: `pulse-desk-fold.png`, `pulse-desk-full.jpg`, `pulse-mob-fold.png`. The homepage is one screen.

- Layout. Bottle green #14241F fills the viewport. A video plays inset inside a 32px green frame on all sides. Four nav words sit in the corners of the frame: DIRECTORS top-left, WORK top-right, ABOUT bottom-left, CONTACT bottom-right. A custom stencil wordmark, cream, about 440px wide, sits centered over the video.
- Type. The nav is Aether AMono (the tool also lists GT Pressura Mono) at 16px uppercase with 1.12px tracking, cream #EBEADB.
- Mobile. The frame stays. The video becomes a tall portrait panel with about 20px of green around it, and the corner words collapse into a hamburger.
- Motion. Only the looping footage.
- For MindInMotion. Four-corner nav around a framed loop. Work, Films, About and Contact map straight onto it, and the frame reads like a matte or a viewfinder.

### Park Pictures

URL: https://parkpictures.com. Shots: `parkpictures-desk-fold.png`, `parkpictures-desk-full.jpg`, `parkpictures-mob-fold.png`.

- Layout. The homepage is a vertical stack of 100vh video panels, one spot per panel. Each panel is captioned "Client - Title" in Untitled Sans 36px white ("Nike - Chance", "Kellogg's Raisin Bran - Will Shat"), with the director in 24px below, placed at the left edge around mid-height.
- Motion. Panels below the current one sit heavily blurred (roughly a 30px Gaussian) inside a dark inner vignette. They sharpen as they scroll into place, like a focus pull.
- Nav. "PARK PICTURES" in bold tracked caps at left, a small tree icon at center, text links at right (Directors, Work, Film & Television, About, News, Contact) at 15px. On mobile the wordmark stretches the full width of the screen.
- Type. Untitled Sans only, with -0.05px tracking. Dates are 10px.

### Somesuch

URL: https://somesuch.co. Shots: `somesuch-desk-fold.png`, `somesuch-desk-full.jpg`, `somesuch-mob-fold.png`.

- Type. Every item's headline is a credit line in Lateral Expanded Heavy, 48 to 64px (3.3 to 4.4vw), line-height 0.96: "CLIQUA for U2, Silencio", "Alfie Whiteman for Tottenham Hotspur, Tottenham 'Til I Die", "Beatrice Gibson, At Night". One line of context sits under it in Lateral Extended Medium 20px. The wordmark "somesuch" is a small lowercase heavy word at top-left, with a two-bar menu icon at top-right.
- Color. White page, black type. Rust #AF3D2C shows up in the shop and near-black #120908 in footers.
- Grid. Items break a 12-column grid on purpose. One spans columns 3 to 10, the next runs full width, the next sits in 7 to 12, the next in 1 to 8. Some media rows overflow to the right, with a second image (a poster) peeking in from the edge.
- Mobile. Same credit lines, stacked, still heavy, about 30px.
- For MindInMotion. The "X for Client, Title" credit line as the headline, for example "Maryland EXCELS, Good Mom" or "For Johns Hopkins AAP, Cuba Field Course". It also meets the audit rule that every tile shows title and client.

### Smuggler

URL: https://smugglersite.com. Shots: `smuggler-desk-fold.png`, `smuggler-desk-full.jpg`, `smuggler-mob-fold.png`, `smuggler-scroll1.png` to `smuggler-scroll3.png`.

- Fold. Warm paper #FCF5E8 with a slow, smudged charcoal brushstroke video across the right two-thirds. "SMUGGLER" is ABC Diatype 800 at 57.6px, caps, -1.8px tracking, khaki #BEB28E, top-left. The nav is Diatype 700 at 18px caps in #343E3B, spread evenly across the top (COMMERCIAL, MUSIC VIDEO, THEATRE&LIVE, FILM&TV, WORK, ABOUT). The bottom row is 12px: socials at left, then "Culture", then the city names spread across the full width (Los Angeles, New York, London).
- Below the fold. The page turns black and the header becomes a cream bar. News rows alternate a third of text with two thirds of image. Headlines are Diatype 500 at 48px, uppercase, tight, each row in its own muted color (tan #BEB28E, copper). The date is 13px. The excerpt is pinned to the bottom of the text column so it lines up with the image's bottom edge.
- For MindInMotion. City names spread across the bottom of the first screen, "Baltimore" and "Orlando", with the phone numbers as `tel:` links.

### Object & Animal

URLs: https://objectanimal.com, https://objectanimal.com/film-and-tv. Shots: `objectanimal-desk-fold.png`, `objectanimal-desk-full.jpg`, `objectanimal-mob-fold.png`, `objectanimal-filmtv-desk-full.jpg`.

- Type and color. Light gray #F2F2F2 and near-black text. Everything is lowercase in Circle at 15px, with 42%-opacity gray for labels. The mission line on Film & TV is 22.8px.
- Home. The logo ("object & animal") sits in a frosted-glass rounded card (about 200x125, 16px radius, backdrop blur) at the top-left, over an inset video with 8px margins. The caption at the bottom-right is small gray lowercase: "troye sivan, party". Scrolling down, small videos about 620px wide sit left or right with a lot of empty space around them. Each has the director at left and "artist, 'title'" at right, underneath.
- Film & TV. Each project is a rounded card with a 1px border, about 1020px wide: poster on the left, a data sheet on the right. Lowercase gray labels sit over black values: title / directors / synopsis / category / status. The status values are plain: "released 2025, available on disney+", "in post production".
- For MindInMotion. A film slate as records with a status field. Incubation would read "status: screening at festivals". Bad Witch would read "released 2018".

### Caviar

URL: https://caviar.tv (redirects to /los-angeles/). Shots: `caviar-desk-fold.png`, `caviar-desk-full.jpg`, `caviar-scroll1.png` to `caviar-scroll3.png`.

- Intro. The wordmark works as a mask, with footage playing inside letterforms about 330px tall on white. "LOS ANGELES" sits under it in 20px caps.
- Work. An offset collage of video tiles of different widths on #F1F1F1. Each has a centered caption, `Client – Title` in Moderat 26px, with `By – Director` under it in GT Super at about 14px. Captions on tiles away from the focus fade to gray.
- Statement. "Caviar is an independent film studio based in Los Angeles, London, Brussels, Paris and Amsterdam. Our film Sound of Metal won two Academy Awards in 2022..." GT Super Display 32px regular, black, left-aligned, about 70 characters to the line. Facts only.
- For MindInMotion. The plain factual paragraph in a large text serif as the About moment (without the awards, see What not to copy).

### Prettybird

URL: https://prettybird.co (redirects to /us/). Shots: `prettybird-desk-fold.png`, `prettybird-mob-fold.png`, `prettybird-scroll1.png` to `prettybird-scroll3.png`.

- Layout. A black page with a bird-foot mark centered at the top and "MENU" at top-right in 20px. Work items are inset videos about 1000px wide, never full-bleed. The director's name runs in Buch at 100px uppercase and hangs past the image's left edge onto the black. Under it, the client in Halbfett 36px caps and the title in Buch 36px caps ("AUTODESK THE WORLD IS YOURS FOR THE MAKING"). The scroll cue is "Explore" over a 1px vertical line.
- News items use a narrower image (about 540px) with the headline in 40px white running off the image's right edge onto black ("Inside 'Sterling Point': Why Megan Park's YA Series..."), and the source underneath ("The Hollywood Reporter").
- Why it matters. Type that hangs over the edge of an inset image makes the frame feel composed instead of boxed.

### Hungryman

URL: https://hungryman.com. Shots: `hungryman-desk-fold.png`, `hungryman-desk-full.jpg`, `hungryman-mob-fold.png`, `hungryman-scroll1.png` to `hungryman-scroll3.png`.

- Hero. Full-bleed video with slightly rounded viewport corners. The company monogram is drawn as a single 1px white outline about 1340x635px, laid over the footage like a matte line. The nav has the "hungryman" wordmark at left and four links spread across the top in NeueMontreal 12px caps. A bottom bar shows "ROSE DELIGHTS / Collage" at left (bold caps client over regular title), "DIRECTOR / Dan Opsal" in the middle, and a 16-dot pager at right with the active dot drawn as a pill. On mobile the outline redraws to fit the portrait frame.
- Footer. Cream #F7F4ED fading to pale blue #CEDAE2. "See All Directors →" in NeueMontreal 38px, then four 12px columns (LOCATIONS, NAVIGATION, FOLLOW US, NEWSLETTER with an underlined field), and a plain "ABOUT" line: "hungryman is an independent production company based in Los Angeles, New York, London, and São Paulo."
- For MindInMotion. The MIM "M" drawn as a 1px outline over the reel loop. It uses the one brand asset they already own.

### Radio Silence

URL: https://www.hiradiosilence.com. Shots: `radiosilence-desk-fold.png`, `radiosilence-desk-full.jpg`, `radiosilence-mob-fold.png`.

- The closest in spirit to MIM: a small horror collective (Ready or Not, Scream, Abigail) with a personal site. Black page, a red stacked-bar logo (#CD322B). The nav is set in chandler-42, a typewriter face, at 12px lowercase with 2.4px tracking, red at 90% opacity, the current page in white: "home, movies, alt. posters, chad, matt & rob, the crawl podcast, soundtracks, posters, gifs, press, contact".
- The homepage is their seven films drawn as worn VHS clamshell spines standing side by side (about 1240px), with rental stickers, "SALE $9.95" and "HI FI" labels. A credit sits under it in the typewriter face: "Art by Shawn Mansfield".
- For MindInMotion. The films shelved as physical objects, and an About page named after the people ("chad, matt & rob"). The spines are commissioned illustration, though. The cheap route is to build them in CSS (see move 17).

### Divide/Conquer

URL: https://www.divideconquer.us. Shots: `divideconquer-desk-fold.png`, `divideconquer-desk-full.jpg`, `divideconquer-mob-fold.png`.

- A horror producer with big hits (The Black Phone 2, M3GAN, Freaky) runs a plain Squarespace page. It's light gray, with a condensed black stacked wordmark "DIVIDE / CONQUER", three nav links in futura-pt 13px tracked caps, and a four-column grid of square poster crops (about 204px, 28px gutters) with centered gray 12px caps titles. A mailing-list modal opens over it ("We have a mailing list! ... We promise minimal emails.").
- Why it matters. It shows a genre producer's site can be a quiet poster grid. That only works because every title has studio key art, and MIM doesn't have that.

---

## Patterns across the set

- The studio sites that feel themed get it from three things per title: one display face, one accent color, one strong image. A template does the rest (Neon, Powster, Searchlight's colored titles, Criterion's panels).
- Production companies credit work in a single line (client, title, director). None of the ten production sites shows a stat counter, a service icon grid, or a centered "What our clients say" section. Those are exactly the parts of the current MIM site that read as a template.
- Nav words are few and spread out: four corners (Pulse), evenly spaced across the top (Smuggler, Hungryman), or inside one small pill (Annapurna).
- Rounded pill buttons show up only on consumer funnels (Shudder, Mubi's signup). The production sites use text links, hairline arrows or square outline buttons.
- Inset images with a margin around them (Pulse, Prettybird, Object & Animal, Somesuch) are as common as full-bleed. An inset frame reads like a print on a wall.
- Texture is rare and aimed at one spot: Shudder's datamosh on one row, Longlegs' radial vignette, Smuggler's paper tone. Nobody lays grain over the whole page.
- Copy is short and plain. The best lines are either a dry joke (Blumhouse) or a factual sentence (Caviar, Hungryman).

---

## Moves a two-person production company could steal

1. **Title index homepage (Annapurna).** List 10 to 14 titles, mixing the films with the strongest client pieces, in a clean sans at 32 to 36px on a 70px pitch, left-aligned at 40px. Hovering or focusing a title swaps the full-bleed background to that project's still (`bad-witch.webp`, `vimeo-1173635320.webp`, `Screen-Shot-2022-06-24-at-6.14.31-PM-2.webp`). Put a black gradient over the left 45% so the list stays readable. A small superscript tag ("spot", "feature", "short", "music video") replaces Annapurna's icons. Every title is a real link, and keyboard focus triggers the same swap as hover. Under reduced motion the swap is instant, with no crossfade.
2. **Four-corner nav around a framed loop (Pulse).** Put a 24 to 32px solid frame in one deep color around the reel poster or silent loop. Set WORK top-left, FILMS top-right, ABOUT bottom-left and CONTACT bottom-right in a monospace at 14 to 16px caps with about 0.07em tracking. "Tell us about your project" goes under the frame or becomes the CONTACT label. On a phone the frame stays and the video goes portrait.
3. **Division rows for the two kinds of work (Blumhouse).** Three rows (Client work, Our films, Post-production), each two-thirds image and one-third text, alternating sides. Each gets a heading, one dry sentence, and a text link pinned to the bottom of the column, closed by a 1px rule. Suggested images: `checklist.webp`, `bad-witch.webp`, `011A1266.webp` (grading panel).
4. **Credit-line headlines (Somesuch, with the Prettybird overhang as a variant).** Caption every work item as "Client, Title" in an extended or heavy grotesk at 48 to 64px, line-height 0.96. For example "Maryland EXCELS, Good Mom" or "For Johns Hopkins AAP, Cuba Field Course". Stagger the items across a 12-column grid (3 to 10, then 1 to 12, then 7 to 12, then 1 to 8). In the Prettybird variant, the title runs about 100px and hangs 80px past the left edge of an inset still.
5. **One template, one accent per project (Neon's Keeper page, Powster).** Build a single project-page template. Each project sets `--accent`, a hero still, and optionally one display face. For example: Bad Witch in the orange of its rim light, Don't Go Hiking in a dried-blood red, Ghost Light in stage gold. Keep MIM's cyan as the studio color, since Neon runs #02FBE8 as a horror accent on Keeper and it holds up.
6. **Three-column credit block on project pages (Neon film page).** Trailer thumbnail with a visible play triangle | "THE BRIEF" | "CREDITS" (client, directed by, shot by, year). Labels are 12 to 13px bold caps over a hairline, values 18 to 20px. It's a real `<button>` with a name like "Play Infinite Legacy, Joe".
7. **Film slate as records with a status field (Object & Animal).** One card per feature: still or key art on the left, then lowercase gray labels over values (title / directed by / shot by / synopsis / status). Status in plain words: "screening at festivals" for Incubation, "released 2018" for Bad Witch. Name no festivals.
8. **Testimonials as pull-quote slides (Neon).** A full-bleed dark still, the quote in the display face at 36 to 44px across the left 40%, the name in small serif caps at the right. Use the four real quotes verbatim (Perillo, White, Moody, Lanzino). This replaces the centered "What Our Clients Say" cards.
9. **Duotone wall to unify mismatched stills (Shudder).** Put 20 to 30 client stills through one hue (grayscale plus `mix-blend-mode: multiply` over the accent, or an SVG `feColorMatrix`). Set them in columns tilted 8 to 15 degrees behind a single headline. The wall is decorative and `aria-hidden`. The real, labeled tiles elsewhere keep their color. Any hue works; it doesn't have to be red.
10. **Rack-focus reveal on scroll (Park Pictures).** Work panels enter at `filter: blur(16px) brightness(.7)` and sharpen to zero as they reach the middle of the viewport, captioned "Client - Title" at 36px and the director at 24px. Under `prefers-reduced-motion`, panels render sharp from the start.
11. **The M as a 1px outline over the hero (Hungryman).** Trace `mindinmotion-logo.png` to an SVG and stroke it at 1px white across about 90% of the viewport, over the reel poster or loop. Add a bottom bar with "CLIENT / Title" at left, "DIRECTED BY / Joshua Land" in the middle, and a small pager at right.
12. **Cities across the bottom of the first screen (Smuggler).** "Baltimore (443) 527-5181" pinned bottom-left and "Orlando (407) 584-8891" bottom-right in 12 to 13px, both as `tel:` links, inside the 100vh hero. It replaces the phone numbers crammed into the current header.
13. **Longlegs' system-font kit for the Films section (Longlegs).** Dark #151412 pages with bone #E3DFD4 credit panels, Georgia 28 to 30px body, Arial 11 to 12px caps at 0.5em tracking for the credit line, square 1px outline buttons, and a radial glow (#25201C to #060606) behind each film title. It costs nothing to load. Keep credits accurate: "A film by Joshua Land & Victor Fink" only on the co-directed films (Bad Witch, Ape Canyon, Incubation). Lotus Eyes and I Like Me read "Directed by Joshua Land · Shot by Victor Fink".
14. **Italic serif links with a hairline arrow (Searchlight).** "Watch the reel" in italic serif at 18 to 20px, followed by a 1px line 60 to 120px long ending in an arrowhead. It replaces the white pill buttons on the current site.
15. **Visible timecode on the reel (IFC).** Under the hero headline, show "00:07 / 01:52" and a mute glyph in a 13px mono, updated from the video's `currentTime`. Show only the running time if the page is displaying a poster.
16. **Black-and-white origin photo with the mark ghosted behind it (Janus).** Open About with `20150810_175223-2-1.webp` (crew hiking a foggy hill with a boom pole), with the M at 10 to 15% opacity overlapping its top-left corner. Next to it goes the story: a 16mm class at Johns Hopkins, a company in 2012.
17. **Films shelved as spines, built in CSS (Radio Silence).** Each film is a spine 70 to 90px wide, titled vertically (`writing-mode: vertical-rl`) in its accent color, with the year and format. Hover or focus slides the spine out to show a still. No illustrated art, no fake distributor logos. Name the About page after the people, "josh & victor", the way Radio Silence uses "chad, matt & rob".
18. **A plain factual paragraph in a large text serif (Caviar, Hungryman).** 30 to 32px, about 65 characters to the line: "MindInMotion is Joshua Land and Victor Fink. Since 2012 we've made commercials, PSAs and nonprofit films for Johns Hopkins, the Maryland State Department of Education and the American Lung Association, and features of our own: Lotus Eyes, I Like Me, Bad Witch, Ape Canyon and Incubation." Name the films. Don't count them.

## What not to copy

- **Blood red on black as the whole identity (Longlegs, Shudder).** It works for one film's campaign. On a services site it tells Johns Hopkins and MSDE that MIM only makes horror. Keep the red and the vignettes inside the Films section and the per-film accents.
- **The Powster ticketing split (Neon's film sites).** Poster left, showtimes right, a "GET TICKETS" strip. It's a ticket funnel, and MIM has nothing to book. Its ghost is the round red icon buttons, which show up on every Neon film site.
- **In-universe ARG microsites (The Birthday Murders).** A stunt tied to one release date, and its domain died within two years. If MIM ever does one, it belongs to a single film's launch and lives on that film's own domain, never on the company site.
- **Poster grids and illustrated VHS spines (Divide/Conquer, Radio Silence, Shudder's rows).** They depend on key art for every title. MIM has one key art frame (`og-share.jpg`) and its client work has none. Spines carrying real studio logos (Paramount, MCA, Searchlight, as on Radio Silence) would pass off other companies' marks as MIM's.
- **Award rows and laurels (Neon's "Award Winners" row with Palme d'Or and Oscar glyphs, Caviar's Academy Award paragraph).** The content brief rules out "award-winning" and festival names. A laurel row with nothing in it is worse than none.
- **Merch rows, newsletter-first layouts, marquee tickers (Neon, Blumhouse, Annapurna's "OUT 9/24!!").** They need a merch line and a steady flow of news. A ticker that hasn't changed in four months makes the site look abandoned.
- **A director roster as the main nav (Park, Prettybird, Somesuch, Hungryman's "See All Directors").** These companies represent 20 to 40 directors. MIM is two people, and a "Directors" page with two faces looks padded. Use About and name Josh and Victor.
- **A24 and Neon knockoff signals.** A floating white nav card over a black ticket strip. A neutral grotesk in tiny caps with monospace labels, black and white only. Letterspaced "A FILM BY" on every page. A distressed red title. Any one of these on its own is fine. Three together and the site reads as a costume.
- **The wordmark as a video mask (Caviar) or a custom stencil logo (Pulse).** "MindInMotion" is 12 letters long, so masking video inside it leaves thin slivers of footage, and the trick is common on agency reels. Use the M alone (move 11).
- **Datamosh or glitch effects on people (Shudder).** The people in MIM's client work are real: organ donor families (Infinite Legacy), ALS researchers, preschoolers. Breaking up their faces is a bad look. If the effect gets used at all, it's for horror stills only.
- **Autoplay 100vh video for every project (Park Pictures, Hungryman).** Each panel needs its own hosted loop. Vimeo background embeds are heavy and block headless browsers (see the content brief). Use one loop at most and stills everywhere else.
- **Hover-only reveals.** Annapurna's index and Caviar's fading captions only respond to a mouse. The audit requires a visible play cue without hover and full keyboard use, so every hover state needs a focus state and a touch fallback.
- **Pages that are blank without JavaScript.** Smuggler, Prettybird and Shudder captured blank below the fold, and The Monkey renders nothing at all. Every title, credit and link should exist in the HTML before any script runs.
- **Consent banners over the fold.** Every studio site here opens with one covering the bottom of the first screen. A site with no third-party trackers doesn't need one, so don't add analytics that would force it.
