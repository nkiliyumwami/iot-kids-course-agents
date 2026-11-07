# Session 1 hardware test: BLOCKED (no board)

- Date: 2026-11-07 17:52 UTC
- Commit checked: 8ed2f7a (local main)
- Target: lessons/01-traffic-light/main.py
- Verdict: **BLOCKED. Nothing was observed on hardware.** Every expected behaviour (red 5 s, green 5 s, yellow 2 s, one LED at a time, wiring) is **NOT OBSERVED**.

## What I checked
```
$ ls /dev/ttyUSB* /dev/ttyACM*
ls: cannot access '/dev/ttyUSB*': No such file or directory
ls: cannot access '/dev/ttyACM*': No such file or directory
$ ls /dev/serial*
ls: cannot access '/dev/serial*': No such file or directory
$ mpremote connect list
bash: mpremote: command not found
$ python3 -m mpremote connect list
/usr/bin/python3: No module named mpremote
```
`lsusb` shows only hubs, Dell dock, keyboard, mouse, webcam, Bluetooth and a Logitech receiver. There is no CP210x, CH340 or Espressif device.
(mpremote is not installed. I did not install it, since there is no board to talk to.)

## Needed to unblock
A human connects an ESP32 by USB data cable to the Acer and builds or confirms the Session 1 circuit (D25/D26/D27 to red/yellow/green LEDs through 330 ohm). That human is named in the next evidence file. Then re-assign this task.
