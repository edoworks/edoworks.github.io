#!/usr/bin/env python3
"""Compare Edoworks's local Rung copy with Foculoom's published status."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
STATUS = "retired and is not an active product or paid offer"
RUNG_PAGES = (
    "portfolio/index.html",
    "rung/index.html",
    "blog/index.html",
    "blog/rung-0-3-1-release.html",
    "blog/rung-0-3-2-release.html",
)


class VisibleText(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.excluded = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("style", "script"):
            self.excluded += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in ("style", "script") and self.excluded:
            self.excluded -= 1

    def handle_data(self, data: str) -> None:
        if not self.excluded:
            self.parts.append(data)


def visible_text(html: str) -> str:
    parser = VisibleText()
    parser.feed(html)
    return " ".join(" ".join(parser.parts).lower().split())


def compare_status(foculoom_html: str, root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    if STATUS not in visible_text(foculoom_html):
        errors.append("Foculoom's live page does not show the expected Rung retirement sentence")
    for path in RUNG_PAGES:
        if STATUS not in visible_text((root / path).read_text(encoding="utf-8")):
            errors.append(f"Edoworks visible copy disagrees with Foculoom: {path}")
    return errors


def main() -> int:
    request = Request("https://foculoom.com/", headers={"User-Agent": "EdoworksCrossDomainStatus/1.0"})
    try:
        with urlopen(request, timeout=20) as response:
            foculoom_html = response.read().decode("utf-8")
    except (HTTPError, URLError, TimeoutError, UnicodeDecodeError) as error:
        print(f"cross-domain status check unavailable: {error}", file=sys.stderr)
        return 1
    errors = compare_status(foculoom_html)
    if errors:
        print("cross-domain status check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("cross-domain Rung status agrees across Foculoom and Edoworks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
