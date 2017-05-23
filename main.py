from network import LoRa
import machine
import socket
import binascii
import time
import pycom
import sensors

'''
The PIR-sensor tells the controller when there is movement, then does the rest
- "Check" for movement
    * Call on function which should:
        -> Take picture
        -> Measure temperature and humidity
        -> Save as json and jpeg on SD-card
'''
def main():
    #Initialize the time
    #rtc = machine.RTC()
    #rtc.init((2014, 5, 1, 4, 13, 0, 0, 0))
    #sck = connect_to_lora()
    sensor = sensors.Sensors()

    day = {}

    # Every 24 hours, do a check on battery, light, acceleration and how much storage is left
    #while(True):
    #   check_status(sensor, sck)
    #    time.sleep(60)

    #sensor.take_picture()

    #movement = sensor.movement_detection()
    #if movement:
    sensor.save_data_json(day)

'''
    Checks the status of the light level, battery,
    direction of the camera and how much storage is
    left and passes it on so it can be sent

'''
def check_status(sensor, sck):
    #Check the light level, if it is too low then send a msg
    lumens = sensor.light_level()

    #Check the battery level, if it is too low then send a msg
    battery = sensor.battery_level()

    #Checks the acceleration, if it is too low then send a msg
    accel = sensor.acceleration()

    #Checks the remaining space, if it is too low then send a msg
    storage = sensor.remaining_space()

    #Create an array contatining all wanted values
    data_array = [lumens, battery, accel, storage]

    send_data(data_array, sck)

'''
Connects to the LoRaWAN.
Returns a socket
'''
def connect_to_lora():
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
        time.sleep(2.5)
        print("Not yet joined count is:" ,  count)
        count = count + 1

    #The socket which is to be used by everyone
    sck = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

    # set the LoRaWAN data rate
    sck.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

    # make the socket non-blocking
    sck.setblocking(False)

    # create a raw LoRa socket
    sck = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    sck.setblocking(False)
    return sck

'''
Sends data over the LoRaWAN
'''
def send_data(data_array, sck):

    #Incase we are disconnected from the lora network for some weird reason
    if not lora.has_joined():
        sck = connect_to_lora()

    sck.send(' '.join(str(x) for x in data_array))


if __name__ == '__main__':
    main()
