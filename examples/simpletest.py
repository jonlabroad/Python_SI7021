#!/usr/bin/python

# Can enable debug output by uncommenting:
#import logging
#logging.basicConfig(level=logging.DEBUG)

import time

import SI7021.SI7021 as SI7021


# Define a function to convert celsius to fahrenheit.
def c_to_f(c):
	return c * 9.0 / 5.0 + 32.0

# Default constructor will use the default I2C address (0x18) and pick a default I2C bus.
#
# For the Raspberry Pi this means you should hook up to the only exposed I2C bus
# from the main GPIO header and the library will figure out the bus number based
# on the Pi's revision.
sensor = SI7021.SI7021()

# Optionally you can override the address and/or bus number:
#sensor = SI7021.SI7021(address=0x20, busnum=2)

# Initialize communication with the sensor.
#sensor.begin()

# Loop printing measurements every second.
print('Press Ctrl-C to quit.')
while True:
	temp = sensor.readTempC()
	print('Temperature: {0:0.3F}*C / {1:0.3F}*F'.format(temp, c_to_f(temp)))
	time.sleep(1.0)

	humidity = sensor.readHumidity()
	print('Humidity: {0:0.1F}%%'.format(humidity))
	time.sleep(1.0)
