#!/usr/bin/env python3
"""Measure required NowNest web token pairings against WCAG thresholds."""

from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
CSS_PATH = ROOT / "nownest/styles.css"

PAIRINGS = {
    "light": (
        ("ink/canvas", "ink", "canvas", 4.5),
        ("muted/canvas", "ink-muted", "canvas", 4.5),
        ("ginger/canvas", "ginger", "canvas", 4.5),
        ("on-honey/honey", "on-honey", "honey", 4.5),
        ("muted/sage-wash", "ink-muted", "sage-wash", 4.5),
        ("sage/sage-wash", "sage", "sage-wash", 3.0),
    ),
    "dark": (
        ("ink/canvas", "ink", "canvas", 4.5),
        ("muted/canvas", "ink-muted", "canvas", 4.5),
        ("ginger/canvas", "ginger", "canvas", 4.5),
        ("on-honey/honey", "on-honey", "honey", 4.5),
        ("muted/sage-wash", "ink-muted", "sage-wash", 4.5),
        ("sage/sage-wash", "sage", "sage-wash", 3.0),
    ),
}


def parse_tokens(block: str) -> dict[str, str]:
    return dict(re.findall(r"--([\w-]+):\s*(#[0-9a-fA-F]{6})\s*;", block))


def luminance(color: str) -> float:
    channels = [int(color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4 for value in channels]
    return sum(value * weight for value, weight in zip(linear, (0.2126, 0.7152, 0.0722)))


def contrast(foreground: str, background: str) -> float:
    high, low = sorted((luminance(foreground), luminance(background)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def measure_css_text(css: str) -> tuple[list[tuple[str, str, float, float]], list[str]]:
    light_match = re.search(r":root\s*\{([^}]*)\}", css, re.DOTALL)
    dark_match = re.search(r"@media\s*\(prefers-color-scheme:\s*dark\)\s*\{\s*:root\s*\{([^}]*)\}", css, re.DOTALL)
    if not light_match or not dark_match:
        return [], ["light or dark NowNest token block is missing"]

    light = parse_tokens(light_match.group(1))
    dark = {**light, **parse_tokens(dark_match.group(1))}
    measurements: list[tuple[str, str, float, float]] = []
    errors: list[str] = []
    for appearance, tokens in (("light", light), ("dark", dark)):
        for name, foreground, background, minimum in PAIRINGS[appearance]:
            if foreground not in tokens or background not in tokens:
                errors.append(f"{appearance} {name}: token missing")
                continue
            ratio = contrast(tokens[foreground], tokens[background])
            measurements.append((appearance, name, ratio, minimum))
            if ratio < minimum:
                errors.append(f"{appearance} {name}: {ratio:.2f}:1 is below {minimum:.1f}:1")
    return measurements, errors


def validate_css_text(css: str) -> list[str]:
    return measure_css_text(css)[1]


def main() -> int:
    measurements, errors = measure_css_text(CSS_PATH.read_text(encoding="utf-8"))
    if errors:
        print("NowNest contrast validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    for appearance, name, ratio, minimum in measurements:
        print(f"PASS {appearance} {name}: {ratio:.2f}:1 (minimum {minimum:.1f}:1)")
    print("NowNest contrast validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
