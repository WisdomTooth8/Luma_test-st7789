import time
from PIL import Image
from luma.core.interface.serial import spi
from luma.lcd.device import st7789

# Try a few SPI speeds that luma allows
SPEEDS = [24000000, 16000000]

# Common settings to sweep:
ROTATIONS = [0, 90]
V_OFFSETS = [0, 80]          # many 240x240 ST7789 panels need v_offset=80
BGR_FLAGS = [False, True]    # some panels are BGR, others RGB

def show_solid(dev, rgb, sec=0.6):
    img = Image.new("RGB", (dev.width, dev.height), rgb)
    dev.display(img)
    time.sleep(sec)

for hz in SPEEDS:
    try:
        serial = spi(
            port=0, device=0,
            gpio_DC=24, gpio_RST=25,
            bus_speed_hz=hz, transfer_size=4096
        )
    except Exception as e:
        print(f"[SPI {hz}] failed to init serial:", e)
        continue

    for rot in ROTATIONS:
        for vo in V_OFFSETS:
            for bgr in BGR_FLAGS:
                print(f"=== Trying speed={hz} rot={rot} v_offset={vo} bgr={bgr} ===")
                try:
                    dev = st7789(
                        serial,
                        width=240, height=240,
                        rotate=rot,
                        bgr=bgr,
                        h_offset=0, v_offset=vo
                    )
                    # flash a few colors so it’s obvious if it worked
                    for c in [(255,0,0),(0,255,0),(0,0,255),(255,255,255)]:
                        show_solid(dev, c, 0.5)
                    print(">>> SUCCESS with these params <<<")
                    input("Leave these on-screen. Press Enter to test next combo...")
                except Exception as e:
                    print("combo failed:", e)
                finally:
                    try:
                        dev.cleanup()
                    except Exception:
                        pass
