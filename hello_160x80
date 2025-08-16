# hello_160x80.py
import time
from PIL import Image, ImageDraw, ImageFont
import st7735

# --- Wiring (Pi Zero 2W, physical pins) ---
# CS -> Pin 24 (CE0)     => cs=0
# DC -> Pin 21 (BCM9)    => dc=9
# BL -> Pin 12 (BCM18)   => backlight=18   (omit this arg if you didn't wire BL)
# SCK -> Pin 23 (BCM11), MOSI -> Pin 19 (BCM10), VCC -> 3V3 (Pin 17), GND -> Pin 20

disp = st7735.ST7735(
    port=0,
    cs=0,                 # CE0; if you actually wired CS to pin 26 (CE1) use cs=1
    dc=9,
    backlight=18,
    rotation=90,          # landscape
    width=160, height=80, # *** key for this 0.96" panel ***
    offset_left=26,       # *** key offsets for ST7735S 160x80 breakout ***
    offset_top=1,
    spi_speed_hz=4000000  # start safe; can raise later
)

disp.begin()

W, H = disp.width, disp.height
img = Image.new("RGB", (W, H), (0, 0, 0))
d = ImageDraw.Draw(img)

font = ImageFont.load_default()
text = "Hello World"

# Pillow (newer): use textbbox instead of textsize
bbox = d.textbbox((0, 0), text, font=font)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

d.rectangle((0, 0, W-1, H-1), outline=(0, 255, 0))
d.text(((W - tw)//2, (H - th)//2), text, font=font, fill=(255, 255, 255))

disp.display(img)
time.sleep(8)
