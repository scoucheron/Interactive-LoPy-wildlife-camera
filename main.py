from network import LoRa
import machine
import socket
import binascii
import time
import pycom
import tsl2561
import ujson

class WildCamera:
    def __init__(self):
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
        self.socket = socket.socket(socker.AF_LORA, socket.SOCK_RAW)


    ''' Measures the temperature and humidity '''
    def temperature_and_humidity(self):
        temp = 12
        hum = 20
        return temp, hum


    ''' Measures how much battery is left '''
    def battery(self):
        battery_level = 100
        return battery_level


    ''' Measures the remaining space '''
    def remaining_space(self):
        storage_left = 100
        return storage_left


    ''' Measures the acceleration (if there is one) '''
    def acceleration(self):
        acceleration_result = 0

        if acceleration_result > 3:
            return True
        else:
            return False


    ''' Measures the light level in lumen '''
    def light_level(self):
        i2c = machine.I2C(0, machine.I2C.MASTER, baudrate=10000)
        sensor = tsl2561.TSL2561(i2c)

        if lumen < 1:
            return False
        else:
            return sensor


    ''' Detects motion through a PIR-sensor '''
    def movement_detection(self):
        movement = 200

        if movement < 300:
            return True
        else:
            return False


    def take_picture(self):
        picture = "0014192.jpg"
        return picture


    ''' Calls on all the sensors and saves the data in JSON on the SD-card '''
    def save_data_json(self,day):
        temp_hum = temperature_and_humidity()
        pic = take_picture()

        day['date'] = ({ 'temp': temp_hum[0],
                         'hum': temp_hum[1],
                         'pic': pic })

        with open ('data.txt', 'a') as outfile:
            ujson.dumps(day, outfile, indent=2)


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
    def main(self):

        # set the LoRaWAN data rate
        self.socket.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

        # make the socket non-blocking
        self.socket.setblocking(False)

        print("Æ E I MAIN")
        #while True:
            #movement = movement_detection()
            #if movement:
            #    save_data_json(day)

            #battery_level = battery()
            #space_left = remaining_space()
            #acceleration_result = acceleration()
            #lumens = light_level()


wildcamera = WildCamera
print("LOL")
if __name__ == "__main__":
    WildCamera.main()
