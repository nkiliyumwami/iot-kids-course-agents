# Review evidence register

One row per session (Session N = `lessons/NN-*`). Every status links to the evidence file behind it. No evidence, no status.

- Ladder: DRAFT → GATES PASS → HARDWARE PASS → SCENE PASS → AWAITING BOARD → READY.
- Maintained by kids-iot-academy. Hardware evidence comes only from hardware-tester.
- **The READY column belongs to the Board. Nobody else writes in it.**

| Session | Folder | Status | Gates evidence | Print evidence | Hardware evidence | Scene evidence | Kid-test evidence | READY (Board only) |
|---|---|---|---|---|---|---|---|---|
| 1 | `lessons/01-traffic-light` | GATES PASS | [gates-2-after-hole-b7-fix.txt](evidence/session01/gates-2-after-hole-b7-fix.txt); [gates-3-after-print-check.txt](evidence/session01/gates-3-after-print-check.txt); [gates-5-after-review-fixes.txt](evidence/session01/gates-5-after-review-fixes.txt) (after the KUNAA-7 review fixes, [review-fixes-2026-11-08.md](evidence/session01/review-fixes-2026-11-08.md)) | [print-a4-2026-11-07.md](evidence/session01/print-a4-2026-11-07.md); [print-a4-2026-11-08.md](evidence/session01/print-a4-2026-11-08.md) (after the review fixes: worksheet 1 page, guide 4 pages) | BLOCKED: no ESP32 on the Acer or the Azure VM, waiting for the lab link ([hardware-BLOCKED-2026-11-07.md](evidence/session01/hardware-BLOCKED-2026-11-07.md), hardware-tester) | none | none | |
| 2 | `lessons/02-patterns` | GATES PASS | [gates-1-draft.txt](evidence/session02/gates-1-draft.txt) (first draft of `main.py`, worksheet and guide, KUNAA-9) | [print-a4-2026-11-08-draft.md](evidence/session02/print-a4-2026-11-08-draft.md) (worksheet 1 page, guide 4 pages) | NOT TESTED (no hardware-tester run yet) | none | none | |
| 3 | `lessons/03-pedestrian-button` | DRAFT | none | none | none | none | none | |
| 4 | `lessons/04-fair-crossing` | DRAFT | none | none | none | none | none | |
| 5 | `lessons/05-crossing-sound` | DRAFT | none | none | none | none | none | |
| 6 | `lessons/06-measuring-light` | DRAFT | none | none | none | none | none | |
| 7 | `lessons/07-night-mode` | DRAFT | none | none | none | none | none | |
| 8 | `lessons/08-hello-wifi` | DRAFT | none | none | none | none | none | |
| 9 | `lessons/09-status-page` | DRAFT | none | none | none | none | none | |
| 10 | `lessons/10-phone-control` | DRAFT | none | none | none | none | none | |

Sessions 3–10: the pages exist, but there is no `main.py`, worksheet or teacher guide yet. Session 2 has a first draft (KUNAA-9), not yet reviewed.
