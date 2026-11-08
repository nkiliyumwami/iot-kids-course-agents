# Phase 0 report: verification gates + Lesson 01 (local only)

Date: 2026-11-07 (overnight run). Repo: `/home/paperclip/work/iot-kids-course`, all branches cut from `main` @ `43bf6ae`.
Nothing was pushed. No `gh`, no GitHub, no sudo. `main` was not committed to and is checked out clean.
I cannot see a board: **no hardware result is claimed anywhere in this report.**

## Summary

| # | Task | Status | Branch | Commit |
|---|---|---|---|---|
| 1 | Gates `tools/verify_lesson.py` + tests | Done | `phase0/gates` | `072ed56` |
| 2 | `lessons/01-traffic-light/main.py` | Done, passes all 5 gates | `phase0/lesson01-main` | `1d09bda` |
| 3 | `lessons/01-traffic-light/worksheet.md` | Done (1 A4 page) | `phase0/lesson01-worksheet` | `a33f482` |
| 4 | `lessons/01-traffic-light/teacher-guide.md` | Done (3 A4 pages) | `phase0/lesson01-guide` | `978769b` |
| 5 | `tools/check.sh` on lesson 01 | Ran: no script errors, no sideways scroll | (no commit; run on `main`) | n/a |

Merged together in a throwaway clone (`/tmp/combo`, since deleted), the four branches give: all 5 gates PASS for
lesson 01, exit 0, and all 32 tests pass. Each branch has one commit on top of `main`.

Commit identity: there is no git user configured and I did not change any git config. Commits use
`-c user.name="Curriculum Builder (Phase 0 agent)" -c user.email=phase0-agent@localhost` and end with a
`Co-Authored-By: Claude` line. Rewrite the author on merge if you want your own name on them.

## Task 1: gates (`phase0/gates`, `072ed56`)

Files: `tools/verify_lesson.py`, `tools/tests/test_verify_lesson.py`.
Run: `python3 tools/verify_lesson.py lessons/01-traffic-light [more lessons] [--base main] [--allow GLOB]`.
Tests: `python3 -m unittest discover -s tools/tests -v` (32 tests, about 6 s, all pass).

What each check does:
- **a. extract.** Evaluates the page's own `window.__lessonProgram = () => …` expression (the exact text sent by
  "Try it on my real board") in Node. It pulls in only the top-level declarations that expression needs, in source
  order, so lesson 01 gets `CODE` with `GREEN_S` → `String(DEFAULT_GREEN)` = 5, and lessons 03–10 run `codeLines()`
  with `sim.cfg = Object.assign({}, DEFAULT_CFG)`. Browser objects get harmless stand-ins. If a stand-in ever leaks
  into the program text, or a name is missing, the check FAILs instead of guessing.
- **b. compile.** `mpy-cross` 1.29.0 on the page program and on `main.py` if present.
- **c. main.py.** Compares line by line, exactly (whitespace included). One relaxation: `main.py` may contain extra
  **whole-line comments**. This was needed so `main.py` can carry the requested "this is the page default" comment.
  Missing `main.py` = FAIL.
- **d. pins.** Parses the Python and finds every `Pin(...)`, following plain-number constants. Rules:
  - The pin must be a real DevKit V1 GPIO.
  - No output (`Pin.OUT`, `PWM`, `DAC`) on D34/D35/VP/VN.
  - No use at all of D2/D5/D12/D15/TX0/RX0. The one exemption is D2 in lesson 00, which is the on-board blue LED, not a new part.
  - D25/D26/D27 must be `Pin.OUT` named `red`/`yellow`/`green`, and `red`/`yellow`/`green` must be on those pins.
  - `ADC(...)` only on ADC1 pins.
  - A pin number that can't be worked out is a FAIL, and so is a program that doesn't parse.
- **e. files.** Collects committed, staged, unstaged and untracked changes since `merge-base(main, HEAD)`.
  - `.github/*`, `AGENT.md`, `CLAUDE.md` and `course.js` always FAIL.
  - Otherwise allowed: `lessons/<this lesson>/*`, `tools/verify_lesson.py`, `tools/tests/*`, plus any `--allow`.
  - `__pycache__/` is ignored.

