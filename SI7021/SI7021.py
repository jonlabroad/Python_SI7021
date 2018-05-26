import logging
import math
import time

# Default I2C address for device.
SI7021_I2CADDR_DEFAULT        = 0x40

# Si7021 Commands (https://cdn-learn.adafruit.com/assets/assets/000/035/931/original/Support_Documents_TechnicalDocs_Si7021-A20.pdf)
SI7021_MEAS_HUMIDITY_HMM			= 0xE5 # Measure Relative Humidity, Hold Master Mode
SI7021_MEAS_HUMIDITY_NO_HMM 		= 0xF5 #Measure Relative Humidity, No Hold Master Mode 0xF5
SI7021_MEAS_TEMP_HMM				= 0xE3 #Measure Temperature, Hold Master Mode 0xE3
SI7021_MEAS_TEMP_NO_HMM 			= 0xF3 #Measure Temperature, No Hold Master Mode 0xF3
SI7021_MEAS_TEMP_PREV 				= 0xE0 #Read Temperature Value from Previous RH Measurement 0xE0
SI7021_RESET 						= 0xFE #Reset 0xFE
SI7021_WRITE_USER_1 				= 0xE6 #Write RH/T User Register 1 0xE6
SI7021_READ_USER_1 					= 0xE7 #Read RH/T User Register 1 0xE7
SI7021_WRITE_HEATER_CONTROL 		= 0x51 #Write Heater Control Register 0x51
SI7021_READ_HEATER_CONTROL 			= 0x11 #Read Heater Control Register 0x11
SI7021_READ_ELECTRONIC_ID_BYTE_1 	= [0xFA, 0x0F] #Read Electronic ID 1st Byte 0xFA 0x0F
SI7021_READ_ELECTRONIC_ID_BYTE_2 	= [0xFC, 0xC9] #Read Electronic ID 2nd Byte 0xFC 0xC9
SI7021_READ_FIRMWARE_REV 			= [0x84, 0xB8] #Read Firmware Revision 0x84 0xB8

class SI7021(object):
    """Class to represent an Adafruit SI7021 precision temperature measurement
    board.
    """

    def __init__(self, address=SI7021_I2CADDR_DEFAULT, i2c=None, **kwargs):
        """Initialize SI7021 device on the specified I2C address and bus number.
        """
        self._logger = logging.getLogger('SI7021.SI7021')
        if i2c is None:
            import Adafruit_GPIO.I2C as I2C
            i2c = I2C
        self._device = i2c.get_i2c_device(address, **kwargs)

    def begin(self):
        """Start taking temperature measurements. Returns True if the device is
        intialized, False otherwise.
        """
		# TODO, defaults might be fine anyhow

	def readTempC(self):
		"""Read sensor and return its value in degrees celsius."""
		# Initiate a temperature read
		self._device.writeRaw8(SI7021_MEAS_TEMP_NO_HMM)
		time.sleep(0.1)
		# Read temperature register value.
		tempRaw = self._device.readU16BE(SI7021_MEAS_TEMP_PREV)

		# Scale and convert to signed value.
		temp = 175.72 * tempRaw / 65536 - 46.85
		return temp

	def readHumidity(self):
		"""Read sensor and return humidity value in percent relative humidity"""
		self._device.writeRaw8(SI7021_MEAS_HUMIDITY_NO_HMM)
		time.sleep(1.0)
		# TODO How to read 16 bytes without referencing a register???
		humRaw1 = self._device.readRaw8()
		humRaw2 = self._device.readRaw8()
		print hex(humRaw1) + " " + hex(humRaw2)
