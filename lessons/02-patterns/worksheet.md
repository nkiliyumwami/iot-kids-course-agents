# Lesson 2 worksheet: Make It Yours: Light Patterns

Name: __________________ Date: ________ **Grown-up who checked my circuit:** ______________

> **Same circuit as Lesson 1. Don't take it apart.** Keep the USB cable unplugged until a grown-up has checked it.
> Today only the code changes. Your teacher has put the new `main.py` on the ESP32. You share one laptop with Thonny on it.

## 1. Predict (look at the code in Thonny with your teacher first)

The top of the program says `RED_S = 5`, `GREEN_S = 5` and `YELLOW_S = 2`. A **variable** is a name that stores a value.
In `set_lights(r, y, g)` the numbers are red, yellow, green: 1 = on, 0 = off.

| Question | My guess &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; |
|---|---|
| Will the lights do anything different from Lesson 1? | |
| Which light does `set_lights(0, 1, 0)` turn on? | |
| And `set_lights(0, 0, 0)`? | |
| With `RED_S = 8`, how long is one full cycle? | |

## 2. Check the circuit (USB unplugged, tick each box)

| Light | ESP32 pin → hole | Resistor | Long leg (+) | Short leg (−) | Black wire | ✔ |
|---|---|---|---|---|---|---|
| Red | D25 → b7 | d7 to g7 | i7 | i8 | j8 → − rail | ☐ |
| Yellow | D26 → b15 | d15 to g15 | i15 | i16 | j16 → − rail | ☐ |
| Green | D27 → b23 | d23 to g23 | i23 | i24 | j24 → − rail | ☐ |

☐ One long black wire joins the **blue − rail** to the GND pin next to D13.

## 3. Observe (plug in, then use the shared laptop)

Count the seconds: red ____ s, green ____ s, yellow ____ s. Same as Lesson 1? ☐ yes ☐ no

In Thonny, press **Run**. Copy the first three messages from the **Shell**:

1. ______________________ 2. ______________________ 3. ______________________

## 4. Make it yours: design a pattern on paper, then type it in with your teacher

| Phase | Message for `print("...")` | `set_lights(_, _, _)` | Seconds |
|---|---|---|---|
| 1 | | ( ___ , ___ , ___ ) | |
| 2 | | ( ___ , ___ , ___ ) | |
| 3 | | ( ___ , ___ , ___ ) | |

## 5. Explain (use your own words)

1. Why write `time.sleep(RED_S)` and not `time.sleep(5)`? ________________________
2. Why must `def set_lights` come **before** `while True:`? ________________________
3. The ESP32 has no screen. Where did your `print()` messages go? ________________________
