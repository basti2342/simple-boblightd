#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial, struct, time

""" Control Ikea Dioder LED strip """
class Dioder:
	def __init__(self, device, baudrate):
		try:
			self.dioder = serial.Serial(device, baudrate)
			time.sleep(2)
		except (serial.serialutil.SerialException, OSError):
			print "Please connect Dioder to %s." % device
			#quit()
			self.dioder = Dry()

	def __del__(self):
		self.dioder.close()

	def checksum(self, body):
		result = ord(body[0])
		for i in range(0, len(body)):
			if i > 0:
				result = result ^ ord(body[i])
		return struct.pack('B', result)

	""" Set colors of all strips. Takes 3 RGB tuples. """
	def setColor(self, strip1, strip2, strip3, strip4):
		colors = [strip1, strip2, strip3, strip4]

		# write header
		self.dioder.write('\xBA\xBE')

		# write body
		body = ""
		for color in colors:
			# RGB => GBR
			for v in [color[1]*255, color[2]*255, color[0]*255]:
				body += chr(int(v))
		self.dioder.write(body)

		# write checksum
		self.dioder.write(self.checksum(body))

class Dry(object):
	def write(self, cmd):
		print cmd

	def close(self):
		pass

""" For testing purposes only. """
def main():
	print "setting color"
	dioder = Dioder("/dev/ttyACM0", 57600)
	color = (1, 1, 1)

	dioder.setColor(color, color, color, color)


if __name__ == '__main__':
	main()
