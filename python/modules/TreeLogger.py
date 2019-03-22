import os
import re
import socket
import csv
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

	def kill(self):
		self.stopped=True

	def run(self):
		csvfile = self.cache.begin_write()
		writer = csv.writer(csvfile, delimiter=CSVCache.ROW_DELIM)
		with open(self.input, 'rb') as instream:
			while self.stopped == False:
				# write all supplied data (rows) to the cache file
				writer.writerow(list(map(lambda x: str(x), instream.read(4))))
				# delay (simulate reading rate)
				sleep(1/12)
		self.cache.end_write()

"""
Chaches and trasmits accelerometer data depending on the current operating mode. 

"""
class TreeLogger():
	
	"""
	Accelerometer Info
	"""
	ACC_NAME = "cp210x"
	ACC_REGEX = re.compile("^.*cp210x converter now attached.*$")
	def find_acc_port(self):
		try:
			syslog = open("/var/log/syslog")
			for line in syslog:
				if ACC_REGEX.match(line):
					print("FOUND ACCELEROMETER AT: "+line.split(" ")[-1])
					return "/dev/%s"%line.split(" ")[-1].strip()
		except: 
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
