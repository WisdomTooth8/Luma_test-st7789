import time
from PIL import Image, ImageDraw, ImageFont
import st7735

disp = st7735.ST7735(
    port=0,
    cs=0,                  # CE0 (pin 24). If you used CE1 (pin 26), change to cs=1
    dc=9,                  # BCM9 (physical pin 21)
    backlight=18,          # BCM18 (physical pin 12). Omit if BL not wired
    rotation=90,           # landscape
    width=160, height=80,  # <-- required for the 0.96" panel
    offset_left=26,        # <-- required
    offset_top=1,          # <-- required
    bgr=True,              # this panel is BGR; remove if colours look fine
    spi_speed_hz=4000000
)

disp.begin()

W, H = disp.width, disp.height
img = Image.new("RGB", (W, H), (0, 0, 0))
d = ImageDraw.Draw(img)

# draw a green border and centered text
d.rectangle((0, 0, W-1, H-1), outline=(0, 255, 0))
font = ImageFont.load_default()
text = "Hello World"
bbox = d.textbbox((0, 0), text, font=font)   # Pillow >= 8
tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
d.text(((W-tw)//2, (H-th)//2), text, font=font, fill=(255, 255, 255))

disp.display(img)
time.sleep(8)
