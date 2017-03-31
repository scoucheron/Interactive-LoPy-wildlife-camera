import machine
import tsl2561
import ujson
import os

class Sensors():
    def __init__(self):
        self.i2c = machine.I2C(0, machine.I2C.MASTER, baudrate=50000)


    ''' Measures the temperature and humidity '''
    def temperature_and_humidity(self):
        temp = machine.rng()
        hum = machine.rng()
        return temp, hum

    ''' Measures how much battery is left '''
    def battery_level(self):

        battery_level = 100
        return battery_level

    ''' Measures the remaining space '''
    def remaining_space(self):
        storage_left = 100
        return storage_left

    ''' Measures the acceleration (if there is one) '''
    def acceleration(self):
        acceleration_result = 0

        if acceleration_result < 1:
            return acceleration_result
        else:
            return False

    ''' Measures the light level in lumen '''
    def light_level(self):
        try:
            sensor = tsl2561.TSL2561(self.i2c)
            lumen = sensor.read()
            if lumen < 0.75:
                return False
            else:
                return lumen

        except:
            print("Light sensor not connected")


    ''' Detects motion through a PIR-sensor '''
    def movement_detection(self):
        movement = False

        return False


    ''' Takes a picture and saves it on the SD-card '''
    def take_picture(self):
        picture = "0014192.jpg"
        return picture

    ''' Calls on all the sensors and saves the data in JSON on the SD-card '''
    def save_data_json(self,day):
        temp_hum = self.temperature_and_humidity()
        pic = self.take_picture()

        day['date'] = ({ 'temp': temp_hum[0],
                         'hum': temp_hum[1],
                         'pic': pic })

        with open ('data.txt', 'a') as outfile:
            outfile.write(ujson.dumps(day))
            outfile.write("\n")
