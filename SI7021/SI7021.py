import logging
import math


# Default I2C address for device.
SI7021_I2CADDR_DEFAULT        = 0x18

# Register addresses.
SI7021_REG_CONFIG             = 0x01
SI7021_REG_UPPER_TEMP         = 0x02
SI7021_REG_LOWER_TEMP         = 0x03
SI7021_REG_CRIT_TEMP          = 0x04
SI7021_REG_AMBIENT_TEMP       = 0x05
SI7021_REG_MANUF_ID           = 0x06
SI7021_REG_DEVICE_ID          = 0x07

# Configuration register values.
SI7021_REG_CONFIG_SHUTDOWN    = 0x0100
SI7021_REG_CONFIG_CRITLOCKED  = 0x0080
SI7021_REG_CONFIG_WINLOCKED   = 0x0040
SI7021_REG_CONFIG_INTCLR      = 0x0020
SI7021_REG_CONFIG_ALERTSTAT   = 0x0010
SI7021_REG_CONFIG_ALERTCTRL   = 0x0008
SI7021_REG_CONFIG_ALERTSEL    = 0x0002
SI7021_REG_CONFIG_ALERTPOL    = 0x0002
SI7021_REG_CONFIG_ALERTMODE   = 0x0001


class SI7021(object):
	"""Class to represent an Adafruit SI7021 precision temperature measurement
	board.
	"""

	def __init__(self, address=SI7021_I2CADDR_DEFAULT, i2c=None, **kwargs):
		"""Initialize MCP9808 device on the specified I2C address and bus number.
		Address defaults to 0x18 and bus number defaults to the appropriate bus
		for the hardware.
		"""
		self._logger = logging.getLogger('Adafruit_MCP9808.MCP9808')
		if i2c is None:
			import Adafruit_GPIO.I2C as I2C
			i2c = I2C
		self._device = i2c.get_i2c_device(address, **kwargs)


	def begin(self):
		"""Start taking temperature measurements. Returns True if the device is 
		intialized, False otherwise.
		"""
		# Check manufacturer and device ID match expected values.
		mid = self._device.readU16BE(SI7021_REG_MANUF_ID)
		did = self._device.readU16BE(SI7021_REG_DEVICE_ID)
		self._logger.debug('Read manufacturer ID: {0:04X}'.format(mid))
		self._logger.debug('Read device ID: {0:04X}'.format(did))
		return mid == 0x0054 and did == 0x0400

	def readTempC(self):
		"""Read sensor and return its value in degrees celsius."""
		# Read temperature register value.
		t = self._device.readU16BE(SI7021_REG_AMBIENT_TEMP)
		self._logger.debug('Raw ambient temp register value: 0x{0:04X}'.format(t & 0xFFFF))
		# Scale and convert to signed value.
		temp = (t & 0x0FFF) / 16.0
		if t & 0x1000:
			temp -= 256.0
		return temp
