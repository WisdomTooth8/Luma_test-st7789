#!/usr/bin/env python3
import time
from luma.core.interface.serial import spi
from luma.lcd.device import st7789
from luma.core.render import canvas

# --- SPI + pins (your wiring) ---
# CE0 is used as the chip-select (board has no CS pin, that’s OK)
DC = 24
RST = 25

serial = spi(port=0, device=0, gpio_DC=DC, gpio_RST=RST, bus_speed_hz=24000000)

# --- Display object (240x240 ST7789) ---
# If you still see nothing, try changing rotate to 90 or bgr=True
device = st7789(serial, width=240, height=240, rotate=0, bgr=False, h_offset=0, v_offset=0)

# --- Draw solid red with text ---
with canvas(device) as draw:
    draw.rectangle(device.bounding_box, fill="red")
    draw.text((10, 10), "ST7789 OK", fill="white")
time.sleep(2)

# --- Cycle a few colors with labels ---
for name, label, txt in [
    ("red",    "RED",    "white"),
    ("green",  "GREEN",  "black"),
    ("blue",   "BLUE",   "white"),
    ("white",  "WHITE",  "black"),
    ("black",  "BLACK",  "white"),
]:
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, fill=name)
        draw.text((10, 10), label, fill=txt)
    time.sleep(1)
