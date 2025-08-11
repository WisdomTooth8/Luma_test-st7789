#!/usr/bin/env python3
import time, board, busio
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw
import adafruit_st7789 as st7789

# SPI0: SCLK=GPIO11, MOSI=GPIO10 (your wiring)
spi = busio.SPI(clock=board.SCLK, MOSI=board.MOSI)

# DC on GPIO24, no hardware reset, no CS (module ties CS internally)
dc = DigitalInOut(board.D24); dc.direction = Direction.OUT
rst = None
cs  = None

def show(dev, color, tag):
    img = Image.new("RGB", (dev.width, dev.height), color)
    d = ImageDraw.Draw(img)
    d.text((8, 8), tag, fill=(255,255,255) if color!=(255,255,255) else (0,0,0))
    dev.blit_buffer(img.tobytes(), 0, 0, dev.width, dev.height)

SPEEDS = [24000000, 16000000]
BGRS   = [False, True]
YOFFS  = [0, 80]   # many 240x240 boards need 80

for hz in SPEEDS:
    for bgr in BGRS:
        for yoff in YOFFS:
            try:
                print(f"Trying baud={hz}, bgr={bgr}, y_off={yoff}, rot=0")
                disp = st7789.ST7789(spi, cs=cs, dc=dc, rst=rst,
                                     width=240, height=240,
                                     rotation=0, baudrate=hz,
                                     x_offset=0, y_offset=yoff, bgr=bgr)
                show(disp, (255,0,0),  f"R bgr={bgr} y={yoff}"); time.sleep(0.8)
                show(disp, (0,255,0),  f"G bgr={bgr} y={yoff}"); time.sleep(0.6)
                show(disp, (0,0,255),  f"B bgr={bgr} y={yoff}"); time.sleep(0.6)
                print(">>> visible output with these params")
                input("Press Enter to try next combo…")
            except Exception as e:
                print("combo failed:", e)
print("Done.")