Proof it fails on broken copies (automated, in a temporary git repo made from the real lesson 01 page):

| Broken copy | Gates that FAIL (asserted exactly) |
|---|---|
| Good version | none, exit 0 |
| Syntax error on page + main.py (`while True` without colon) | b, d |
| Syntax error only in main.py; bad indent only in main.py | b, c, d |
| main.py number changed / line missing / extra code line / green 7 s | c |
| main.py missing | c |
| red on D34 (input-only); red on D26 (swapped); green on D12 (start-up pin); yellow on GPIO24 (doesn't exist) | d |
| Wrong pin only in main.py | c, d |
| AGENT.md edited; `.github/x.yml` added; lesson 02 edited and committed; stray untracked file | e |
| Page has no `__lessonProgram` | a (and dependants) |

There are also unit tests for the pin rules (PWM on D35, ADC2 pin, serial pins, named constants, the lesson-0 D2
exemption) and a read-only test that all 11 real lessons extract, compile and pass the pin rules.

**Read-only run on lessons 00–10 (from `phase0/gates`, before task 2):**

| Lesson | a extract | b compile | c main.py | d pins | e files |
|---|---|---|---|---|---|
| 00–10 (all 11) | PASS | PASS | **FAIL: no main.py** | PASS | PASS |

- Every page program extracts, compiles with mpy-cross and follows the pin rules.
- Lesson 00 passes d only because of the documented D2 on-board-LED exemption.
- No lesson on `main` has a `main.py`, so c fails everywhere. That's expected, not a bug in the pages.
- Extracted programs spot-checked: lesson 01 = 26 lines with `time.sleep(5)` for green. In lesson 04, `while count < 80:` (4 s ÷ 0.05) and the 5 s crossing match `DEFAULT_CFG`.

Not checked by the gates:
- The 3D wiring drawn on the page. "D25/D26/D27 wiring kept" is checked in **code only**, not against the scene or the `wiring:` sentence.
- Whether the program behaves correctly. Compiling is not running.
- MicroPython API correctness beyond syntax. For example, a misspelt `Pin.OTU` would compile.
- Lessons whose program the code can only build in a non-default state, such as lesson 03's "no pull-up" variant. Only the default the board button sends is checked.
- Modules (`m-*`) and labs. They weren't asked for, and nothing was run on them.

Limitations and assumptions:
- Extraction relies on top-level declarations starting at column 0, which is true for every lesson today. A future page that breaks this pattern fails loudly at check a rather than passing wrongly.
- Requires `node`, `git` and `mpy-cross`. If `mpy-cross` is missing, check b FAILs; it is never skipped.
- **Assumption:** a missing `main.py` is a FAIL, not a skip. A gate that quietly skips is worse.
- **Assumption:** extra whole-line comments in `main.py` are allowed (see check c). Anything else must match exactly.
- **Assumption:** the D2 exemption is hard-coded for `00-meet-esp32` only.

## Task 2: Lesson 01 main.py (`phase0/lesson01-main`, `1d09bda`)

- Identical to the page program (default green 5 s). The only addition is one comment line above the green `time.sleep(5)`: `# GREEN_S on the page: 5 seconds is the page's default green time (its slider goes from 2 to 10)`.
- Gates on this branch: **a PASS, b PASS (page and main.py), c PASS (comment line 20 allowed), d PASS, e PASS. Exit 0.**
- Extra non-hardware evidence: I ran it under CPython with a fake `machine.Pin` and a fake `time.sleep`. The order was red 5 s → green 5 s → yellow 2 s, repeating, with exactly one light on in each phase.
- Not checked: a real ESP32. Real timing, real LEDs and real flashing are all unverified.

## Task 3: worksheet (`phase0/lesson01-worksheet`, `a33f482`)

- One page: Predict, Wire (tick-box wiring table), Observe (count seconds twice, write the order, the unplug-GND demo), Explain (4 questions), plus a "Make it yours" sum.
- Hole positions are taken from the page code: wire into b7/b15/b23, resistor d→g, LED legs in i7/i8, i15/i16 and i23/i24, black wires from j8/j16/j24, rail to the GND pin next to D13.
- Fits **one A4 page**. Checked by rendering the Markdown with python-markdown, printing to PDF with headless Chrome (A4, 12 mm margins) and looking at the image. A different Markdown renderer or larger fonts could spill onto a second page. Not checked: printing from GitHub's own renderer.
- Gates on this branch: a, b, d, e PASS. **c FAILs (no main.py) only because this branch is cut from `main` as instructed.** It passes once merged with `lesson01-main`.
- "No screen" assumes the teacher has already put `main.py` on the board; the sheet says so.

## Task 4: teacher guide (`phase0/lesson01-guide`, `978769b`)

- Sections: before class (load `main.py` with Thonny, offline), a 35-minute timing plan (matches `course.js`), parts list, wiring table, an 8-step wiring check per light, 5 likely faults with fixes (plus a note on dim LEDs and the wrong resistor), 7 discussion questions, and the full program.
- The guide's code block is byte-identical to `main.py` (checked with `diff`).
- About 3 A4 pages.
- Gates: same as task 3 (c FAILs only because `main.py` isn't on this branch).
- **Honest note:** the "5 most likely faults" are my judgement from how the circuit is built, not from classroom data. The guide says so.
- The split-rail warning is general advice about long breadboards. The lesson's rail use (rows 8 to 30) would be fine on a 400-hole board.

## Task 5: tools/check.sh on lesson 01

- Installed for my user only:
  - `playwright` through npm into a user prefix.
  - Chromium headless shell into the Playwright cache under `$HOME`.
  - `mpy-cross` and `markdown` with `pip install --user --break-system-packages`. The system Python is PEP 668 "externally managed". That flag only allows a `--user` install and changes no system files.
- **Two environment problems, worked around without editing `check.sh`:**
  1. `npm root -g` prints this runner's `$HOME` with its UUID-like part replaced by `***`, so `check.sh`'s `NODE_PATH` pointed at a path that doesn't exist and `require('playwright')` failed. Workaround: a symlink `/home/paperclip/.npm-global-phase0` → the user npm prefix, with `NPM_CONFIG_PREFIX` set to it.
  2. A second run into the same `OUT` folder fails: `cp -r` copies `.git` objects, which are read-only. Workaround: a fresh `OUT=/tmp/iotkids-shots-l01`. Possible fix for `check.sh` later, not done: exclude `.git` or clear `$OUT/site` first.
- Result for `tools/check.sh lessons/01-traffic-light "0,6,11,13,14,16"`:
  - **no errors** (no page errors, no console errors).
  - scrollWidth is 1400 at 1400 px and **400 at 400 px**, so no sideways scroll.
  - Screenshots are in `/tmp/iotkids-shots-l01/`. I looked at steps 6 and 14 (desktop) and 0 (400 px): labels readable, nothing clipped.
  - Step index 16 is past the last step (the page has 16 steps, 0–15), so that shot just repeats the end.
- Not checked: clicking through the quiz, every step, and the real-board panel (it needs a serial port; out of scope).

## Things noticed on the page (not changed)

- Lesson 01, step "Red: D25 → resistor → LED": the "Why?" card asks **"Why row 7? Why hole a?"**, but the code (`holeAt(ch.col, 'b')`) and AGENT.md put the jumper in **hole b7**. The answer text says any of a–e works, so it isn't wrong, but the question names the wrong hole. My worksheet and guide say b7, matching the code. It's a one-word page fix if you want it. I didn't make it because it wasn't asked for.
- ROADMAP.md was not updated (its log is normally edited with lesson changes). I left it alone so the gates stay strict; add a log line on merge if you want one.

## Honest quality assessment

- **Gates: good, with known limits.**
  - The extraction runs the page's real code rather than copying it by hand, which is the strongest part.
  - The tests show each gate failing for the right reason.
  - Weak points: Node-based extraction depends on the page's coding style (column-0 declarations), and the pin check only sees code, not the 3D wiring.
- **main.py: good.** It is mechanically the page program plus one comment, and verified by the gates and a simulated run. Not run on hardware.
- **Worksheet and guide: solid first drafts.** They're accurate to the page, but nobody has used them in a classroom. A teacher should read them once before use, especially the fault table and the 35-minute plan.
