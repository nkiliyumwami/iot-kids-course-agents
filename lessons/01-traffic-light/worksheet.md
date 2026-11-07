# Lesson 1 worksheet: My First Traffic Light

Name: ____________________ Date: __________ **Grown-up who checked my circuit:** ____________________

> **Keep the USB cable unplugged while you wire.** Plug it in only after a grown-up has checked the circuit.
> Before class, your teacher puts `main.py` (from this lesson's folder) on the ESP32. No screen or internet needed.

## 1. Predict (before you build)

The program turns on **red for 5 s**, then **green for 5 s**, then **yellow for 2 s**, and repeats forever.

| Question | My guess |
|---|---|
| Which light comes on **first**? | |
| How many seconds is one full cycle (red + green + yellow)? | |
| How many full cycles happen in one minute? | |
| If one LED is put in **backwards**, what will that light do? | |

## 2. Wire it (tick each box when it is in)

Like water in pipes: the **pin** is a pump, **wires** are pipes, the **resistor** is a narrow pipe that slows the flow, the **LED** is a water wheel that glows and only turns one way.

| Light | ESP32 pin → hole | 330 Ω resistor (crosses the middle gap) | LED long leg (+) | LED short leg (−) | Black wire to − rail | ✔ |
|---|---|---|---|---|---|---|
| Red | D25 → b7 | d7 to g7 | i7 | i8 | j8 → − rail | ☐ |
| Yellow | D26 → b15 | d15 to g15 | i15 | i16 | j16 → − rail | ☐ |
| Green | D27 → b23 | d23 to g23 | i23 | i24 | j24 → − rail | ☐ |
| Ground | GND pin (next to D13) → blue − rail | | | | | ☐ |

Check: the long leg and the short leg are in **different** rows. Every LED has **its own** resistor.

## 3. Observe (plug in the USB cable and watch)

Count the seconds out loud ("one elephant, two elephants…") for each light. Do it twice.

| | Red | Green | Yellow | Whole cycle |
|---|---|---|---|---|
| Try 1 (seconds) | | | | |
| Try 2 (seconds) | | | | |

Order I saw (write R, G or Y): ___ → ___ → ___ → ___ → ___ → ___   Was my prediction right? ☐ yes ☐ no

Ask your grown-up to unplug **only** the GND wire for a moment. What happened? ______________________________

## 4. Explain (use your own words)

1. Why does each LED need a resistor? ______________________________________________________________
2. Why is the short leg in a **different row** from the long leg? _____________________________________
3. Why did the lights stop when the GND wire came out? ______________________________________________
4. The program says `red = Pin(25, Pin.OUT)`. What does the `25` mean? ________________________________

**Make it yours:** In the lesson you can change the green time (2 to 10 s). If green were **8 s**, how long would one full cycle be? ______ s
