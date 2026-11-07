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
- **Push to GitHub.** `GH_TOKEN` is still empty after the Board bound it (length 0, re-checked 2026-11-07 ~18:00 UTC). Waiting for the Board to fix the secret. `gh` is not logged in, and no git credentials are set up.
  - All of today's commits are on the local `main` only. They are not on GitHub yet.
  - Needs the Board: give the token to the Director's runtime.
- **No ESP32 is connected to the Acer.** There is no `/dev/ttyUSB*` or `/dev/ttyACM*`, and `mpremote` is not installed. Session 1 can't reach HARDWARE PASS until a board and the circuit are on the bench.
- ~~I can't change agent permissions.~~ Resolved: the Board removed `canCreateAgents` from the new hires.

**Board decisions (2026-11-07, comment on KUN-3)**
1. GitHub token: yes, bound to the Director's runtime as `GH_TOKEN`.
   - Checked 2026-11-07: `GH_TOKEN length: 0` (still empty).
   - Per the Board, pushing is **stopped** until the Board fixes the secret.
   - When it's fixed, push with `git push https://x-access-token:${GH_TOKEN}@github.com/nkiliyumwami/iot-kids-course-agents.git main`. Never store the token in a file or in git config.
2. ESP32: the Board will connect a board with the Session 1 circuit tonight. hardware-tester keeps KUN-5 open with the blocker until then.
3. `canCreateAgents` removed from hardware-tester and curriculum-builder by the Board.
4. hardware-tester on Sonnet: approved.
5. Session 1 = `lessons/01-traffic-light` only. Lesson 00 and the labs are out of scope for now.
6. (18:00 UTC) The Board re-saved `GH_TOKEN`. From now on, every Director run starts with a self-check: token length, `git ls-remote` reachability and a `/dev/ttyUSB*`/`/dev/ttyACM*` board check, with the three results posted before any other work.

**Self-check log**
| When (UTC) | GH_TOKEN length | Repo reachable | Board present |
|---|---|---|---|
| 2026-11-07 18:00 | 0 (variable not set at all) | yes, `origin/main` = `43bf6ae` | no |

**Assumptions**
- Session N = `lessons/NN-*`. Session 1 = `lessons/01-traffic-light` (confirmed by the Board). Lesson 00 (Pin Detective) and the Circuit Labs come before the course and are not part of the 10 sessions.
- The charter overrides `AGENT.md` §"Each daily run" for this repo. In the agents fork, the Director may commit and push to `main`. Team members never commit to `main`: they work on their own branch in their own worktree (`/home/paperclip/work/wt/<agent>`), and the Director merges.
- Evidence lives in `evidence/sessionNN/`. To keep gate e strict, runs that write evidence pass `--allow 'evidence/*'` and leave the gate's default allowlist unchanged.
- hardware-tester runs on Sonnet: its work is routine and tokens are money. The charter doesn't name its model.
- The worksheet expects the teacher to load `main.py` before class (no screen for kids). I accepted that as the offline model.

## kids-iot-academy

_No run under the new instructions yet. First task: Session 1 A4 print check + REVIEW-REGISTER.md._

## hardware-tester

_Hired 2026-11-07. First task: flash Session 1 `main.py` on a real ESP32, or record that no board is connected as a blocker._

## curriculum-builder

_Hired 2026-11-07. No task yet. Planned first task once Session 1 reaches HARDWARE PASS: a consistency review of the Session 1 page, worksheet, guide and code._
