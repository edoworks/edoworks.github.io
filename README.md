# edoworks.github.io

Public website for **Edoworks**.

- **Domain:** `edoworks.com` (pending registration, FG-114 — founder
  approval gate. See
  `.factory/reports/2026-07-21-edoworks-brand-infrastructure-5-whys.md`.)
- **Surfaces:** landing (`index.html`), blog (`blog/index.html`), and portfolio
  (`portfolio/index.html`).
- **Build stamp:** every HTML page carries
  `<meta name="generator" content="Edoworks <version>">` and a
  `Built by Edoworks <version>.` footer per
  `.factory/standards/factory-stamp.md`.

## Brand architecture

- **Edoworks** = software engineering work (portfolio + blog at `edoworks.com`).
- **Foculoom LLC** = legal entity (corporate site at `foculoom.com`).

See `.factory/standards/factory-stamp.md` § Brand architecture.

## Local structure

```
edoworks.github.io/
├── CNAME            # edoworks.com (set after domain registration)
├── index.html       # landing (links to portfolio + blog)
├── blog/
│   └── index.html   # blog index (empty until first post)
└── robots.txt
```

## Publishing

This is a GitHub Pages site. Until `edoworks.com` is registered and the
repo is pushed, this directory is a **local scaffold only** — do not push
without founder approval (`AUTHORIZE EDOWORKS SITE PUSH`, gated on
FG-114).
