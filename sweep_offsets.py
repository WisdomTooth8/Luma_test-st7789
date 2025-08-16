# save as sweep_offsets.py, then: python3 sweep_offsets.py
import time
from itertools import product
from PIL import Image, ImageDraw, ImageFont
import st7735

DC = 9    # BCM9  (physical pin 21)
BL = 18   # BCM18 (physical pin 12)

def show(rot, cs, bgr, ol, ot):
    disp = st7735.ST7735(
        port=0,
        cs=cs,                  # 0=CE0 (pin 24)  1=CE1 (pin 26)
        dc=DC,
        backlight=BL,
        rotation=rot,           # 90 or 270
        width=160, height=80,   # 0.96" panel
        offset_left=ol, offset_top=ot,
        bgr=bgr,
        spi_speed_hz=4000000
    )
    disp.begin()

    W, H = disp.width, disp.height
    img = Image.new("RGB", (W, H), (0,0,0))
    d = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    d.rectangle((0,0,W-1,H-1), outline=(0,255,0))
    d.line((W//2,0,W//2,H-1), fill=(255,0,0))
    d.line((0,H//2,W-1,H//2), fill=(255,0,0))
    label = f"rot={rot} cs={cs} bgr={bgr} OL={ol} OT={ot}"
    d.text((2,2), label, font=font, fill=(255,255,255))
    disp.display(img)
    return label

tests = list(product([90,270], [0,1], [True,False], [26,24], [1,0]))
print(f"Trying {len(tests)} configs…")
for t in tests:
    label = show(*t)
    print("Showing:", label)
    time.sleep(3)
