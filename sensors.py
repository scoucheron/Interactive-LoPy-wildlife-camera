import machine
import tsl2561
import mpu6050
import battery
import ujson
import bme280
import os
import time

class Sensors():
    def __init__(self):
        self.i2c = machine.I2C(0, machine.I2C.MASTER, baudrate=50000)

    ''' Measures the temperature and humidity '''
    def temperature_and_humidity(self):
        try:
            weather = bme280.BME280(i2c=self.i2c)
            data = weather.values
            return data[0], data[2]
        except:
            print("The temperature and humidity sensor is not connected")
            return False, False

    ''' Measures how much battery is left '''
    def battery_level(self):
        battery_percent = battery.measure()
        battery_percent = round(battery_percent, 2)
        return battery_percent

    ''' Measures the remaining space '''
    def remaining_space(self):

        storage_left = 100
        return storage_left

    ''' Measures the acceleration (if there is one) '''
    def acceleration(self):
        try:
            mpu = mpu6050.MPU(self.i2c)
            mpu.wake()
            acceleration_result = mpu.pitch()
            return acceleration_result

        except:
            print("Acceleration sensor not connected")
            return "Not connected"

    ''' Measures the light level in lumen '''
    def light_level(self):
        try:
            sensor = tsl2561.TSL2561(self.i2c)
            lumen = sensor.read()
            return lumen
        except:
            print("Light sensor not connected")
            return "Not connected"

    ''' Detects motion through a PIR-sensor '''
    def movement_detection(self):
        pir = Pin('GP4',mode=Pin.IN,pull=Pin.PULL_UP)
        pir.callback(Pin.IRQ_RISING, pirTriggered)
        return False

    def pirTriggered(pin):
        print("Pir triggered")
        global pir_triggered
        pir_triggered = 1

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
