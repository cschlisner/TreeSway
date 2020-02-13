#!/usr/bin/env python
import sys, os
import logging
import math
import serial, serial.tools, serial.tools.list_ports
import usb.core, usb.util


ID_VEND=0x10C4
ID_PROD=0xEA60
ACC_NAME = "CP210x"

log = logging.getLogger(__name__)


class SerialAccel:

	""" Static """
	def find_accel():
		acc_id_string = "VID:PID=%X:%X"%(ID_VEND, ID_PROD)
		
		for comport in serial.tools.list_ports.comports():
			# print(comport, comport.usb_info())
			desc = comport.usb_info()
			if acc_id_string in desc or ACC_NAME in desc:
				log.info("Found device '%s' at %s: %s"%(ACC_NAME, comport, desc))
				return comport
		return None

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

class USBAccel():

	def __init__(self):
		
		# logging
		# os.environ['PYUSB_ERROR']="DEBUG"
		# os.environ['LIBUSB_DEBUG']="4"

		# find our device
		self.dev = usb.core.find(idVendor=ID_VEND, idProduct=ID_PROD)
		interface = 0
		epout = dev[0][(0,0)][0]
		epin = dev[0][(0,0)][1]

		# was it found?
		if dev is None:
			raise ValueError('Device not found')
		else:
			print(dev)
			# alt = usb.util.find_descriptor(dev[0], find_all=True, bInterfaceNumber=0) #alternate settings for configuration -- only one for cp1205

		if dev.is_kernel_driver_active(interface) is True:
			# tell the kernel to detach
			dev.detach_kernel_driver(interface)
			print("Detaching kernel driver")
			# claim the device
			usb.util.claim_interface(dev, interface)

	def close(self):
		usb.util.dispose_resources(self.dev)

	
