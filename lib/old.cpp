
static const uint8_t TX_RESET[] = { 0x56, 0x00, 0x26, 0x00 };
static const uint8_t RX_RESET[] = { 0x76, 0x00, 0x26, 0x00 };

static const uint8_t TX_TAKE_PICTURE[] = { 0x56, 0x00, 0x36, 0x01, 0x00 };
static const uint8_t RX_TAKE_PICTURE[] = { 0x76, 0x00, 0x36, 0x00, 0x00 };

static const uint8_t TX_READ_JPEG_FILE_SIZE[] = { 0x56, 0x00, 0x34, 0x01, 0x00 };
static const uint8_t RX_READ_JPEG_FILE_SIZE[] = { 0x76, 0x00, 0x34, 0x00, 0x04, 0x00, 0x00 };

static const uint8_t TX_READ_JPEG_FILE_CONTENT[] = { 0x56, 0x00, 0x32, 0x0C, 0x00, 0x0A, 0x00, 0x00 };
static const uint8_t RX_READ_JPEG_FILE_CONTENT[] = { 0x76, 0x00, 0x32, 0x00, 0x00 };

static const uint8_t TX_STOP_TAKING_PICTURES[] = { 0x56, 0x00, 0x36, 0x01, 0x03 };
static const uint8_t RX_STOP_TAKING_PICTURES[] = { 0x76, 0x00, 0x36, 0x00, 0x00 };

static const uint8_t TX_SET_COMPRESSION_RATIO[] = { 0x56, 0x00, 0x31, 0x05, 0x01, 0x01, 0x12, 0x04 };
static const uint8_t RX_SET_COMPRESSION_RATIO[] = { 0x76, 0x00, 0x31, 0x00, 0x00 };

static const uint8_t TX_SET_IMAGE_SIZE[] = { 0x56, 0x00, 0x31, 0x05, 0x04, 0x01, 0x00, 0x19 };
static const uint8_t RX_SET_IMAGE_SIZE[] = { 0x76, 0x00, 0x31, 0x00, 0x00 };

static const uint8_t TX_ENTER_POWER_SAVING[] = { 0x56, 0x00, 0x3E, 0x03, 0x00, 0x01, 0x01 };
static const uint8_t RX_ENTER_POWER_SAVING[] = { 0x76, 0x00, 0x3E, 0x00, 0x00 };

static const uint8_t TX_EXIT_POWER_SAVING[] = { 0x56, 0x00, 0x3E, 0x03, 0x00, 0x01, 0x00 };
static const uint8_t RX_EXIT_POWER_SAVING[] = { 0x76, 0x00, 0x3E, 0x00, 0x00 };

static const uint8_t TX_CHANGE_BAUD_RATE[] = { 0x56, 0x00, 0x24, 0x03, 0x01 };
static const uint8_t RX_CHANGE_BAUD_RATE[] = { 0x76, 0x00, 0x24, 0x00, 0x00 };

LSY201::LSY201()
{
  _debug = NULL;
  _eof = false;
}

void LSY201::setSerial(Stream &stream)
{
  _camera = &stream;
}

void LSY201::setDebugSerial(Stream &stream)
{
  _debug = &stream;
}

void LSY201::reset()
{
  resetWithoutWaitingForInitEnd();
  waitForInitEnd();
}

void LSY201::resetWithoutWaitingForInitEnd()
{
  while (_camera->available())
    _camera->read();

  tx(TX_RESET, sizeof(TX_RESET));
  rx(RX_RESET, sizeof(RX_RESET));
}

void LSY201::waitForInitEnd()
{
  char buf[25] = { 0 }, *p = buf;

  while (1)
  {
    *p = readByte();

    if (*p == '\n')
    {
      if (_debug)
        _debug->print(buf);

      if (strcmp(buf, "Init end\r\n") == 0)
        break;

      memset(buf, 0, sizeof(buf));
      p = buf;
    }
    else
      p ++;
  }
}

void LSY201::takePicture()
{
  _eof = false;
  tx(TX_TAKE_PICTURE, sizeof(TX_TAKE_PICTURE));
  rx(RX_TAKE_PICTURE, sizeof(RX_TAKE_PICTURE));
}

