#!/usr/bin/env python3
"""Check public distribution links independently of site deployment CI."""

from __future__ import annotations

import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


URLS = (
    "https://edoworks.com/",
    "https://edoworks.com/portfolio/",
    "https://edoworks.com/rung/",
    "https://edoworks.com/mews-and-woofs/",
    "https://github.com/edoworks/rung",
    "https://github.com/edoworks/rung/releases",
    "https://pypi.org/project/rung-audit/",
    "https://mews-and-woofs.foculoom-5388.chatgpt.site/",
    "https://rung-evidence.foculoom-5388.chatgpt.site/",
    "https://buy.stripe.com/5kQ7sL2zx3snavce9t9AA03",
    "https://buy.stripe.com/dRm8wP2zxd2X32KaXh9AA08",
    "https://buy.stripe.com/5kQfZheif1kf6eW5CX9AA09",
)


def main() -> int:
    failures: list[str] = []
    for url in URLS:
        request = Request(url, headers={"User-Agent": "EdoworksPublicLinkCheck/1.0"})
        for attempt in range(3):
            try:
                with urlopen(request, timeout=20) as response:
                    if response.status < 200 or response.status >= 400:
                        raise RuntimeError(f"HTTP {response.status}")
                    print(f"ok {response.status} {url}")
                    break
            except (HTTPError, URLError, TimeoutError, RuntimeError) as error:
                if attempt < 2:
                    time.sleep(10)
                    continue
                failures.append(f"{url}: {error}")
    if failures:
        print("public link check failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
