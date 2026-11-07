# My First Traffic Light (ESP32)
from machine import Pin
import time

red = Pin(25, Pin.OUT)
yellow = Pin(26, Pin.OUT)
green = Pin(27, Pin.OUT)

while True:
    # Red light: stop
    red.value(1)
    yellow.value(0)
    green.value(0)
    time.sleep(5)

    # Green light: go
    red.value(0)
    yellow.value(0)
    green.value(1)
    # GREEN_S on the page: 5 seconds is the page's default green time (its slider goes from 2 to 10)
    time.sleep(5)

    # Yellow light: get ready to stop
    red.value(0)
    yellow.value(1)
    green.value(0)
    time.sleep(2)
