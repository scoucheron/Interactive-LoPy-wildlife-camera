import machine
from time import sleep
from struct import unpack
from math import atan2,degrees,pi
class MPU():

    I2Cerror = "I2C communication failure"

    def __init__(self, disable_interrupts=False):
        self.mpu_addr = 104
        self.mpu_refresh_rate = 5
        self.i2c =  machine.I2C(0, machine.I2C.MASTER, baudrate=100000)

        # apply user setting for interrupts
        self.disable_interrupts = disable_interrupts

        # wake devise up
        self.wake()

        # set sensitivity
        self.gyro_range(0)
        self._gr = self.gyro_range()
        self.accel_range(3)
        self._ar = self.accel_range()

        self.accel_reg = 0x3B
        self.gyro_reg = 0x43


    def write(self, devaddr, memaddr, data, disable_interrupts=False):
        '''
        Perform a memory write. Caller should trap OSError.
        '''
        # irq_state = True
        # if self.disable_interrupts:
        #     irq_state = machine.disable_irq()
        self.i2c.writeto_mem(devaddr, memaddr, data)
        # machine.enable_irq(irq_state)


    def read(self, devaddr, memaddr, data):
        '''
        Perform a memory read. Caller should trap OSError. Possible values of
        error args[0]: errorno.ETIMEDOUT errno.EBUSY or errno.EIO
        '''
        # irq_state = True
        # if self.disable_interrupts:
        #     irq_state = machine.disable_irq()

        result = self.i2c.readfrom_mem(devaddr, memaddr, data)
        # machine.enable_irq(irq_state)
        return bytes(result)


    def wake(self):
        '''
        Wakes the device.
        '''
        try:
            self.write(self.mpu_addr, 0x6B, bytes(0x01))
        except:
            pass
        return 'awake'


    def sleep(self):
        '''
        Sets the device to sleep mode.
        '''
        try:
            self.write(self.mpu_addr, 0x6B, chr(0x40))
        except:
            pass

    # sample rate
    def sample_rate(self, rate=None):
        '''
        Returns the sample rate or sets it to the passed arg in Hz. Note that
        not all sample rates are possible. Check the return value to see which
        rate was actually set.
        '''

        gyro_rate = 8000 # Hz

        # set rate
        try:
            if rate is not None:
                rate_div = int( gyro_rate/rate - 1 )
                if rate_div > 255:
                    rate_div = 255
                self.write(self.mpu_addr, 0x19, rate_div)

            # get rate
            rate = gyro_rate/(unpack('<H', self.read(self.mpu_addr, 0x19, 1))[0]+1)
        except OSError:
            rate = None
        return rate


########## GYROSCOPE ##########

    def gyro(self, xyz=None):
        '''
        Returns the accelerations on axis passed in arg. Pass xyz or every
        subset of this string. None defaults to xyz.
        '''
        if xyz is None:
            xyz = 'xyz'

        scale = (131.0, 65.5, 32.8, 16.4)

        try:
            graw = self.read(self.mpu_addr, self.gyro_reg, 6)
        except OSError:
            graw = b'\x00\x00\x00\x00\x00\x00'

        gxyz = {'x': unpack('>h', graw[0:2])[0]/scale[self._gr],
                'y': unpack('>h', graw[2:4])[0]/scale[self._gr],
                'z': unpack('>h', graw[4:6])[0]/scale[self._gr]}

        gout = []
        for char in xyz:
            gout.append(gxyz[char])
        return gout

    # gyroscope range
    def gyro_range(self, gyro_range=None):
        '''
        Returns the gyroscope range or sets it to the passed arg.
        Pass:               0   1   2    3
        for range +/-:      250 500 1000 2000  degrees/second
        '''
        # set range
        try:
            if gyro_range is None:
                pass
            else:
                gr = (0x00, 0x08, 0x10, 0x18)
                try:
                    self.write(self.mpu_addr, 0x1B, bytes(gr[gyro_range]))
                except IndexError:
                    print('gyro_range can only be 0, 1, 2 or 3')
            # get range
            grange = int(unpack('<H', self.read(self.mpu_addr, 0x1B, 1))[0]/8)
        except OSError:
            grange = None

        if grange is not None:
            self._gr = grange
        return grange

    # get gyro pitch - y - axis in degrees
    def get_gy(self):
        scale = (131.0, 65.5, 32.8, 16.4)
        raw = self.read(self.mpu_addr, self.gyro_reg, 6)
        gy =  unpack('>h', raw[2:4])[0]/scale[self._gr]
        return gy

########## ACCELEROMETER ##########

    # get acceleration
    def accel(self, xyz=None):
        '''
        Returns the accelerations on axis passed in arg. Pass xyz or every
        subset of this string. None defaults to xyz.
        '''
        if xyz is None:
            xyz = 'xyz'
        # machine.enable_irq(irq_state)
        scale = (16384, 8192, 4096, 2048)

        try:
            graw = self.read(self.mpu_addr, self.accel_reg, 6)
        except OSError:
            graw = b'\x00\x00\x00\x00\x00\x00'

        axyz = {'x': unpack('>h', graw[0:2])[0]/scale[self._ar],
                'y': unpack('>h', graw[2:4])[0]/scale[self._ar],
                'z': unpack('>h', graw[4:6])[0]/scale[self._ar]}

        aout = []
        for char in xyz:
            aout.append(axyz[char])
        return aout

    # accelerometer range
    def accel_range(self, accel_range=3):
        '''
        Returns the accelerometer range or sets it to the passed arg.
        Pass:               0   1   2   3
        for range +/-:      2   4   8   16  g
        '''
        # set range
        try:
            if accel_range is None:
                pass
            else:
                ar = (0x00, 0x08, 0x10, 0x18)
                try:
                    self.write(self.mpu_addr, 0x1C, bytes(ar[accel_range]))
                except IndexError:
                    print('accel_range can only be 0, 1, 2 or 3')
            # get range
            ari = int(unpack('<H', self.read(self.mpu_addr, 0x1C, 1))[0]/8)
        except OSError:
            ari = None
        if ari is not None:
            self._ar = ari
        return ari


    # get pitch
    def pitch(self):
        '''
        Returns pitch angle in degrees based on x and z accelerations.

        '''
        scale = (16384, 8192, 4096, 2048)
        raw = self.read(self.mpu_addr, self.accel_reg, 6)
        y = unpack('>h', raw[2:4])[0]/scale[self._ar]
        z = unpack('>h', raw[4:6])[0]/scale[self._ar]
        pitch = degrees(pi+atan2(-y,-z))
        if (pitch>=180) and (pitch<=360):
            pitch-=360
        return pitch