uint16_t LSY201::readJpegFileSize()
{
  tx(TX_READ_JPEG_FILE_SIZE, sizeof(TX_READ_JPEG_FILE_SIZE));
  rx(RX_READ_JPEG_FILE_SIZE, sizeof(RX_READ_JPEG_FILE_SIZE));

  return (((uint16_t) readByte()) << 8) | readByte();
}

bool LSY201::readJpegFileContent(uint16_t offset, uint8_t *buf, uint16_t size)
{
  static uint8_t last = 0x00;

  if (_eof)
    return false;

  tx(TX_READ_JPEG_FILE_CONTENT, sizeof(TX_READ_JPEG_FILE_CONTENT));

  uint8_t params[] = {
    (offset & 0xFF00) >> 8,
    (offset & 0x00FF),
    0x00,
    0x00,
    (size & 0xFF00) >> 8,
    (size & 0x00FF),
    0x00,
    0x0A
  };

  tx(params, sizeof(params));

  rx(RX_READ_JPEG_FILE_CONTENT, sizeof(RX_READ_JPEG_FILE_CONTENT));

  while (size --)
  {
    *buf++ = readByte();

    if (last == 0xFF && buf[-1] == 0xD9)
      _eof = true;

    last = buf[-1];
  }

  rx(RX_READ_JPEG_FILE_CONTENT, sizeof(RX_READ_JPEG_FILE_CONTENT));

  return true;
}

void LSY201::setCompressionRatio(uint8_t value)
{
  tx(TX_SET_COMPRESSION_RATIO, sizeof(TX_SET_COMPRESSION_RATIO));
  tx(&value, 1);

  rx(RX_SET_COMPRESSION_RATIO, sizeof(RX_SET_COMPRESSION_RATIO));
}

void LSY201::setImageSize(Size size)
{
  tx(TX_SET_IMAGE_SIZE, sizeof(TX_SET_IMAGE_SIZE));
  tx((uint8_t *) &size, 1);

  rx(RX_SET_IMAGE_SIZE, sizeof(RX_SET_IMAGE_SIZE));
}

void LSY201::setBaudRate(unsigned long baud)
{
  tx(TX_CHANGE_BAUD_RATE, sizeof(TX_CHANGE_BAUD_RATE));

  uint16_t params = 0xC8AE; /* 9600 */
  switch (baud)
  {
    case 19200: params = 0xE456; break;
    case 38400: params = 0xF22A; break;
    case 57600: params = 0x4C1C; break;
    case 115200: params = 0xA60D; break;;
  };

  tx((uint8_t *) &params, 2);

  rx(RX_CHANGE_BAUD_RATE, sizeof(RX_CHANGE_BAUD_RATE));
}

void LSY201::stopTakingPictures()
{
  tx(TX_STOP_TAKING_PICTURES, sizeof(TX_STOP_TAKING_PICTURES));
  rx(RX_STOP_TAKING_PICTURES, sizeof(RX_STOP_TAKING_PICTURES));
}

void LSY201::tx(const uint8_t *bytes, uint8_t length)
{
  if (_debug)
    _debug->print("sending bytes:");

  while (length --)
  {
    if (_debug)
    {
      _debug->print(" ");
      _debug->print(*bytes, HEX);
    }

    _camera->write(*bytes);

    bytes ++;
  }

  if (_debug)
    _debug->println("");
}

void LSY201::rx(const uint8_t *bytes, uint8_t length)
{
  int i;

  if (_debug)
  {
    _debug->print("expecting bytes:");

    for (i = 0; i < length; i ++)
    {
      _debug->print(' ');
      _debug->print(bytes[i], HEX);
    }

    _debug->println();
  }

  for (i = 0; i < length; i ++)
  {
    uint8_t byte = readByte();

    if (_debug)
    {
      _debug->print(byte, HEX);
      _debug->print(" ");
      _debug->println(byte == bytes[i] ? "ok" : "unexpected");
    }
  }
}

uint8_t LSY201::readByte()
{
  while (!_camera->available())
    ;

  return _camera->read();
}
