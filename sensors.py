import machine
import tsl2561
import mpu6050
import ujson
import os
import time

pir_triggered=0


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
        numADCreadings = const(20)
        adc = machine.ADC(0)
        adcread = adc.channel(attn=1, pin='P16')
        samplesADC = [0.0]*numADCreadings; meanADC = 0.0
        i = 0
        while (i < numADCreadings):
            adcint = adcread()
            samplesADC[i] = adcint
            meanADC += adcint
            i += 1
        meanADC /= numADCreadings
        varianceADC = 0.0
        for adcint in samplesADC:
            varianceADC += (adcint - meanADC)**2
        varianceADC /= (numADCreadings - 1)
        battery_percent = ((meanADC*1400/4096)/1400)*100
        battery_percent = round(battery_percent, 2)

        if battery_percent < 20:
            return False
        else:
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

            if acceleration_result < 120 and acceleration_result > 60:
                return acceleration_result
            else:
                return False

        except:
            print("Acceleration sensor not connected")


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
