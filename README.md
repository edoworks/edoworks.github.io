# edoworks.github.io

Public website for **Edoworks**.

- **Domain:** `edoworks.com` (live via GitHub Pages and Cloudflare DNS).
- **Surfaces:** landing (`index.html`), blog (`blog/index.html`), portfolio
  (`portfolio/index.html`), and Rung project page (`rung/index.html`).
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
│   └── index.html   # blog index
├── rung/
│   └── index.html   # static Rung distribution page
└── robots.txt
```

## Publishing

This is a GitHub Pages site. Publishing changes requires rendered-page review
and the public-link check.
