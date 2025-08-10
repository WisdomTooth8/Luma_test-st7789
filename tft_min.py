from time import sleep
from PIL import Image
from luma.core.interface.serial import spi
from luma.lcd.device import st7789

serial = spi(port=0, device=0, gpio_DC=24, gpio_RST=25, bus_speed_hz=12000000)
dev = st7789(serial, width=240, height=240, rotate=0)

for rgb in ((255,0,0),(0,255,0),(0,0,255),(255,255,255),(0,0,0)):
    dev.display(Image.new("RGB",(240,240), rgb))
    sleep(1)
