# Session 1 consistency review (no hardware): 2026-11-08

- **Task:** KUNAA-7. **Reviewer:** curriculum-builder. **Branch:** `curriculum-builder/session01-review`, based on `main` @ `f469a49`.
- **Scope:** `lessons/01-traffic-light/` `index.html`, `worksheet.md`, `teacher-guide.md`, `main.py`. These are findings only: no lesson file was edited. kids-iot-academy applies any it accepts.
- **Method:** I read all four files side by side. I compared every pin, hole, colour, timing and step order, checked the rules in `AGENT.md` and `team/HOUSE-RULES.md`, and ran the five gates (`gates-5-consistency-review-2026-11-08.txt`).
- **Not done:** no hardware (the VM has no ESP32), no browser render and no print render. Nothing here says the session is ready or tested.

## What already agrees (no change needed)

| Item | page `index.html` | `main.py` | worksheet | teacher guide |
|---|---|---|---|---|
| Pins red/yellow/green | D25/D26/D27 (`CH`, l.621–623; `CODE`, l.1432–1434) | `Pin(25/26/27)` l.5–7 | §2 l.25–27 | §4 l.50–52 |
| Holes | pin→b7/b15/b23, resistor d→g, long leg i7/i15/i23, short leg i8/i16/i24, black j8/j16/j24 → − rail (Why cards l.1654–1729) | n/a | §2 table | §4 table, §5 checks |
| GND | the GND pin next to D13, on the same side as D25–D27 (`NEAR_PINS` l.753, Why l.1729) | n/a | l.28 | l.53 |
| Order and timing | red 5 → green 5 (slider 2–10) → yellow 2, so 12 s (`PHASES` l.1401, cycle bar l.530–534, step 1 l.1576) | l.9–27, 5/5/2 | §1 l.10 | §1 l.19 |
| Arithmetic | 5 + g + 2 (l.2102) | n/a | 60 ÷ 12 = 5 cycles; with 8 s green, 15 s | §7 Q7 |
| Quiz ↔ Explain | resistor, short leg, GND (l.2106–2121) | n/a | §4 Q1–3 (+ Pin(25) Q4) | §7 Q1–3 |
| Pin rules | no D34/D35/VP/VN outputs; no new parts on D2/D5/D12/D15/TX0/RX0; D25/26/27 wiring kept | gate d PASS | | |

`main.py` matches the program on the page line by line (gate c). Its only extra line is the comment on l.20, which F1 is about.

## Findings

Severity: **must-fix** = a learner or teacher will be misled, or two files disagree; **should-fix** = harder than it needs to be for a 10-year-old without a screen; **nice** = polish.

I found no must-fix *disagreement* on pins, holes, colours, timings or order. Two of the must-fix items are screen-only instructions that don't fit the no-screen classroom.

### F1. must-fix: `main.py` comment uses page-only jargon, and the guide says "identical"
- `lessons/01-traffic-light/main.py:20` and `teacher-guide.md:122` (the same line in §8).
- The comment `# GREEN_S on the page: 5 seconds is the page's default green time (its slider goes from 2 to 10)` names a placeholder and a slider that a learner holding paper never sees. `teacher-guide.md:100` then says the listing is "identical to the lesson page". It isn't: the page shows `time.sleep(GREEN_S)` and has no comment.
- Proposed `main.py:20` (and the same line in guide §8):
  ```python
      # Green time in seconds. Change the 5 to make green longer or shorter (2 to 10).
  ```
  Gate c allows extra whole-line comments in `main.py`, so this change keeps 5/5.
- Proposed `teacher-guide.md:100` heading:
  `## 8. The program (for reference; the same as the lesson page with green set to 5 s, plus one comment)`

