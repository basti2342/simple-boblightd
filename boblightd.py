#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ./boblightd.py localhost:5555
# boblight-X11 -slocalhost:5555 -y off

import socket, sys
from dioder import Dioder

class BoblightServer:
	def __init__(self, host, port, serialPort="/dev/ttyACM0", baudrate=57600, numOfStrips=4):
		self.numOfStrips = numOfStrips
		self.handle = { "hello": self.hello, # reply hello
					 "get version": self.version, # send version number
					 "get lights": self.getLights, # send light responsibility
					 "set light": self.setLight, # get colors from screen
					 "ping": self.ping } # send pong

		self.stripes = [ (0,0,0) for i in range(self.numOfStrips) ]

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((host, port))
		s.listen(1)

		print "Waiting for boblight client to connect.."
		self.conn, addr = s.accept()
		print "..done."
		self.dioder = Dioder(serialPort, baudrate)

	def send(self, msg):
		print "[send]", msg
		self.conn.sendall("%s\n" % msg)

	def serve(self):
		rest = ""
		data = rest + self.conn.recv(1024)
		data = data.split("\n")
		dataList, rest = data[:-1], data[-1]
		for data in dataList:
			print "[recv]", data
			keyString = " ".join(data.split()[:2])
			if keyString in self.handle:
				self.handle[keyString](data)

	def hello(self, data):
		self.send("hello")

	def version(self, data):
		self.send("version 5")

	def ping(self, data):
		self.send("ping 0")

	def getLights(self, data):
		# send number of lights
		self.send("lights %d" % self.numOfStrips)

		# divide the screen into parts
		part = 50 / self.numOfStrips
		for i in range(self.numOfStrips):
			# which light is responsible for which part of the screen
			self.send("light %d scan 0 100 %d %d" % (i, (i*part)+50, ((i+1)*part)+50))

	def setLight(self, data):
		# receive new light data
		dataList = data.split()

		# ignore fancy light features
		if dataList[3] != "rgb": return

		# abuse the name as light number
		lightNum = int(dataList[2])
		r, g, b = dataList[4:7]
		r, g, b = float(r), float(g), float(b)

		alt_r, alt_g, alt_b = r, g, b

		"""
		# FILTER / SMOOTH LIGHTS
		# full brightness
		if sum((r,g,b)) > 0.01:
			diff = 0.5 / max(r,g,b)
			r, g, b = r*diff, g*diff, b*diff
		else:
			print "black"

		 dim bright white
		if abs(r - g) < 0.35 and abs(g - b) < 0.35 and sum((r, g, b)) > 0.3:
			r = r * 0.2
			g = g * 0.2
			b = b * 0.2
			print "%s dimmed:" % lightNum
		"""

		print "%s\t%s\t%s\t%s\t\t%s\t%s\t%s\t\t%s" % (lightNum, round(r, 3), round(g, 3), round(b, 3), round(alt_r, 3), round(alt_g, 3), round(alt_b, 3), round(sum((r,b,g)), 3))

		# print line break after last light
		if lightNum == 3: print

		self.stripes[lightNum] = (r, g, b)
		self.dioder.setColor(*self.stripes)


def main():
	try:
		args = sys.argv[1].split(":")
		server = BoblightServer(args[0], int(args[1]))

		while True:
				server.serve()
	except (IndexError, ValueError):
		print "Please specify host/port: %s HOST:PORT" % sys.argv[0]


if __name__ == '__main__':
	main()
