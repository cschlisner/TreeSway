import os, sys
import re
import socket
import csv
import serial
from time import sleep
import threading
from enum import Enum

from CSVCache import CSVCache
# from TreeTransmitter import TreeTransmitter
from NetTransmitter import NetTransmitter

"""
State of data logger 

Mode.TRASMIT: Logger sends all data in cache while caching sensor data in secondary cache, then transitions to CACHE mode.
Mode.CACHE: Logger adds all new sensor data to cache.
"""
class Mode(Enum):
	TRANSMIT = 1
	CACHE = 2

"""
Thread to cache data from input in a CSVCache
"""
class CacheThread(threading.Thread):
	def __init__(self, cache, inputdev):
		threading.Thread.__init__(self)
		self.cache = cache
		self.input = inputdev
		self.stopped = False
	
	def readLine(self, ser):
		buf = b''
		data = ser.readline()
		if data.__len__() > 0:
			buf += data
			if b'\n' in buf and buf[0] < 0x80:
				return buf[:-2].decode()
		return ""
		
	def kill(self):
		self.stopped=True

	def run(self):
		# serial set up
		port = serial.Serial(self.input, baudrate=115200, timeout=3.0)
		port.nonblocking()
		port.write('x\r\n'.encode()) # reset device
		port.write('--\r\n'.encode()) # halve sample rate
		for i in range(9):
			port.readline() # get rid of info lines
			
		csvfile = self.cache.begin_write()
		writer = csv.writer(csvfile, delimiter=CSVCache.ROW_DELIM)
		while self.stopped == False:
			writer.writerow(self.readLine(port).split(","))
		self.cache.end_write()

"""
Chaches and trasmits accelerometer data depending on the current operating mode. 

"""
class TreeLogger():
	
	"""
	Accelerometer Info
	"""
	
	def find_acc_port(self):
		ACC_NAME = "cp210x"
		ACC_REGEX = re.compile("^.*cp210x converter now attached.*$")
		try:
			syslog = open("/var/log/syslog")
			for line in syslog:
				if ACC_REGEX.match(line):
					print("FOUND ACCELEROMETER AT: "+line.split(" ")[-1])
					return "/dev/%s"%line.split(" ")[-1].strip()
		except Exception as e:
			print(e) 
			return "/dev/urandom"

	def __init__(self, name=socket.gethostname()):
		self.opmode=Mode.CACHE
		lock_primary = threading.Lock()
		lock_secondary = threading.Lock()
		self.cache_primary = CSVCache(lock_primary, name="%s-TS_PRIMARY.csv"%name)
		self.cache_secondary = CSVCache(lock_secondary, name="%s-TS_SECONDARY.csv"%name)
		# self.transmitter = TreeTransmitter()
		self.network = NetTransmitter()
		self.ACC_PORT = self.find_acc_port()
		self.accel_reader = None
	
	
		
	def start(self,mode=Mode.CACHE):
		
		
		#port.write('c\r\n'.encode()) # get config
		#print(self.readLine(port))
		#port.write('s\r\n'.encode()) # get status
		#print(self.readLine(port))
		
		self.change_mode(mode)
		
	def stop(self):
		self.accel_reader.kill()


	"""
	Change operating state of logger 
	"""
	def change_mode(self, mode):
		self.opmode = mode
		if mode==Mode.TRANSMIT:
			print("-- TRANSMITTING --")
			self.transmit()
		elif mode==Mode.CACHE:
			print("-- CACHING --")
			self.cache()

	def transmit(self):
		# kill acceleromter logging to primary cache
		if self.accel_reader is not None:
			print("killing cache thread")
			self.accel_reader.kill()
		
		print("starting new cache thread")
		# start acceleromter logging to secondary cache
		self.accel_reader = CacheThread(self.cache_secondary, self.ACC_PORT)
		self.accel_reader.start()

		print("reading primary cache")
		# load all data from primary cache into memory (expensive, may be problematic)
		self.cache_primary.read()

		print("sending primary cache data")
		# send primary cache data over RF until everything is sent
		self.network.send(self.cache_primary.dataset)

		print("killing cache thread")
		# stop the accelerometer reading
		self.accel_reader.kill()

		print("swapping cache data")
		# All data from primary cache is now sent, swap the secondary and primary caches
		cache_p_name = self.cache_primary.name
		self.cache_primary.name = self.cache_secondary.name
		self.cache_secondary.name = cache_p_name

		# Switch back to caching mode
		self.change_mode(Mode.CACHE)

	def cache(self):
		print("starting new cache thread")
		# start reading accelerometer data into primary cache
		self.accel_reader = CacheThread(self.cache_primary, self.ACC_PORT)
		self.accel_reader.start()
		# self.accel_reader.join()
