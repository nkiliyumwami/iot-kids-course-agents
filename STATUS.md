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

_Last run: 2026-11-08 (KUNAA-6, Board answers Q3–Q5)._

**Run 2026-11-08 (KUNAA-6, Board answers)**
- Q3 yes: the Board will copy `PHASE0-REPORT.md` from the Acer into the repo. Until it lands, `STATUS.md` + `evidence/session01/` are the record.
- Q4 hold: no Modeler/Inspector hire until Blender is reachable (Acer via SSH, or installed on the VM). Session 1 scene stays BLOCKED.
- Q5 yes: agents call the Paperclip API at `http://127.0.0.1:3100` (checked: `/api/health` → 200). Rule added to `team/HOUSE-RULES.md`; house rules now name the office VM, not the Acer.
- Open: S2 yes/no (start Session 2 DRAFT with kids-iot-academy while Session 1 waits on hardware).

**Run 2026-11-08 later (KUNAA-6, after KUNAA-7/8 done)**
- Reviewed and merged `curriculum-builder/session01-review` (KUNAA-7, `56c14c9`) and `kids-iot-academy/session01-review-fixes` (KUNAA-8, `14aaef8`). The lesson edits are text only. Wiring, pins and timings are unchanged.
- Director accepts the KUNAA-8 calls: F2 second blank dropped, F12 water-pipe line removed from the worksheet (still in the guide), F5/F6 shortened. Worksheet stays 1 page, guide 4.
- Gates on merged `main`: 5/5 PASS, unit tests 32 OK: `evidence/session01/gates-6-after-review-merge.txt`.
- VM note: the unit tests need `MPY_CROSS` set too (without it, 28 fail). Run gates before writing the gate file into the repo, or gate e flags the new file.
- Session 1 = GATES PASS (review applied). Next: HARDWARE PASS (blocked on the Acer lab link), then scene (blocked on Blender), then kid-tester.

**Run 2026-11-08 (KUNAA-6, office move)**
- The team now runs on `kundakode-office-vm` (Azure). Checkout is clean on `main` at `f469a49` and `GH_TOKEN` length is 93. The VM has no ESP32, mpremote, Blender or camera.
- Restored the shared `mpy-cross` 1.29.0 at `/home/paperclip/work/.tools/py`. Session 1 gates are 5/5 on the VM.
- Session 1 hardware is **BLOCKED until the Board opens the SSH link to the Acer lab**. hardware-tester (KUNAA-5) gets no board task until then.
- Plan change: the Session 1 consistency review now runs before HARDWARE PASS. KUNAA-7 is assigned to curriculum-builder; KUNAA-8 is assigned to kids-iot-academy and is blocked by KUNAA-7.
- The Board confirmed that all agents are active and wake when given a task, so none need to be resumed.
- `PHASE0-REPORT.md` was never in git and exists only on the Acer.
- Board questions (3)–(5) answered later the same day: yes / hold / yes (see run above).

**Run 2026-11-07 ~18:15 UTC (KUN-3 follow-up)**
- Added the Board's runtime rule (Legacy runner + Claude CLI; first-run self-check) to `team/HOUSE-RULES.md` (`757e89f`).
- Reviewed and merged `kids-iot-academy/session01-print` (KUN-4) and `hardware-tester/session01-2026-11-07` (KUN-5 blocker evidence). Gates on merged `main`: 5/5 PASS, `evidence/session01/gates-4-after-merge-kun4-kun5.txt`.
- Director calls on KUN-4 trade-offs:
  - Teacher guide stays 4 pages. §8 (the program listing) is useful offline, when the teacher has no screen.
  - Worksheet stays 1 page with ~5 cm answer blanks for now. kid-tester (Day 2–3) will judge whether a 10-year-old can write in them; we change it then if needed.
- Next: Day 2–3 hire Modeler and Inspector with the Board's runtime setup; curriculum-builder starts after HARDWARE PASS.

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
| 2026-11-08 01:2x (Azure VM) | 93 | yes, `origin/main` = `f469a49` | no (VM has no USB board) |

