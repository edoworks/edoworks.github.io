#!/usr/bin/env python3
"""Fail closed when active pages overstate availability or omit discovery."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
NOWNEST_PAGES = (
    "nownest/index.html",
    "nownest/support/index.html",
    "nownest/privacy/index.html",
    "nownest/terms/index.html",
)
NOWNEST_URLS = {
    "https://edoworks.com/nownest/",
    "https://edoworks.com/nownest/support/",
    "https://edoworks.com/nownest/privacy/",
    "https://edoworks.com/nownest/terms/",
}
FORBIDDEN_CLAIMS = (
    re.compile(r"available (?:now\b|today\b|for download)", re.IGNORECASE),
    re.compile(r"available\s+to\s+download", re.IGNORECASE),
    re.compile(r"download (?:now\b|today\b|on the app store)", re.IGNORECASE),
    re.compile(r"(?:accepted|approved) by apple|apple (?:accepted|approved)", re.IGNORECASE),
    re.compile(r"apple acceptance (?:is |has been )?(?:complete|completed)|(?<!not )completed apple acceptance", re.IGNORECASE),
    re.compile(r"(?:nownest|the app|app)\s+(?:has been|is|was)\s+released|now released", re.IGNORECASE),
    re.compile(r"(?:answers?|answered|responds?|repl(?:y|ies)|response)[^.]{0,30}within\s+(?:one|a|\d+)\s+(?:business\s+)?(?:hour|day)", re.IGNORECASE),
    re.compile(r"(?:can|may|lets? (?:you|users?)|allows? (?:you|users?) to)\s+(?:delete|remove|erase)[^.]{0,40}(?:saved ideas?|ideas?|notes?)[^.]{0,30}(?:one at a time|individually)", re.IGNORECASE),
    re.compile(r"nownest\s*[™®]", re.IGNORECASE),
    re.compile(r"nownest(?: name)?\s+(?:is|is registered as|has become)\s+(?:a\s+)?(?:registered\s+)?trademark", re.IGNORECASE),
)
REQUIRED_PAGE_PHRASES = {
    "nownest/index.html": (
        "saves it locally with the context it interrupted",
        "resume",
        "done",
        "save again",
        "abandon",
    ),
    "nownest/support/index.html": (
        "does not provide an individual hard-delete action",
        "whole-store removal path",
    ),
    "nownest/privacy/index.html": (
        "no analytics",
        "does not create an account",
        "no api calls, cloud sync, or remote storage",
        "network access",
        "does not schedule or send notifications",
    ),
    "nownest/terms/index.html": (
        "provisional product name pending clearance",
        "does not claim trademark registration or adoption",
    ),
}


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    pages = {path: (root / path).read_text(encoding="utf-8") for path in NOWNEST_PAGES}
    combined = "\n".join(pages.values()).lower()
    for phrase in ("free to download", "app release notes"):
        if phrase in combined:
            errors.append(f"unsupported NowNest claim remains: {phrase}")
    for phrase in (
        '"nownest" is a trademark',
        "delete individual",
        "park ideas",
        "park interruptions",
        "review later",
    ):
        if phrase in combined:
            errors.append(f"stale or unsupported NowNest wording remains: {phrase}")
    for pattern in FORBIDDEN_CLAIMS:
        for match in pattern.finditer(combined):
            prefix = combined[max(0, match.start() - 30):match.start()]
            if pattern is FORBIDDEN_CLAIMS[0] and re.search(r"not\s+currently\s+$", prefix):
                continue
            errors.append(f"unsupported NowNest claim pattern remains: {pattern.pattern}")
            break
    for path, text in pages.items():
        normalized = " ".join(text.lower().split())
        unavailable = re.search(r"not currently (?:available|offered) for download", normalized)
        if not unavailable or "qualification" not in normalized:
            errors.append(f"NowNest qualification and unavailability are not both disclosed: {path}")
        if '<meta name="generator" content="Edoworks ' not in text or "Built by Edoworks " not in text:
            errors.append(f"NowNest page lacks the repository page stamp: {path}")
        if '<link rel="stylesheet" href="/nownest/styles.css">' not in text:
            errors.append(f"NowNest page lacks the shared product theme: {path}")
        for phrase in REQUIRED_PAGE_PHRASES.get(path, ()):
            if phrase not in normalized:
                errors.append(f"NowNest public contract is incomplete in {path}: {phrase}")

    all_html = "\n".join(path.read_text(encoding="utf-8") for path in root.rglob("*.html"))
    if re.search(r'href=["\']https?://rung\.edoworks\.com', all_html, re.IGNORECASE):
        errors.append("active page links to failing rung.edoworks.com")
    for href in re.findall(r'href=["\'](/[^"\'#?]*)', all_html, re.IGNORECASE):
        relative = href.removeprefix("/")
        target = root / relative
        if not relative or href.endswith("/"):
            target = target / "index.html"
        if not target.is_file():
            errors.append(f"local link target is missing: {href}")

    portfolio = (root / "portfolio/index.html").read_text(encoding="utf-8")
    if 'class="card card-portfolio" id="nownest"' not in portfolio or "not available for download" not in portfolio:
        errors.append("portfolio lacks the NowNest qualification record")
    home = (root / "index.html").read_text(encoding="utf-8")
    if 'class="product-spotlight" id="nownest"' not in home or 'href="/nownest/"' not in home:
        errors.append("home does not feature the NowNest qualification record")
    nownest_home = pages["nownest/index.html"]
    if "Save it for later." not in nownest_home or "Return to now." not in nownest_home:
        errors.append("NowNest home lacks the approved public headline")
    for asset in ("nownest/styles.css", "nownest/assets/sophie-nest.svg"):
        if not (root / asset).is_file():
            errors.append(f"NowNest product asset is missing: {asset}")

    manifest = json.loads((root / "source-page-manifest.json").read_text(encoding="utf-8"))
    manifest_paths = {page["path"] for page in manifest["pages"]}
    expected_paths = {url.removeprefix("https://edoworks.com") for url in NOWNEST_URLS}
    if not expected_paths <= manifest_paths:
        errors.append("source-page manifest omits NowNest pages")

    sitemap = ET.parse(root / "sitemap.xml")
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    sitemap_urls = {element.text for element in sitemap.findall("sm:url/sm:loc", namespace)}
    if not NOWNEST_URLS <= sitemap_urls:
        errors.append("sitemap omits NowNest pages")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("site claim validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("site claim validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
