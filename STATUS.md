# KundaKode team status

Each agent updates **only its own section** at the end of every run: what changed, what is blocked, what it assumed.
The Academy Director reads this file before every decision. Team rules: `team/HOUSE-RULES.md`.

## Sessions

| Session | Folder | Status | Evidence |
|---|---|---|---|
| 1 | `lessons/01-traffic-light` | GATES PASS | `evidence/session01/gates-2-after-hole-b7-fix.txt` |
| 2–10 | `lessons/02-…` to `lessons/10-…` | DRAFT (pages exist, no `main.py`, worksheet or guide yet) | gates read-only run in PHASE0-REPORT (c fails: no main.py) |

Status ladder: DRAFT → GATES PASS → HARDWARE PASS → SCENE PASS → AWAITING BOARD → READY (Board only).

---

## academy-director

_Last run: 2026-11-07 (KUN-3, Day 1)._

**Changed**
- Merged `phase0/gates`, `phase0/lesson01-main`, `phase0/lesson01-worksheet` and `phase0/lesson01-guide` into `main`, in that order and without conflicts.
  - Gates on Lesson 01: 5/5 PASS. Unit tests: 32 OK. Evidence: `evidence/session01/gates-1-after-phase0-merge.txt`.
- Lesson 01 page: the "Why?" card asked "Why hole a?", but the wire goes into b7. It now says "Why hole b7?" and the answer names b7.
  - Gates re-run: 5/5 PASS. Evidence: `evidence/session01/gates-2-after-hole-b7-fix.txt`.
- Installed `mpy-cross` 1.29.0 (the same version as Phase 0) into a shared folder, `/home/paperclip/work/.tools/py`, so every agent can run gate b.
  - Each agent runs with its own HOME, so a `pip --user` install is invisible to the others.
  - Every gate run must set `MPY_CROSS=/home/paperclip/work/.tools/py/mpy_cross/mpy-cross`.
- Added `team/HOUSE-RULES.md` with the rules every agent follows.
- Hired hardware-tester (Sonnet 5.5) and curriculum-builder (Opus 5.5). kids-iot-academy now reports to the Director and has new instructions.
  - All three run one at a time, with a 30-minute timeout, and wake only when assigned a task.

**Blocked**
- **Push to GitHub.** `GH_TOKEN` is empty in the Director's environment. `gh` is not logged in, and no git credentials are set up.
  - All of today's commits are on the local `main` only. They are not on GitHub yet.
  - Needs the Board: give the token to the Director's runtime.
- **No ESP32 is connected to the Acer.** There is no `/dev/ttyUSB*` or `/dev/ttyACM*`, and `mpremote` is not installed. Session 1 can't reach HARDWARE PASS until a board and the circuit are on the bench.
- I can't change agent permissions ("Only CEO can manage permissions"). The new hires still have `canCreateAgents: true`, and their instructions forbid using it.

**Assumptions**
- Session N = `lessons/NN-*`. Session 1 = `lessons/01-traffic-light`. Lesson 00 (Pin Detective) and the Circuit Labs come before the course and are not part of the 10 sessions.
- The charter overrides `AGENT.md` §"Each daily run" for this repo. In the agents fork, the Director may commit and push to `main`. Team members never commit to `main`: they work on their own branch in their own worktree (`/home/paperclip/work/wt/<agent>`), and the Director merges.
- Evidence lives in `evidence/sessionNN/`. To keep gate e strict, runs that write evidence pass `--allow 'evidence/*'` and leave the gate's default allowlist unchanged.
- hardware-tester runs on Sonnet: its work is routine and tokens are money. The charter doesn't name its model.
- The worksheet expects the teacher to load `main.py` before class (no screen for kids). I accepted that as the offline model.

## kids-iot-academy

_No run under the new instructions yet. First task: Session 1 A4 print check + REVIEW-REGISTER.md._

## hardware-tester

- 2026-11-07: Session 1 hardware test **BLOCKED**. No /dev/ttyUSB* or /dev/ttyACM*, no mpremote, no Espressif USB device. Evidence: `evidence/session01/hardware-BLOCKED-2026-11-07.md`. Nothing observed, so no hardware verdict.
- Needs: a board plugged into the Acer plus a named human to build or confirm the wiring.

## curriculum-builder

_Hired 2026-11-07. No task yet. Planned first task once Session 1 reaches HARDWARE PASS: a consistency review of the Session 1 page, worksheet, guide and code._
