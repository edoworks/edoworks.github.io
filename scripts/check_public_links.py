#!/usr/bin/env python3
"""Check public distribution links independently of site deployment CI."""

from __future__ import annotations

import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


URLS = (
    "https://edoworks.com/",
    "https://edoworks.com/portfolio/",
    "https://edoworks.com/rung/",
    "https://github.com/edoworks/rung",
    "https://github.com/edoworks/rung/releases",
    "https://pypi.org/project/rung-audit/",
)


def main() -> int:
    failures: list[str] = []
    for url in URLS:
        request = Request(url, headers={"User-Agent": "EdoworksPublicLinkCheck/1.0"})
        try:
            with urlopen(request, timeout=20) as response:
                if response.status < 200 or response.status >= 400:
                    failures.append(f"{url}: HTTP {response.status}")
                else:
                    print(f"ok {response.status} {url}")
        except (HTTPError, URLError, TimeoutError) as error:
            failures.append(f"{url}: {error}")
    if failures:
        print("public link check failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
