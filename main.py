from network import LoRa
import machine
import socket
import binascii
import time
import pycom
import sensors


pycom.heartbeat(False)
pycom.rgbled(0x000000)
#Initialize LoRa in LORAWAN mode
lora = LoRa(mode=LoRa.LORAWAN)

# create an OTAA authentication parameters
dev_eui = binascii.unhexlify("000000000000010b")
app_eui = binascii.unhexlify("0000000000000050")
app_key = binascii.unhexlify("5939673537414b332b33665352554b6d")

# join a network using OTAA (Over the Air Activation)
lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

# wait until the module has joined the network
count = 0
while not lora.has_joined():
    pycom.rgbled(0xff0000)
    time.sleep(2.5)
    pycom.rgbled(0x000000)
    print("Not yet joined count is:" ,  count)
    count = count + 1

#The socket which is to be used by everyone
sck = socket.socket(socker.AF_LORA, socket.SOCK_RAW)

''' TODO (Should do when finished):

The PIR-sensor tells the controller when there is movement, then does the rest
- "Check" for movement
    * Call on function which should:
        -> Take picture
        -> Measure temperature and humidity
        -> Save as json and jpeg on SD-card

#########################################################################
These checks should be done once a day

- Check battery_level
    * If there is less than 10%, send warning to user

- Check space left on SD card
    * If there is less than 10%, send WARNING to user

- Check if the acceleration or the direction the camera is off
    * If the acceleration is too hight, or the wrong direction, send WARNING

- Check the light level
    * If it is too low, send WARNING to user
'''

# set the LoRaWAN data rate
sck.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# make the socket non-blocking
sck.setblocking(False)

#while True:
    #movement = movement_detection()
    #if movement:
    #    save_data_json(day)

    #battery_level = battery()
    #space_left = remaining_space()
    #acceleration_result = acceleration()
    #lumens = light_level()
