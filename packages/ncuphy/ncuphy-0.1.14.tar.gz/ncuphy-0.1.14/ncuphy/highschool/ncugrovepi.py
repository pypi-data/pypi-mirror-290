
"""
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2017  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import smbus2 as smbus
import RPi.GPIO as GPIO


rev = GPIO.RPI_REVISION
if rev == 2 or rev == 3:
    bus = smbus.SMBus(1)
else:
    bus = smbus.SMBus(0)

# I2C Address of Arduino
address = 0x04

# Command Format
# digitalRead() command format header
dRead_cmd = [1]
# digitalWrite() command format header
dWrite_cmd = [2]
# analogRead() command format header
aRead_cmd = [3]
# analogWrite() command format header
aWrite_cmd = [4]
# pinMode() command format header
pMode_cmd = [5]

debug = 0
unused = 0


# Write I2C block
def write_i2c_block(address, block):
	try:
		return bus.write_i2c_block_data(address, 1, block)
	except IOError:
		return -1
	

# Read I2C byte
def read_i2c_byte(address):
	try:
		return bus.read_byte(address)
	except IOError:
		return -1


# Read I2C block
def read_i2c_block(address):
	try:
		return bus.read_i2c_block_data(address, 1, 10)
	except IOError:
		return -1

# Arduino Digital Read
def digitalRead(pin):
	write_i2c_block(address, dRead_cmd + [pin, unused, unused])
	# time.sleep(.1)
	n = read_i2c_byte(address)
	return n

# Arduino Digital Write
def digitalWrite(pin, value):
	write_i2c_block(address, dWrite_cmd + [pin, value, unused])
	return 1


# Setting Up Pin mode on Arduino
def pinMode(pin, mode):
	if mode == "OUTPUT":
		write_i2c_block(address, pMode_cmd + [pin, 1, unused])
	elif mode == "INPUT":
		write_i2c_block(address, pMode_cmd + [pin, 0, unused])
	return 1


# Read analog value from Pin
def analogRead(pin):
	write_i2c_block(address, aRead_cmd + [pin, unused, unused])
	read_i2c_byte(address)
	number = read_i2c_block(address)
	print(number)
	return number[1] * 256 + number[2]
