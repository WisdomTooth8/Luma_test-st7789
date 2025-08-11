#!/usr/bin/env python3
import time
import board
import digitalio

# Your wiring on the Pi:
# DC -> GPIO24 (pin 18)
# RST -> GPIO25 (pin 22)
DC_PIN  = board.D24
RST_PIN = board.D25

dc  = digitalio.DigitalInOut(DC_PIN)
dc.direction  = digitalio.Direction.OUTPUT

rst = digitalio.DigitalInOut(RST_PIN)
rst.direction = digitalio.Direction.OUTPUT

print("Pulsing RESET 5 times…")
for i in range(5):
    rst.value = False   # hold reset low
    time.sleep(0.05)
    rst.value = True    # release reset
    time.sleep(0.25)

print("Toggling DC 20 times…")
for i in range(20):
    dc.value = (i % 2 == 0)
    time.sleep(0.1)

dc.deinit()
rst.deinit()
print("Done.")
