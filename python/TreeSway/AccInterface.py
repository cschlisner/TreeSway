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


class SerialAcc:

	""" Static method for locating CP210x Accelerometer """
	def find_device():
		acc_id_string = "VID:PID=%X:%X"%(ID_VEND, ID_PROD)
		
		for comport in serial.tools.list_ports.comports():
			# print(comport, comport.usb_info())
			desc = comport.usb_info()
			if acc_id_string in desc or ACC_NAME in desc:
				log.info("Found device '%s' at %s: %s"%(ACC_NAME, comport, desc))
				return comport.device
		return None

	""" Reads (and decodes) one line of data from the accelerometer """
	def read(self):
		try:
			return self.port.readline()[:-2].decode()
		except:
			return ""

	""" Encodes and writes data to the accelerometer, reads device response
	"""
	def write(self, msg):
		try:
			self.port.write(msg.decode())
			for i in range(5):
				print(self.port.readline())
		except:
			pass

	def __init__(self, dev=None, config=None):
		# store default sample rate
		self.samplerate=50
		
		# if no device location was supplied, find it using the vendor/product IDs
		if dev is None:
			dev = SerialAcc.find_device()
		
		self.port = serial.Serial(dev, baudrate=115200, timeout=3.0)

		# reset the device
		self.reset()

		# apply settings from config
		if config is not None:
			self.set_samplerate(config['samplerate'])
			self.set_microresolution(config['microresolution'])


	""" SSP-x Commands -- see http://gcdataconcepts.com/GCDC_SSP_User_Manual.pdf """

	def set_samplerate(self, samplerate):	
		# only available rates for cp210x
		samplerates = [12,25,50,100,200]
		# get highest available rate at or equal to requested rate
		sr = max(filter(lambda r: r <= samplerate, samplerates))
		# current sample rate
		csr = self.samplerate
		# double/half sample rate until we get there
		while (csr != sr):
			if (csr < sr):
				self.write("+")
				csr = csr<<1
			else:
				self.write("-")
				csr = csr>>1
			for i in range(5):
					print(self.port.readline())
		# store new device samplerate
		self.samplerate = csr
	def stop_datastream(self):
		self.write("D")
	def start_datastream(self):
		self.write("d")
	def reset(self):
		self.write('x')
	def set_microresolution(self, m):
		self.write("m" if m else "M")
	def version(self):
		self.write("v")
	def status(self):
		self.write("s")
	def configuration(self):
		self.write("c")

	def close(self):
		self.port.flush()
		self.port.close()

class USBAcc():

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

	
