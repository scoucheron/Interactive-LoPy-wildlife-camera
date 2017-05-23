import machine

TX_RESET = [0x56, 0x00, 0x26, 0x00]
RX_RESET = [ 0x76, 0x00, 0x26, 0x00 ]

TX_TAKE_PICTURE = [ 0x56, 0x00, 0x36, 0x01, 0x00 ]
RX_TAKE_PICTURE = [ 0x76, 0x00, 0x36, 0x00, 0x00 ]

TX_READ_JPEG_FILE_SIZE = [ 0x56, 0x00, 0x34, 0x01, 0x00 ]
RX_READ_JPEG_FILE_SIZE = [ 0x76, 0x00, 0x34, 0x00, 0x04, 0x00, 0x00 ]

TX_READ_JPEG_FILE_CONTENT = [ 0x56, 0x00, 0x32, 0x0C, 0x00, 0x0A, 0x00, 0x00 ]
RX_READ_JPEG_FILE_CONTENT = [ 0x76, 0x00, 0x32, 0x00, 0x00 ]

TX_STOP_TAKING_PICTURES = [ 0x56, 0x00, 0x36, 0x01, 0x03 ]
RX_STOP_TAKING_PICTURES = [ 0x76, 0x00, 0x36, 0x00, 0x00 ]

TX_SET_COMPRESSION_RATIO = [ 0x56, 0x00, 0x31, 0x05, 0x01, 0x01, 0x12, 0x04 ]
RX_SET_COMPRESSION_RATIO = [ 0x76, 0x00, 0x31, 0x00, 0x00 ]

TX_SET_IMAGE_SIZE = [ 0x56, 0x00, 0x31, 0x05, 0x04, 0x01, 0x00, 0x19 ]
RX_SET_IMAGE_SIZE = [ 0x76, 0x00, 0x31, 0x00, 0x00 ]

TX_ENTER_POWER_SAVING = [ 0x56, 0x00, 0x3E, 0x03, 0x00, 0x01, 0x01 ]
RX_ENTER_POWER_SAVING = [ 0x76, 0x00, 0x3E, 0x00, 0x00 ]

TX_EXIT_POWER_SAVING = [ 0x56, 0x00, 0x3E, 0x03, 0x00, 0x01, 0x00 ]
RX_EXIT_POWER_SAVING = [ 0x76, 0x00, 0x3E, 0x00, 0x00 ]

TX_CHANGE_BAUD_RATE = [ 0x56, 0x00, 0x24, 0x03, 0x01 ]
RX_CHANGE_BAUD_RATE = [ 0x76, 0x00, 0x24, 0x00, 0x00 ]

class LSY201():
    def __init__(self, baudRate = 38400):
        self.eof = False
        self.ser = UART(1, baudRate)
        self.ser.init(9600, bits=8, parity=None, stop=1)

    def reset():
        self.ser.write(TX_RESET)
        self.ser.read(RX_RESET)

    def takePicture():
        self.eof = False
        self.ser.write(TX_TAKE_PICTURE)
        self.ser.read(RX_TAKE_PICTURE)

    def readJpegFileSize():
        self.ser.write(TX_READ_JPEG_FILE_SIZE)
        self.ser.read(RX_READ_JPEG_FILE_SIZE)
        return ((readByte()) << 8) | readByte()

    def readJpegFileContent(offset, buf, size):
          last = 0x00

          if(self.eof):
            return False

          self.ser.write(TX_READ_JPEG_FILE_CONTENT)

          params = [ (offset & 0xFF00) >> 8, (offset & 0x00FF), 0x00, 0x00, (size & 0xFF00) >> 8, (size & 0x00FF), 0x00, 0x0A]

          self.ser.write(params, len(params))
          self.ser.read(RX_READ_JPEG_FILE_CONTENT)

          while (size --):
            buf++ = readByte()

            if (last == 0xFF && buf[-1] == 0xD9):
              self.eof = True

            last = buf[-1]

          self.ser.read(RX_READ_JPEG_FILE_CONTENT)
          return True


    def setCompressionRatio(value):
        self.ser.write(TX_SET_COMPRESSION_RATIO)
        self.ser.write(value)
        self.ser.read(RX_SET_COMPRESSION_RATIO)

    def setImageSize(size):
        self.ser.write(TX_SET_IMAGE_SIZE)
        self.ser.write(size)
        self.ser.read(RX_SET_IMAGE_SIZE)

    def setBaudRate(baud):
        self.ser.write(TX_CHANGE_BAUD_RATE)
        params = 0xC8AE # 9600

        if baud = 19200:
            params = 0xE456
        elif baud = 19200:
            params = 0xE456
        elif baud = 38400:
            params = 0xF22A
        elif baud = 57600:
            params = 0x4C1C
        elif baud = 115200:
            params = 0xA60D

        self.ser.write(params)
        self.ser.read(RX_CHANGE_BAUD_RATE)

    def stopTakingPictures():
        self.ser.write(TX_STOP_TAKING_PICTURES)
        self.ser.read(RX_STOP_TAKING_PICTURES)
