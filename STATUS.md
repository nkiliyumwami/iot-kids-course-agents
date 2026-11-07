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
- ~~Push to GitHub.~~ Resolved 2026-11-07 ~18:06 UTC. After the Board switched the Director to a runner that passes environment variables, `GH_TOKEN` length was 93. `main` is pushed (`43bf6ae..a6c159d`), and the token is not stored in any file or git config.
- **No ESP32 is connected to the Acer.** There is no `/dev/ttyUSB*` or `/dev/ttyACM*`, and `mpremote` is not installed. Session 1 can't reach HARDWARE PASS until a board and the circuit are on the bench.
- ~~I can't change agent permissions.~~ Resolved: the Board removed `canCreateAgents` from the new hires.

**Board decisions (2026-11-07, comment on KUN-3)**
1. GitHub token: yes, bound to the Director's runtime as `GH_TOKEN`.
   - Was empty (0) until ~18:06 UTC. It is now working (93), and pushing has resumed.
   - Push with `git push https://x-access-token:${GH_TOKEN}@github.com/nkiliyumwami/iot-kids-course-agents.git main`. Never store the token in a file or in git config.
2. ESP32: the Board will connect a board with the Session 1 circuit tonight. hardware-tester keeps KUN-5 open with the blocker until then.
3. `canCreateAgents` removed from hardware-tester and curriculum-builder by the Board.
4. hardware-tester on Sonnet: approved.
5. Session 1 = `lessons/01-traffic-light` only. Lesson 00 and the labs are out of scope for now.
7. (18:13 UTC) Runtime rule: `GH_TOKEN` only reaches an agent on **Runner = Legacy runner + Execution engine = Claude CLI**. The Board set this for kids-iot-academy, hardware-tester and curriculum-builder. Every new hire gets the same setup and runs the three-line self-check on its first run. Recorded in `team/HOUSE-RULES.md` § "Runtime setup and first-run self-check".
6. (18:00 UTC) The Board re-saved `GH_TOKEN`. From now on, every Director run starts with a self-check: token length, `git ls-remote` reachability and a `/dev/ttyUSB*`/`/dev/ttyACM*` board check, with the three results posted before any other work.

**Self-check log**
| When (UTC) | GH_TOKEN length | Repo reachable | Board present |
|---|---|---|---|
| 2026-11-07 18:00 | 0 (variable not set at all) | yes, `origin/main` = `43bf6ae` | no |
| 2026-11-07 18:02 (after runtime reset) | 0 (variable not set; no GH_TOKEN/GITHUB_TOKEN name in env) | yes, `origin/main` = `43bf6ae` | no |
| 2026-11-07 18:06 (new runner with env vars) | 93 | yes; pushed, `origin/main` = `a6c159d` | no |
| 2026-11-07 ~18:15 | 93 | yes, `origin/main` = `6e28eb9` | no |

**Assumptions**
- Session N = `lessons/NN-*`. Session 1 = `lessons/01-traffic-light` (confirmed by the Board). Lesson 00 (Pin Detective) and the Circuit Labs come before the course and are not part of the 10 sessions.
- The charter overrides `AGENT.md` §"Each daily run" for this repo. In the agents fork, the Director may commit and push to `main`. Team members never commit to `main`: they work on their own branch in their own worktree (`/home/paperclip/work/wt/<agent>`), and the Director merges.
- Evidence lives in `evidence/sessionNN/`. To keep gate e strict, runs that write evidence pass `--allow 'evidence/*'` and leave the gate's default allowlist unchanged.
- hardware-tester runs on Sonnet: its work is routine and tokens are money. The charter doesn't name its model.
- The worksheet expects the teacher to load `main.py` before class (no screen for kids). I accepted that as the offline model.

## kids-iot-academy

_Last run: 2026-11-07 (KUN-4). Branch `kids-iot-academy/session01-print`._

**Changed**
- Session 1 A4 print check. Headless Chrome 156, A4, 12 mm margins. Renderer: `evidence/session01/print-a4-render.py`.
  - The worksheet was 2 pages. I shortened the answer blanks and removed no content. It is now **1 page**.
  - The teacher guide is **4 pages**: §1–§7 on pages 1–3, and the §8 program listing alone on page 4.
  - Evidence: `evidence/session01/print-a4-2026-11-07.md` plus the two PDFs.
- Consistency spot-check of the page, worksheet, guide and `main.py`: holes, pins, timings and order all agree. Details are in the same evidence file.
- Created `REVIEW-REGISTER.md`. Session 1 is GATES PASS with gates and print evidence. Sessions 2–10 are DRAFT. READY is blank (Board only).
- Gates 5/5 PASS: `evidence/session01/gates-3-after-print-check.txt`.

**Blocked**
- Nothing on my side. Session 1 can't go past GATES PASS until hardware-tester has a board (see the Director's section).

**Assumptions / decisions for the Director**
- The worksheet's §4 answer blanks are now about 5 cm. That is tight for kids' handwriting. Should we give them more room by cutting something else?
- The guide is 4 pages, not 3. Exactly 3 pages would mean dropping §8, the copy of `main.py`. I left that call to the Director.
- The register columns follow KUN-4. The print evidence column notes the page counts.

## hardware-tester

- 2026-11-07: Session 1 hardware test **BLOCKED**. No /dev/ttyUSB* or /dev/ttyACM*, no mpremote, no Espressif USB device. Evidence: `evidence/session01/hardware-BLOCKED-2026-11-07.md`. Nothing observed, so no hardware verdict.
- Needs: a board plugged into the Acer plus a named human to build or confirm the wiring.

## curriculum-builder

_Hired 2026-11-07. No task yet. Planned first task once Session 1 reaches HARDWARE PASS: a consistency review of the Session 1 page, worksheet, guide and code._
