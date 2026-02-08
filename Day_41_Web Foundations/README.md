# Day 41 – Web Foundations 🌐

This day focuses on building a strong foundation in web development using HTML, CSS, basic JavaScript concepts, PHP, and JSON. The exercises are organised as small labs and mini-projects so you can explore each concept independently.

Purpose
- Provide a navigable entry point and small starter examples to learn HTML, CSS, JSON and basic backend concepts.
- Offer tiny projects that show how files talk to each other in a real web workflow.

Topics Covered
- HTML elements and document structure (headings, paragraphs, lists)
- Links, images, and void elements
- Forms and basic PHP form handling
- CSS: inline, internal, external
- CSS selectors, colors, fonts, and the box model
- Simple projects (Movie Ranking, Birthday Invite, Motivation Meme)
- JSON structure and parsing; small JS examples that fetch JSON
- Intro to server-side: PHP demo and a tiny FastAPI/Python pointer in `KnowJSON`

Why This Day Matters
These fundamentals are the base of modern web applications. A solid understanding here makes frameworks like React, Django, and FastAPI much easier to learn later.

Status
- ✔ Completed as learning labs and mini-projects

Quick Links
- `index.html` — top-level navigator for Day 41 examples
- `starter-html.html` — minimal HTML starter
- `starter-json.html` — small JSON fetch demo
- `forms/input.html` — form examples that link to `forms/server.php`
- `KnowJSON/data.json` — sample JSON referenced by starter pages

How to use / Quick start
1. Open the top-level `index.html` in a browser for quick navigation.
2. For local static preview (recommended):

```bash
# from the Day 41 folder
python -m http.server 8000
# then open http://localhost:8000 in your browser
```

3. To test PHP examples (uses `forms/server.php`):

```bash
cd "c:/100 days of python code/Web Foundation Day 41"
php -S localhost:8000
# then open http://localhost:8000/forms/input.html or
# http://localhost:8000/forms/server.php
```

Notes
- `starter-json.html` and the index attempt to fetch `KnowJSON/data.json`. If that file is not present or you want to try different data, edit or replace it.
- The PHP demo (`forms/server.php`) is intentionally simple and meant for teaching — don't use it as-is in production.

Want more?
- I can add a short `php-intro.md` with exercises, or a tiny `serve.ps1`/`serve.sh` helper to start local servers. Tell me which and I'll add it.