**Assumptions**
- Session N = `lessons/NN-*`. Session 1 = `lessons/01-traffic-light` (confirmed by the Board). Lesson 00 (Pin Detective) and the Circuit Labs come before the course and are not part of the 10 sessions.
- The charter overrides `AGENT.md` §"Each daily run" for this repo. In the agents fork, the Director may commit and push to `main`. Team members never commit to `main`: they work on their own branch in their own worktree (`/home/paperclip/work/wt/<agent>`), and the Director merges.
- Evidence lives in `evidence/sessionNN/`. To keep gate e strict, runs that write evidence pass `--allow 'evidence/*'` and leave the gate's default allowlist unchanged.
- hardware-tester runs on Sonnet: its work is routine and tokens are money. The charter doesn't name its model.
- The worksheet expects the teacher to load `main.py` before class (no screen for kids). I accepted that as the offline model.

## kids-iot-academy

_Last run: 2026-11-08 (KUNAA-8), first run on the Azure VM. Branch `kids-iot-academy/session01-review-fixes`._

**VM first-run self-check (2026-11-08, at the start of this run)**
- `GH_TOKEN` length: 93. The token is set (value not recorded).
- `git ls-remote …/iot-kids-course-agents.git main` → `d2d926d…  refs/heads/main`. The remote is reachable.
- `ls /dev/ttyUSB* /dev/ttyACM*` → no such file. There is no board on this VM, as expected.
- The Paperclip API redirects to Cloudflare at `office.aikigali.com` but answers on `http://127.0.0.1:3100`.

**Changed**
- Applied curriculum-builder's Session 1 review (KUNAA-7): 13 findings in full, F2/F5/F6 shortened, F12 rejected (water-pipe line removed instead of moved, to keep 1 page). The list with one line per finding is in `evidence/session01/review-fixes-2026-11-08.md`.
  - Files: `worksheet.md`, `teacher-guide.md`, `main.py` (comment line 20 only), `index.html` (F14 wiring sentence, F15 "Step 1 of 16").
- Print check redone on the VM with Playwright Chromium (Chrome isn't installed). Worksheet **1** page, guide **4** pages. Evidence: `evidence/session01/print-a4-2026-11-08.md` and its two PDFs. New renderer: `evidence/session01/print-a4-render-playwright.py` (same CSS as the Chrome one).
- Gates 5/5 PASS: `evidence/session01/gates-5-after-review-fixes.txt`.
- `REVIEW-REGISTER.md`: Session 1 is still GATES PASS, with the new gates and print evidence; hardware is BLOCKED, waiting for the lab link.

**Blocked**
- Session 1 hardware: no ESP32 on this VM. It needs the lab link (hardware-tester, via the Director).

**Assumptions / decisions for the Director**
- F10, open question 1 (do classroom kids do the Labs first?) is still open. I wrote the guide so it works either way.
- To keep the worksheet on 1 page, I removed its water-pipe line (the guide still teaches it) and dropped F2's second blank ("which line would change?"; guide §7 Q7 still asks it).
- Print tools were installed into `/home/paperclip/work/.tools/` without root: free downloads, no accounts. If the Board would rather install system Chrome and poppler, the old renderer works again.
- I worked from the review on curriculum-builder's branch (it isn't merged into `main` yet). My branch doesn't include their commits.

## hardware-tester

- 2026-11-07: Session 1 hardware test **BLOCKED**. No /dev/ttyUSB* or /dev/ttyACM*, no mpremote, no Espressif USB device. Evidence: `evidence/session01/hardware-BLOCKED-2026-11-07.md`. Nothing observed, so no hardware verdict.
- Needs: a board plugged into the Acer plus a named human to build or confirm the wiring.

## curriculum-builder

_Last run: 2026-11-08 (KUNAA-7). Branch `curriculum-builder/session01-review`._

**Changed**
- Session 1 consistency review of the page, worksheet, teacher guide and `main.py` (no hardware, findings only, no lesson file edited): `evidence/session01/consistency-review-2026-11-08.md`.
  - Pins, holes, colours, timings (5/5/2 s, 12 s cycle) and the light order agree across all four files, and the pin rules are followed.
  - 15 findings: 3 must-fix (a `main.py` comment that only makes sense on the page; a screen-only "Make it yours" on the worksheet; an ambiguous "unplug the GND wire"), 7 should-fix and 5 nice. Each has file:line and the exact proposed text.
- Gates 5/5 PASS on this branch: `evidence/session01/gates-5-consistency-review-2026-11-08.txt`.

**Blocked**
- Nothing. No hardware or render checks were done (the VM has no ESP32), and none are claimed.

**Assumptions / open questions for the Director**
- F10: do classroom kids do Pin Detective and the Circuit Labs before Session 1? The guide and the page assume they do.
- F5/F6 add about 3 lines to the one-page worksheet. If they don't fit, which content gives way?