### F2. must-fix: the worksheet's "Make it yours" assumes the kid has the lesson screen
- `worksheet.md:52`: "In the lesson you can change the green time (2 to 10 s)." Kids have no screen (`worksheet.md:6` says "No screen or internet needed").
- Proposed:
  `**Make it yours:** The program keeps green on for 5 s. Your teacher can change that number to anything from 2 to 10. If green were **8 s**, how long would one full cycle be? ______ s   Which line of the program would change? ______________`
  (The second blank matches guide §7 Q7. If the one-page limit is tight, drop it.)

### F3. must-fix: "unplug only the GND wire" is ambiguous on paper
- `worksheet.md:43`, `worksheet.md:49` (Q3) and `teacher-guide.md:29` (25–30 row). The circuit has four black wires. The page demo (`index.html:1964`, `setLoopBroken`) removes only the long one from the − rail to the ESP32 GND pin. A grown-up could pull a short cathode wire instead, and then only one light goes dark.
- Proposed `worksheet.md:43`:
  `Ask your grown-up to pull out **only the long black wire that goes to the ESP32's GND pin** for a moment. What happened? ________________________`
- Proposed `teacher-guide.md:29`, change the text "Try the "unplug only the GND wire" demo" to:
  `Try the demo: pull out only the long black wire from the − rail to the GND pin (all lights go dark), then plug it back.`

### F4. should-fix: the "Predict" question about the first light is answered in the line above it
- `worksheet.md:10` tells the order (red, then green, then yellow). `worksheet.md:14` then asks "Which light comes on **first**?"
- Proposed `worksheet.md:14`, a real prediction about the loop:
  `| After **yellow**, which light comes on next? | |`

### F5. should-fix: the worksheet never says which − rail, or that the red + rail sits next to it
- `worksheet.md:23` and the column "Black wire to − rail". On the page's breadboard the red + rail lies between row j and the blue − rail (`index.html:614`: `POS_RAIL_Z = 1.95`, `NEG_RAIL_Z = 2.2`; row j is at 1.375). So each black wire from j must cross the + rail. The guide warns about this (`teacher-guide.md:69`); the kid's sheet doesn't.
- Proposed new sentence after `worksheet.md:30` ("Check: the long leg…"):
  `Black wires go into the rail with the **blue line and − sign**, on the j side. Not the red + rail next to it!`

### F6. should-fix: the worksheet doesn't say how to read a hole name or find a pin
- `worksheet.md:19–28`. A 10-year-old without the 3D page meets "b7" and "D25" here first. The guide explains both (`teacher-guide.md:46`, `teacher-guide.md:64`). The worksheet doesn't.
- Proposed new line just before the §2 table (`worksheet.md:23`):
  `**b7** means letter **b**, row **7** (the numbers along the breadboard). Find **D25** by reading the tiny label printed next to the pin; don't count pins.`
- Print note: the worksheet is 1 page with little room (KUN-4). F5 and F6 together add about 3 lines. If they don't fit, take the room from the water-pipe sentence (`worksheet.md:21`), which the guide already covers at 5–10 min (see F12).

### F7. should-fix: the build order on the worksheet differs from the page and the guide
- The page builds each light's pin wire, resistor and LED. Then it adds all three cathode wires together ("Cathodes to the ground rail", `index.html:1593`), then rail → GND (`index.html:1595`). The guide follows that order (`teacher-guide.md:27`: "red, then yellow, then green, then the ground wires"). The worksheet puts each black wire in that light's row (`worksheet.md:25–27`), so kids will tick it per light.
- Either order makes the same circuit. The fix is for the sheet to match the teacher. Proposed: move the "Black wire to − rail" column out of the table into its own row, just above the Ground row:
  `| Black wires | j8, j16, j24 → blue − rail (one short black wire each) | | | | | ☐ |`
  The Red/Yellow/Green rows then end at "LED short leg (−)".

