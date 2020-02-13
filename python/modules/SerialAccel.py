#!/usr/bin/env python
import sys,math,serial,os

class SerialAccel:

	def readLine(self, ser):
		str=""
		while 1:
			ch=ser.read()
			if(ch == '\r' or ch == '\n'):
				break
			str += ch
		return str

	def findChar(self, str,look):
		i = 0
		while i < len(str) - 1:
			if(str[i] == look):
				return 1
			i += 1
		return 0
		
				
	def setSample(self):
	#setup serial port
		i = 1
		port = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=3.0)
		port.nonblocking()
		port.write('x\r\n')
		r = self.readLine(port)
		while i == 1:
			while self.findChar(r,';') == 1:
				r = self.readLine(port)
			r = self.readLine(port)
			if self.findChar(r,';') != 1:
				break
			r = self.readLine(port)

		os.system('echo ++  >> /dev/ttyUSB0')
		r = self.readLine(port)
		r = self.readLine(port)
		port.flush()
		port.close()

	def clean(self, string):
		sep = '='
		string = string.strip('\r\n')
		string = string.split(sep)
		string = string[1]
		return string
