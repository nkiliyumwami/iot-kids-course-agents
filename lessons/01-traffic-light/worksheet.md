# Lesson 1 worksheet: My First Traffic Light

Name: __________________ Date: ________ **Grown-up who checked my circuit:** ______________

> **Keep the USB cable unplugged while you wire.** Plug it in only after a grown-up has checked the circuit.
> Your teacher puts `main.py` (from this lesson's folder) on the ESP32 before class. No screen or internet needed.

## 1. Predict (before you build)

The program turns on **red for 5 s**, then **green for 5 s**, then **yellow for 2 s**, and repeats forever.

| Question | My guess |
|---|---|
| After **yellow**, which light comes on next? | |
| How many seconds is one full cycle (red + green + yellow)? | |
| How many full cycles happen in one minute? | |
| If one LED is put in **backwards**, what will that light do? | |

## 2. Wire it (tick each box when it is in)

**b7** = letter **b**, row **7**. Find **D25** by reading the tiny label next to the pin; don't count pins.

| Light | ESP32 pin → hole | 330 Ω resistor (across the gap) | Long leg (+) | Short leg (−) | ✔ |
|---|---|---|---|---|---|
| Red | D25 → b7 | d7 to g7 | i7 | i8 | ☐ |
| Yellow | D26 → b15 | d15 to g15 | i15 | i16 | ☐ |
| Green | D27 → b23 | d23 to g23 | i23 | i24 | ☐ |
| Black | j8, j16, j24 → − rail | one short wire each | | | ☐ |
| Ground | GND by D13 → − rail | one long wire | | | ☐ |

Check: the long leg and the short leg are in **different** rows. Every LED has **its own** resistor.
Black wires go in the rail with the **blue line and − sign**, not the red + rail next to it!

## 3. Observe (plug in the USB cable and watch)

Count the seconds out loud ("one elephant, two elephants…") for each light. Do it twice.

| | Red | Green | Yellow | Whole cycle |
|---|---|---|---|---|
| Try 1 (seconds) | | | | |
| Try 2 (seconds) | | | | |

Order I saw (write R, G or Y): ___ → ___ → ___ → ___ → ___ → ___   Was my prediction right? ☐ yes ☐ no

Ask a grown-up to pull out **only the long black wire to the GND pin** for a moment. What happened? ________

## 4. Explain (use your own words)

1. Why does each LED need a resistor? ________________________
2. Why is the short leg in a **different row** from the long leg? ________________________
3. Why did the lights stop when the GND wire came out? ________________________
4. The program says `red = Pin(25, Pin.OUT)`. What does the `25` mean? ________________________

**Make it yours:** Green stays on for 5 s. Your teacher can change that to anything from 2 to 10 s. If green were **8 s**, how long would one full cycle be? ______ s
