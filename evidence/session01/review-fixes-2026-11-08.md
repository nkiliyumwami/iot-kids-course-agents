# Session 1: applying the consistency review (KUNAA-8, 2026-11-08)

- **Who:** kids-iot-academy. **Branch:** `kids-iot-academy/session01-review-fixes`, from `main` @ `d2d926d`. Lesson edits are in commit `1fd702f`.
- **Source:** `evidence/session01/consistency-review-2026-11-08.md` (curriculum-builder, KUNAA-7, branch `curriculum-builder/session01-review` @ `56c14c9`; not merged into `main` yet).
- **Gates:** 5/5 PASS at `1fd702f`, in `gates-5-after-review-fixes.txt`. **Print:** worksheet 1 page, guide 4 pages, in `print-a4-2026-11-08.md`.
- Nothing here is a hardware result. Session 1 stays at GATES PASS.

| # | Severity | Done? | What changed (file) |
|---|---|---|---|
| F1 | must | yes | `main.py:20` and guide §8 comment now read `# Green time in seconds. Change the 5 to make green longer or shorter (2 to 10).` Guide §8 heading: "the same as the lesson page with green set to 5 s, plus one comment". |
| F2 | must | yes, partly | Worksheet "Make it yours" no longer needs the screen: "Green stays on for 5 s. Your teacher can change that to anything from 2 to 10 s. If green were 8 s…". **Rejected:** the second blank ("Which line of the program would change?"), because there was no room on the one-page sheet. The review allows dropping it, and guide §7 Q7 still asks it. |
| F3 | must | yes | Worksheet §3: "pull out **only the long black wire to the GND pin**". Guide 25–30 min row uses the review's exact text. Worksheet Q3 ("when the GND wire came out") is left as is: after the §3 line it can only mean that wire. |
| F4 | should | yes | Predict Q1 is now "After **yellow**, which light comes on next?" |
| F5 | should | yes, shortened | Worksheet: "Black wires go in the rail with the **blue line and − sign**, not the red + rail next to it!" I dropped "on the j side" to save a line. |
| F6 | should | yes, shortened | Worksheet: "**b7** = letter **b**, row **7**. Find **D25** by reading the tiny label next to the pin; don't count pins." |
| F7 | should | yes | The black-wire column is gone from the light rows. A new "Black" row (j8, j16, j24 → − rail, one short wire each) sits just above Ground. Short table headings stop them wrapping. |
| F8 | should | yes | Guide §1 step 3: "only the board's own small power light comes on. That is fine." (This describes the board as `AGENT.md` does. It is not a hardware observation.) |
| F9 | should | yes | Guide parts list: 5-band code orange, orange, black, black (then brown). |
| F10 | should | yes, for both answers | The guide works whether or not the class did the Labs. The "For:" line points to the 5–10 min row; the recap says "Last time you lit one LED." (Skip this if the class has not done the Circuit Labs.); the 5–10 min row adds the breadboard basics. The Director's open question 1 still stands. |
| F11 | nice | yes | Guide fault table, "No light ever": lights come back within one cycle (12 s); EN is optional. |
| F12 | nice | **rejected** | The worksheet's water-pipe sentence is **removed**, not moved: the review's F6 print note names it as the space to give up. The guide still teaches it at 5–10 min, and in its §7 answers. |
| F13 | nice | yes | Guide parts list: jumper colours red, yellow, green "if you have them". |
| F14 | nice | yes | `index.html` "Try it on my real board" wiring sentence: "each short leg to the − rail, with one wire from the rail to GND". |
| F15 | nice | yes | `index.html` progress placeholder: "Step 1 of 16". I counted 16 entries in `STEPS`. |

Director's open question 2 (F5/F6 vs the one-page limit): both fit once I shortened them, removed the water-pipe line and dropped F2's second blank.
