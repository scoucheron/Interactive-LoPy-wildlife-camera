# boot.py -- run on boot-up
import os
from machine import UART
from machine import SD
import time
uart = UART(0, 115200)
os.dupterm(uart)

#Initialize sd-card
sd = SD()
time.sleep(1)
os.mount(sd, '/sd')
