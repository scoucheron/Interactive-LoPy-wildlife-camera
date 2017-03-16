#from network import LoRa
#import socket
#import binascii
import datetime
import random
import json
#import pycom

''' Measures the temperature and humidity '''
def temperature_and_humidity():
    temp = random.randint(0, 1000)
    hum = random.randint(0, 1000)
    return temp, hum


''' Measures how much battery is left '''
def battery():
    battery_level = random.randint(0, 1000)
    return battery_level


''' Measures the remaining space '''
def remaining_space():
    storage_left = random.randint(0, 1000)
    return storage_left


''' Measures the acceleration (if there is one) '''
def acceleration():
    acceleration_result = random.randint(0, 1000)

    if acceleration_result < 3:
        return True
    else:
        return False


''' Measures the light level in lumen '''
def light_level():
    lumen = random.randint(0, 1000)

    if lumen < 3:
        return True
    else:
        return False


''' Detects motion through a PIR-sensor '''
def movement_detection():
    movement = random.randint(0, 1000)

    if movement < 300:
        return True
    else:
        return False


def take_picture():
    picture = "0014192.jpg"
    return picture


''' Calls on all the sensors and saves the data in JSON on the SD-card '''
def save_data_json(day):
    temp_hum = temperature_and_humidity()
    pic = take_picture()

    day['date'] = ({ 'temp': temp_hum[0],
                     'hum': temp_hum[1],
                     'pic': pic })

    with open ('data.txt', 'a') as outfile:
        json.dump(day, outfile, indent=2)

def main():
    day = {}
    day['date'] = []

    while True:
        movement = movement_detection()
        if movement:
            save_data_json(day)

        battery_level = battery()
        space_left = remaining_space()
        acceleration_result = acceleration()

        if(battery_level < 3):
            print('WE ARE OUT OF BATTERY')

        if(space_left < 3):
            print('WE ARE OUT OF STORAGE')

        if(acceleration_result):
            print("THE CAMERA HAS FALLEN DOWN. PLS SEND HELP")


if __name__ == "__main__":
    main()

























''' Joins the LoRaWAN and blinks a bit '''
def join_network():
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

    # create a LoRa socket
    pycom.rgbled(0x0000ff)
    time.sleep(0.1)
    pycom.rgbled(0x000000)
    time.sleep(0.1)
    pycom.rgbled(0x0000ff)
    time.sleep(0.1)
    pycom.rgbled(0x000000)

    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

    # set the LoRaWAN data rate
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

    # make the socket non-blocking
    s.setblocking(False)

    print ("After while, count is: ",  count)

''' Sends the relevnt data back to the user '''
def send_data():
    print("Create LoRaWAN socket")
    # create a raw LoRa socket
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setblocking(False)

    ''' Want to send this to the user if the leves are critical'''
    battery_level = battery()
    space_left = remaining_space()
    acceleration_result = acceleration()

    count = 0
    while True:
        print("Send data...",  count)
        data = "Hello from the LoPy: %s" % (count)
        count = count + 1
        # send some data
        s.send(data)
        pycom.rgbled(0x00ff00)
        time.sleep(0.1)
        pycom.rgbled(0x000000)
        time.sleep(0.1)
        pycom.rgbled(0x00ff00)
        time.sleep(0.1)
        pycom.rgbled(0x000000)
        print("Sending data done...")
        # get any data received...
        data = s.recv(64)
        print("Received Data:",  data)
        time.sleep(30)