### F8. should-fix: the guide's "Before class" says nothing visible happens, but the power light comes on
- `teacher-guide.md:16`: "with nothing wired up yet, nothing visible happens." `AGENT.md` describes the DevKit V1 with a red power LED, which a teacher will see light up. That could look like an error.
- Proposed: `3. Unplug and plug the board back in. With nothing wired up yet, only the board's own small power light comes on. That is fine.`
  (This is a description of the board in `AGENT.md`, not a hardware result. hardware-tester can confirm it on the real board.)

### F9. should-fix: 5-band resistors
- `teacher-guide.md:39` and `:66` give only the 4-band code (orange, orange, brown, gold). Many kits ship 1% resistors with 5 bands. A teacher who sees orange-orange-black-black-brown may think the part is wrong.
- Proposed note on `teacher-guide.md:39`: `colour bands orange, orange, brown (then gold); on 5-band resistors: orange, orange, black, black (then brown)`

### F10. should-fix: the guide's Session 1 recap assumes the Labs
- `teacher-guide.md:3` ("who have done Pin Detective and the two Circuit Labs") and `:25` ("Last time you lit one LED from D25"). Page step 1 (`index.html:1576`) assumes the same. The Board set Session 1 = `lessons/01` and said Lesson 00 and the Labs are outside the 10 sessions. A no-screen class that starts at Session 1 hasn't built that first LED.
- **Open question for the Director:** do classroom kids do the Labs (on a shared laptop) before Session 1? If not, proposed change to `teacher-guide.md:26` (5–10 min):
  `| 5–10 | Parts check, LED legs (long leg = anode +, flat edge = cathode −) and the breadboard: the 5 holes in a row are joined underneath, and the middle gap splits each row in two. Water-pipe picture: pin = pump, wire = pipe, resistor = narrow pipe, LED = one-way glowing water wheel. |`
  and change `:25` to `Recap: "Last time you lit one LED." (Skip this if the class has not done the Circuit Labs.)`

### F11. nice: the guide's "no light ever" fix tells the teacher to press EN when there's no need
- `teacher-guide.md:84`. `main.py` keeps looping. Once the ground path is fixed, the next phase lights by itself within 12 s. EN only adds a step.
- Proposed fix cell: `Check steps 6–7. Once the loop is complete the lights come back on their own within one cycle (12 s); pressing EN to restart is optional.`

### F12. nice: water-pipe sentence placement on the worksheet
- `worksheet.md:21` puts the analogy in the "Wire it" section, but kids use it in §4 Explain (Q1, Q3). Proposed: move it to just under the `## 4. Explain` heading, unchanged.

### F13. nice: parts list wire colours
- The page draws the D25/D26/D27 jumpers red, yellow and green (`index.html:621–623`, `wire:`). `teacher-guide.md:40` says only "one each for D25, D26, D27". Proposed: `one each for D25, D26, D27 (red, yellow, green if you have them, to match the lights); one black for GND`.

### F14. nice: wiring sentence in the "Try it on my real board" panel
- `index.html:2448`: "…and each short leg to GND." Proposed: `…and each short leg to the − rail, with one wire from the rail to GND.` This is a page edit, so kids-iot-academy should re-run the gates after it.

### F15. nice: the progress label placeholder
- `index.html:510`: `Step 1 of 14`, but there are 16 steps. JS overwrites it on load (`index.html:2183`), so it only shows if the script fails. Proposed: `Step 1 of 16`.

## Rules check
- Pin rules and the D25/D26/D27 wiring: followed in all four files (gate d PASS). None of the proposals changes a pin or a hole.
- One new idea and no new part (`AGENT.md`): yes. The new idea is a three-phase `while True:` loop, and the new parts are two more LED + resistor pairs of a part type learners already know.
- Recap, "Make it yours" and a quiz of 2–3 questions: all on the page. The worksheet has Explain questions in place of the quiz, and F2 fixes its "Make it yours".

## Open questions for the Director
1. F10: do classroom kids do Pin Detective and the Circuit Labs before Session 1?
2. F5/F6: if both don't fit the one-page worksheet, which content should give way?
