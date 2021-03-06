'''
 Sverre Coucheron (sverre.coucheron@gmail.com),
 Martin Stensen (martin.stensen92@gmail.com) and
 Vebjørn Haugland (vha044@post.uit.no)

 Developed spring 2017 for INF-3910-2
'''
import machine
import tsl2561
import mpu6050
import battery
import ujson
import bme280
import os
import time
from LSY201 import LSY

class Sensors():
    def __init__(self):
        self.i2c = machine.I2C(0, machine.I2C.MASTER, baudrate=50000)
        self.storage_left = 100

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
        self.storage_left = self.storage_left -1
        return self.storage_left

    ''' Measures the acceleration (if there is one) '''
    def acceleration(self):
        try:
            mpu = mpu6050.MPU(self.i2c)
            mpu.wake()
            acceleration_resultY = mpu.pitchY()
            print (acceleration_resultY)
            acceleration_resultX = mpu.pitchX()
            print (acceleration_resultX)
            return acceleration_resultX, acceleration_resultY

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
    def movement_detection(self, sensor, day):
        curr_val = 0
        num_detections=0
        pir = machine.Pin('G4',mode=machine.Pin.IN,pull=machine.Pin.PULL_UP)
        print("Waiting for pir-sensor to initialize (60 sec)...")
        # time.sleep(60)
        while True:
            tmp = curr_val
            curr_val = pir.value()
            if curr_val != 0:
                if curr_val != tmp:
                    num_detections +=1
                    print ("Movement detected!" + "\t" + "Total number of detections: " +  str(num_detections))
                    # sensor.take_picture()
                    # sensor.save_data_json(day)
            else:
                if curr_val != tmp:
                    print ("No movement" + "\t" + "Total number of detections: " + str(num_detections) )


    ''' Takes a picture and saves it on the SD-card '''
    def take_picture(self):
        try:
            camera = JPEGCamera()
            picture = camera.simpleTakePhoto('image.jpg')
        except:
            print("Camera is not connected")
            return "Not connected"


    ''' Calls on all the sensors and saves the data in JSON on the SD-card '''
    def save_data_json(self,day):
        temp_hum = self.temperature_and_humidity()
        pic = self.take_picture()

        day['date'] = ({ 'temp': temp_hum[0],
                         'hum': temp_hum[1],
                         'pic': pic })

        with open ('/sd/data.txt', 'a') as outfile:
            outfile.write(ujson.dumps(day))
            outfile.write("\n")
