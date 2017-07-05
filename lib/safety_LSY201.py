## Mads Adrian Hansen, mha308@post.uit.no
## Developed May 2017 for INF-3910-3

"""
    Micropython source for the Link Sprite Y201 camera

    As of 03.07.17:
    _savePicture() is not working properly. Had problems with
    timing the reading and saving to file at the same time. Some variation of
    the commented out code has worked.

    reset() has not been working as expected. The first while loop is a
    hack to solve it ish, but the assert on the returned value have failed at
    several occasions if reset is called before the camera is finished returning
    a photo.
"""
import utime
import machine
import ubinascii as b2a

class LSY:
    def __init__(self, uartID, baudRate=38400):
        self.baudRate = baudRate
        self.uart = machine.UART(uartID)
        self.uart.init(self.baudRate, bits=8, parity=None, stop=1)
        self.reset()
        self.setResolution('160x120')

    def _transmit(self,hexPack):
        bytesPack = b2a.unhexlify(hexPack)
        return self.uart.write(bytesPack)

    def _receive(self,nbytes):
        while self.uart.any() < nbytes:
            utime.sleep(0.001)
        bytesPack = self.uart.read(nbytes)
        return b2a.hexlify(bytesPack)

    def reset(self):
        ## Dump RX of camera
        while self.uart.any():
            _ = self.uart.read()
            utime.sleep(0.001)
        ## Send reset command, assert length of sent command
        n = self._transmit(b'56002600')
        assert n == 4, "In reset: Transmit error "
        ## Check return value
        returned = self._receive(4)
        assert returned == b'76002600', "In reset: Receive error . {}".format(returned)
        ## Loop to find init complete from camera
        a = b''
        while True:
            tmp = self.uart.readline()
            a += (tmp if tmp is not None else b'')
            # print(b2a.hexlify(a))
            if a is not None:
                if b2a.hexlify(a[-10:]) == b'496e697420656e640d0a':
                    break
            utime.sleep(10/self.baudRate)

    def setBaudRate(self, baudRate):
        baudRates = {
            9600:   b'5600240301AEC8',
            19200:  b'560024030156E4',
            38400:  b'56002403012AF2',
            57600:  b'56002403011C4C',
            115200: b'56002403010DA6'
        }
        assert baudRate in baudRates, 'Value ' + baudRate + ' is not a valid baudrate'

        ## Send command to change camera's baud rate
        n = self._transmit(baudRates[baudRate])
        ## The unhexlifyed version of the baudRates shall have length 7
        assert n == 7, "In baudRate: Transmit error "
        ## Receive return value from camera and assert it
        returned = self._receive(5)
        assert returned == b'7600240000', "In baudRate: Receive error . {}".format(returned)

        self.baudRate = baudRate
        self.uart.close()
        self.uart.init(baudRate)


    def setResolution(self, resolution):
        resolutions = {
            "640x480": b'560031050401001900',
            "320x240": b'560031050401001911',
            "160x120": b'560031050401001922'
        }
        assert resolution in resolutions, 'Value ' + resolution + ' is not a valid resolution'
        self.resolution = resolution

        ## Send command to change camera's image size
        n = self._transmit(resolutions[resolution])
        ## The unhexlifyed version of the resolutions shall have length 9
        assert n == 9, "In setResolution: Transmit error "
        ## Receive return value from camera and assert it
        returned = self._receive(5)
        assert returned == b'7600310000', "In setResolution: Receive error . {}".format(returned)

    def _getSize(self):
        n = self._transmit(b'5600340100')
        assert n==5, "In _getSize: Receive error "
        returned = self._receive(9)
        print(len(returned))
        assert returned[:14] == b'76003400040000', "In _getSize: Receive error . {}".format(returned)

        return returned[14:18]

    def _takePicture(self):
        n = self._transmit(b'5600360100')
        assert n == 5, 'In takePicture: Transmit error '
        returned = self._receive(5)
        assert returned == b'7600360000', 'In takePicture: Receive error. {}'.format(returned)


    def _savePicture(self,filename='pic.jpeg'):
        MHML,KHKL,XXXX = b'0000', self._getSize(), b'000A'
        # MHML,KHKL,XXXX = b'0000', b'FFFF', b'000A'
        m,st = int(KHKL,16),int(XXXX,16)*1E-5
        print(KHKL,m)

        hexPack = b'5600320C000A0000' + MHML + b'0000' + KHKL + XXXX
        n = self._transmit(hexPack)
        assert n == 16, 'In _savePicture: Transmit error'
        returned = self._receive(5)
        assert returned == b'7600320000', 'In takePicture: Receive error. {}'.format(returned)
        # print(self.uart.any())
        # for i in range(20):
        #     utime.sleep(2**i*st)
        #     print(2**i*st,self.uart.any())
        #
        # return
        utime.sleep(st)

        # A=[]
        # while self.uart.any():
        #     A.append(self.uart.read(m))
        #     utime.sleep(st)
        #
        # utime.sleep(st)
        # returned = b2a.hexlify((A[-1])[-5:])
        # assert returned == b'7600320000', 'In takePicture: Receive error. {}'.format(returned)
        #
        # (A[-1]) = (A[-1])[:-5]

        # l = 0
        # f = open(filename,'w')
        # for a in A:
        #     b=b2a.hexlify(a)
        #
        #     print(b)
        #     l += f.write(b)
        # f.close()
        # print('l=',l)

        f = open(filename,'w')

        ## Fails if last 7 bits doesn't come in same read
        while True:
            tmp = self.uart.read(m)
            #print("\n********\n\n")
            #print(b2a.hexlify(tmp))
            #print("\n********\n\n")

            if b2a.hexlify(tmp[-7:]) == b'ffd97600320000':
                f.write(tmp[:-5])
            else:
                f.write(tmp)
                if not self.uart.any():
                    utime.sleep(1)

        f.close()

        # print(b2a.hexlify(tmp))

        utime.sleep(st)
        # returned = self._receive(5)
        # assert returned == b'7600320000', 'In takePicture: Receive error. {}'.format(returned)

        # f = open(filename,'w')
        # f.write(pic)
        # f.close()

        return

        picture = b''

        # picture = self._receive(2)
        # assert picture == b'ffd8'
        while True:
            tmp = self._receive(8)
            print(tmp)
            picture += tmp
            utime.sleep(int(XXXX,16)*0.02)
            # if (tmp[0:4]==b'FFD9' or tmp[2:6]==b'FFD9' or tmp[4:8]==b'FFD9' or
            #     tmp[6:10]==b'FFD9' or tmp[8:12]==b'FFD9' or tmp[10:14]==b'FFD9' or
            #     tmp[12:16]==b'FFD9'):
            if tmp[-4:]==b'ffd9':
                print('ffd9')
                break
            if self.uart.any() < 8:
                print('end')
                picture+= self._receive(self.uart.any())
                break


        return picture

    def stopTakingPictures(self):
        n = self._transmit(b'5600360103')
        assert n == 5, 'In stopTakingPictures: Transmit error '
        returned = self._receive(5)
        assert returned == b'7600360000', 'In stopTakingPictures: Receive error. {}'.format(returned)

    def close(self):
        self.uart.uinit()
sa
