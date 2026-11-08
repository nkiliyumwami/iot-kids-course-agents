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
