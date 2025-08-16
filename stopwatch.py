# Stopwatch on ST7735 with "USB button" as a keyboard key trigger.
# Triggers on SPACE or Enter by default (works with foot pedals that type a key).

import sys, time, termios, tty, select, signal
from PIL import Image, ImageDraw, ImageFont
import st7735

# ---------- Display setup (your working wiring) ----------
disp = st7735.ST7735(
    port=0,
    cs=0,          # CE0 (physical pin 24)
    dc=9,          # BCM9 (physical pin 21)
    backlight=18,  # BCM18 (physical pin 12) - omit if you didn't wire BL
    rotation=90,
    spi_speed_hz=4_000_000,
)
disp.begin()
W, H = disp.width, disp.height

# ---------- Fonts ----------
def load_font(size):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", size)
    except Exception:
        return ImageFont.load_default()

FONT_BIG   = load_font(26)
FONT_SMALL = load_font(12)

# ---------- Helpers ----------
def fmt_time(seconds: float) -> str:
    m, s = divmod(seconds, 60)
    return f"{int(m):02d}:{s:06.3f}"  # MM:SS.mmm

def render(current_s: float, last_lap_s: float | None):
    img = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(img)

    d.text((2, 2), "STOPWATCH", font=FONT_SMALL, fill=(160,160,160))
    cur = fmt_time(current_s)
    tw, th = d.textbbox((0,0), cur, font=FONT_BIG)[2:]
    d.text(((W - tw)//2, (H - th)//2 - 6), cur, font=FONT_BIG, fill=(255,255,255))

    last_text = "--" if last_lap_s is None else fmt_time(last_lap_s)
    d.text((2, H-14), f"Last: {last_text}", font=FONT_SMALL, fill=(0,255,128))

    hint = "SPACE/Enter=Lap  q=Quit"
    hw, _ = d.textbbox((0,0), hint, font=FONT_SMALL)[2:]
    d.text((W - hw - 2, H-14), hint, font=FONT_SMALL, fill=(120,120,120))

    disp.display(img)

# ---------- Keyboard (USB HID) non-blocking input ----------
# Any USB button that types a key will be seen here.
TRIGGER_KEYS = {b' ', b'\n', b'\r'}  # SPACE or Enter
QUIT_KEYS    = {b'q', b'Q'}

class RawStdin:
    def __enter__(self):
        self.fd = sys.stdin.fileno()
        self.old = termios.tcgetattr(self.fd)
        tty.setcbreak(self.fd)  # raw-ish, returns keys immediately
        return self
    def __exit__(self, exc_type, exc, tb):
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old)

def read_key(timeout=0.0):
    if sys.stdin in select.select([sys.stdin], [], [], timeout)[0]:
        ch = sys.stdin.buffer.read(1)
        return ch
    return None

# ---------- Main loop ----------
running   = True
last_lap  = None
start     = time.monotonic()
last_draw = 0.0

def handle_sigint(signum, frame):
    global running
    running = False
signal.signal(signal.SIGINT, handle_sigint)

render(0.0, last_lap)

try:
    with RawStdin():
        while running:
            now = time.monotonic()
            elapsed = now - start

            # Check for USB "button" (keyboard) key
            ch = read_key(0.01)
            if ch:
                if ch in QUIT_KEYS:
                    break
                if ch in TRIGGER_KEYS:
                    last_lap = elapsed
                    start = time.monotonic()  # reset stopwatch
                    render(0.0, last_lap)
                    continue

            # Refresh ~10 fps
            if now - last_draw >= 0.1:
                render(elapsed, last_lap)
                last_draw = now
finally:
    # Clear screen on exit
    img = Image.new("RGB", (W, H), (0, 0, 0))
    disp.display(img)
