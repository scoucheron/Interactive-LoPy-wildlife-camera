import machine
import tsl2561
import ujson

class Sensors():
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

    ''' Takes a picture and saves it on the SD-card '''
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