# Refined current site (review copy)

The current mindinmotion.tv layout, rebuilt without Tailwind or React, with Concept D's monochrome look and the best parts of the old Squarespace site. It's a design review copy: every page has `noindex`, the canonical links point at mindinmotion.tv, and the contact form doesn't send.

- `ASSESSMENT.md`: the side-by-side of the live site, Squarespace and Concept D, and what the demo keeps, cuts and brings back.
- `COPY-REVIEW.md`: every copy change from the approved Concept D copy, with the old line, the new line and why.
- `_build/build.py`: writes all eight pages. Run it from the repo root with `python3 refined-current-site/_build/build.py` (needs Pillow). Copy, work list, logos and slideshows all live in that file.
- `site.css` and `site.js`: hand-written, no framework.
- `img/`: images only this folder uses (founder photos, generated monochrome client logos, a few crops). Everything else comes from the shared `../assets/img/`.

Client logos are generated from the source files in `../assets/img/` (and `img/logos-src/` for ones added here) into flat bone-colored PNGs in `img/logos/`. A client with no logo file yet shows its name in type.
