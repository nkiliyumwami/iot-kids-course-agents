# Teacher guide: Lesson 2, Make It Yours: Light Patterns

**For:** learners aged 10–15 (or adult beginners) who have built the Lesson 1 traffic light.
**New idea:** give things names: variables (`RED_S = 5`), one function (`set_lights`) and `print()` to see what the program is doing.
**New part:** none. The circuit is exactly the Lesson 1 circuit. **Time:** about 40 minutes.
**Needs:** the kit, one shared laptop with Thonny (works offline once installed) and the printed worksheet. No phones.

> This is a low-voltage circuit (3.3 V from the ESP32, powered by USB). Keep the USB cable **unplugged while
> checking or changing wires**, and have an adult check every circuit before it is plugged in. The lesson's 3D
> animation is a learning picture, not a safety test.

## 1. Before class (10 minutes, once per board)

1. The board needs MicroPython already on it (as for Lesson 1).
2. Copy `lessons/02-patterns/main.py` onto each board as **`main.py`**, replacing the Lesson 1 program (in Thonny:
   open the file, *File → Save as… → MicroPython device*, name it `main.py`). Keep a copy on the laptop too.
3. Check the board: unplug, plug back in. Red should light within a second or two, then green, then yellow.
4. Use a **data** USB cable. Some cables only charge and cannot load programs or show messages.

The lights do **exactly the same as in Lesson 1** (red 5 s → green 5 s → yellow 2 s, a 12 s cycle). That is the point:
the program is easier to read and change, but it does the same job.

## 2. Timing (40 minutes)

| Minutes | What happens |
|---|---|
| 0–5 | Recap: "Last time you built a traffic light." Hand out the worksheet. Show the program in Thonny on the laptop (or read section 8 aloud). Learners do **1. Predict**. |
| 5–10 | **2. Check the circuit** with USB unplugged (section 4), then plug in. |
| 10–18 | Variables: `RED_S = 5` stores 5 in a box labelled `RED_S`. `=` means "store", not "equals". Learners count the seconds (**3. Observe**, first line). |
| 18–25 | The function: `def` teaches the ESP32 a new word; `set_lights(1, 0, 0)` fills in r, y, g. Learners answer the `set_lights` rows in **1. Predict**. |
| 25–30 | `print()`: connect the laptop, press Run in Thonny (section 5). Learners copy three Shell messages (**3. Observe**). |
| 30–38 | **4. Make it yours**: each group designs a pattern on paper; you or a learner types it in and runs it (section 6). |
| 38–40 | **5. Explain** and discussion questions (section 7). Put the class `main.py` back if anyone saved over it. |

## 3. Parts list (per board or pair of learners)

The Lesson 1 traffic light, still built: ESP32 DevKit V1 with MicroPython, breadboard, red, yellow and green LEDs,
three 330 Ω resistors, three jumper wires to D25, D26 and D27, three short black wires and one long black GND wire.
Plus: one USB **data** cable and one shared laptop with Thonny for the class (or one per group, if you have them).

## 4. Circuit check (USB unplugged; same as Lesson 1)

| Light | ESP32 pin → hole | 330 Ω resistor | Long leg (+) | Short leg (−) | Black wire |
|---|---|---|---|---|---|
| Red | D25 → b7 | d7 → g7 (across the gap) | i7 | i8 | j8 → − rail |
| Yellow | D26 → b15 | d15 → g15 | i15 | i16 | j16 → − rail |
| Green | D27 → b23 | d23 → g23 | i23 | i24 | j24 → − rail |
| Ground | GND pin next to D13 → blue − rail | | | | |

Read the pin labels; don't count pins. If a circuit was taken apart since Lesson 1, use the full 8-step check in the
Lesson 1 teacher guide (section 5). Nothing new is wired today, and no other ESP32 pin is used.

## 5. Seeing `print()` messages on the shared laptop

1. Plug the board into the laptop with the data cable. Open Thonny. Bottom right, choose *MicroPython (ESP32)* and the board's port.
2. Thonny stops the running program when it connects, so the lights may freeze. That is normal.
3. Open `main.py` (from the laptop copy or from the device) and press the green **Run** button (or F5).
4. The lights start again and the **Shell** under the code shows `Red: stop`, `Green: go`, `Yellow: get ready`, one
   message each time the light changes. Press the red **Stop** button to stop.
5. Unplug and plug back in: the board runs the `main.py` saved on it again, with no laptop needed.

`print()` never changes the lights. It only sends text down the USB cable. Without the laptop the messages go nowhere.

