#!/usr/bin/env python
import sys,math,serial,os

class SerialAccel():

	def readLine(self):
		buf = b''
		data = self.port.readline()
		if data.__len__() > 0:
			buf += data
			if b'\n' in buf and buf[0] < 0x80:
				return buf[:-2].decode()
		return ""

	def findChar(self, str,look):
		i = 0
		while i < len(str) - 1:
			if(str[i] == look):
				return 1
			i += 1
		return 0
		
				
	def clean(self, string):
		sep = '='
		string = string.strip('\r\n')
		string = string.split(sep)
		string = string[1]
		return string

	def __init__(self, loc="/dev/tty.SLAB_USBtoUART"):
		
		
		self.port = serial.Serial(loc, baudrate=115200, timeout=3.0)
		self.port.nonblocking()

		self.port.write("x\r\n".encode())
		r = self.readLine()
		
		i = 1
		while i == 1:
			while self.findChar(r,';') == 1:
				r = self.readLine()
			r = self.readLine()
			if self.findChar(r,';') != 1:
				break
			r = self.readLine()

		os.system("echo ++  >> %s"%loc)
		r = self.readLine()
		r = self.readLine()
		
		self.port.flush()

	def close(self):
		self.port.close()

	
