'''
 Sverre Coucheron (sverre.coucheron@gmail.com),
 Martin Stensen (martin.stensen92@gmail.com) and
 Vebjørn Haugland (vha044@post.uit.no)

 Developed spring 2017 for INF-3910-2
'''

# boot.py -- run on boot-up
import os
from machine import UART
from machine import SD
import time
uart = UART(0, 115200)
os.dupterm(uart)

#Initialize sd-card
print("********* Initializing the SD-card *********")
sd = SD()
time.sleep(3)
os.mount(sd, '/sd')
print("********* SD-card is initialized *********")
