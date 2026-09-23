# NowNest dark-mode contrast root cause

Date: 2026-09-23
Tracker: edoworks/factory#57

## Defect

The numbered honey circles inherited the dark appearance `ink` token, producing
light text on a light honey background at 1.69:1 contrast.

## Why chain

1. The foreground changed to light text because `.feature-number` used the
   appearance-dependent `ink` token.
2. Honey remains a light action color in both appearances, so its foreground
   cannot follow the general text token.
3. The initial token map did not define a semantic foreground for honey.
4. Screenshot review showed the hierarchy but did not quantify this small text
   pairing.
5. The website had no mechanical contrast validator for light and dark token
   pairs.

## Corrections

- Immediate: add an appearance-stable `on-honey` token and use it for numbered
  honey circles.
- Root cause: distinguish foreground tokens by semantic background rather than
  assuming the general text token is valid on every accent.
- Recurrence guard: `scripts/check_nownest_contrast.py` measures required light
  and dark pairings; its negative unit test proves the original failure is
  rejected in CI.