## 6. Make it yours: the three patterns from the lesson page

To try a pattern, change only the lines shown below in the laptop copy, press **Run**, and watch. Keep the top of the
program (`from machine…`, the three `Pin` lines and `def set_lights`) as it is. **Run** does not save anything on
the board; to keep a pattern after unplugging, save it on the device as `main.py`.

| Pattern | Variable lines | Lines inside `while True:` (each indented 4 spaces) |
|---|---|---|
| Classic (the class program) | `RED_S = 5`, `GREEN_S = 5`, `YELLOW_S = 2` | see section 8 |
| Warning flasher | `FLASH_S = 0.5` | `print("Flash on")`, `set_lights(0, 1, 0)`, `time.sleep(FLASH_S)`, then `print("Flash off")`, `set_lights(0, 0, 0)`, `time.sleep(FLASH_S)` |
| Light chase | `STEP_S = 1` | `print("Red")`, `set_lights(1, 0, 0)`, `time.sleep(STEP_S)`, then the same three lines for `Yellow` `(0, 1, 0)` and `Green` `(0, 0, 1)` |

When you replace the variable lines, also replace the loop lines, or Python stops with a NameError (for example
`RED_S` is used but no longer set). Challenges from the page: red for 8 s (change only `RED_S = 5` to `RED_S = 8`);
the flasher twice as fast (`FLASH_S = 0.25`); the chase in the order green, yellow, red (swap the numbers in the first
and last `set_lights`); then the learners' own pattern from worksheet section 4, each phase three lines:
`print`, `set_lights`, `time.sleep`.

## 7. Likely problems (and fixes)

| What you see | Most likely cause | Fix |
|---|---|---|
| `NameError: name 'red_s' isn't defined` | Spelling or capitals differ: `red_s` is not `RED_S` | Copy the name exactly as it is written at the top. |
| `NameError` for `set_lights` | The loop was typed above `def set_lights`, or `def` was deleted | Python reads top to bottom: `def` must come before `while True:`. |
| `IndentationError` | Lines inside `def` or `while True:` are not lined up | Use exactly 4 spaces before each line inside them. |
| `SyntaxError` | A missing comma or bracket, or a message without both quote marks | Compare with section 8: `set_lights(1, 0, 0)` and `print("Red: stop")`. |
| The wrong colour lights up | The three numbers are in the wrong order | The order is always red, yellow, green, as in `def set_lights(r, y, g)`. |
| Nothing appears in the Shell | Thonny is not connected, the wrong port is chosen, or a charge-only cable | Check the port (bottom right), press Stop then Run, try another cable. |
| After unplugging, the board does the old pattern | The new pattern was only Run, not saved | Save on the device as `main.py`, or leave the class program there on purpose. |
| No light at all, even with the class program | The circuit has changed since Lesson 1 | Do the check in section 4. |

## 8. The program (for reference; the same as the lesson page with its default times, plus one comment)

```python
# Light Patterns (ESP32)
from machine import Pin
import time

red = Pin(25, Pin.OUT)
yellow = Pin(26, Pin.OUT)
green = Pin(27, Pin.OUT)

# How long each light stays on (seconds)
RED_S = 5
GREEN_S = 5
YELLOW_S = 2

def set_lights(r, y, g):
    red.value(r)
    yellow.value(y)
    green.value(g)

# print() messages appear in the Shell in Thonny when the board is connected to the laptop.
while True:
    print("Red: stop")
    set_lights(1, 0, 0)
    time.sleep(RED_S)

    print("Green: go")
    set_lights(0, 0, 1)
    time.sleep(GREEN_S)

    print("Yellow: get ready")
    set_lights(0, 1, 0)
    time.sleep(YELLOW_S)
```

## 9. Discussion questions and worksheet answers

1. Why `time.sleep(RED_S)` and not `time.sleep(5)`? (The name says what the number means, and you change it in one place.)
2. Why does `set_lights` switch all three lights every time? (Nothing from before stays on; red and green are never on together.)
3. Why must `def` come before the loop? (Python reads top to bottom; otherwise it does not know the word yet.)
4. Where did the `print()` messages go? (Down the USB cable to the Shell in Thonny on the laptop.)
5. Lesson 1 needed three `value()` lines per phase. How many lines does a phase need now? (Lesson 1 needed four, three of them to switch lights. Now three, and only `set_lights` switches lights.)

Worksheet: 1. No, same lights and times; yellow; none, all off; 8 + 5 + 2 = 15 s. 3. 5, 5, 2 s, yes;
`Red: stop`, `Green: go`, `Yellow: get ready`.
