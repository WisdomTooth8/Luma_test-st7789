#!/usr/bin/env python3
# Minimal ST7789 test (works with your sweep result)
# Wiring (BCM GPIO numbers):
# SCLK = GPIO11 (pin 23), MOSI = GPIO10 (pin 19), CS = CE0 (pin 24, not wired on your board),
# DC = GPIO24 (pin 18), RST = GPIO25 (pin 22), VCC = 3V3 (pin 17), GND = GND (pin 20), BLK = 3V3 (pin 1)

from luma.core.interface.serial import spi
from luma.lcd.device import st7789
from PIL import Image, ImageDraw, ImageFont
import time

# ---- fixed, working parameters from your sweep ----
BUS_SPEED = 24_000_000     # 24 MHz
ROTATION  = 0              # 0 = no rotation
X_OFF     = 0
Y_OFF     = 0
BGR_MODE  = False          # your panel works with RGB (not BGR)

# GPIOs
GPIO_DC  = 24              # D/C
GPIO_RST = 25              # RESET

# Create SPI & device
serial = spi(port=0, device=0, gpio_DC=GPIO_DC, gpio_RST=GPIO_RST, bus_speed_hz=BUS_SPEED)
display = st7789(serial,
                 width=240, height=240,
                 rotation=ROTATION,
                 x_offset=X_OFF, y_offset=Y_OFF,
                 bgr=BGR_MODE)

# Simple demo: solid colors, then text
try:
    # cycle a few colors so you can see it clearly
    for color in [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255), (0, 0, 0)]:
        display.clear(color)
        time.sleep(0.8)

    # draw some text
    img = Image.new("RGB", (display.width, display.height), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 22)
    except:
        font = ImageFont.load_default()
    draw.text((10, 10),  "ST7789 OK", fill=(0, 255, 0), font=font)
    draw.text((10, 40),  f"{BUS_SPEED//1_000_000} MHz", fill=(0, 200, 255), font=font)
    draw.text((10, 70),  f"rot={ROTATION}  x={X_OFF}  y={Y_OFF}", fill=(255, 255, 0), font=font)
    display.display(img)

    # keep it on until you Ctrl+C
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    pass
