import os, sys
import re
import socket
import csv
from time import sleep
import threading
from enum import Enum
import logging
import json

from CSVCache import CSVCache
from NetInterface import FTPNet
from AccInterface import SerialAcc

log = logging.getLogger(__name__)

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
	def __init__(self, cache, acc):
		threading.Thread.__init__(self)
		self.cache = cache
		self.dev = acc
		self.stopped = False
			
	def kill(self):
		self.stopped=True

	def run(self):

		# setup cache		
		csvfile = self.cache.begin_write()
		writer = csv.writer(csvfile, delimiter=CSVCache.ROW_DELIM)
		
		# store beginning time (for remote cache name)
		self.cache.log_time()

		# read and cache data until we're told to stop
		while self.stopped == False:
			writer.writerow(self.dev.read().split(","))
		
		# clean up cache/serial device
		self.cache.end_write()
		self.dev.close()


"""
Chaches and trasmits accelerometer data depending on the current operating mode. 
"""
class TreeLogger():
	
	def __init__(self, name=socket.gethostname(), config_path="config.json"):
		
		# load settings into object for reference
		self.config = json.load(open(config_path))

		# We start in cache mode (assuming no data at start)
		self.opmode=Mode.CACHE

		# create primary, secondary caches
		lock_primary = threading.Lock()
		self.cache_primary = CSVCache(lock_primary, name="%s-TS_PRIMARY.csv"%name)
		lock_secondary = threading.Lock()
		self.cache_secondary = CSVCache(lock_secondary, name="%s-TS_SECONDARY.csv"%name)
		
		# set up network -- FTP 
		self.network = FTPNet(config=self.config['network']['debug']['ftp'])

		# set up accelerometer -- Serial
		self.accelerometer = SerialAcc(config=self.config['accelerometer'])

		# background thread for caching data
		self.reader_thread = None
	
		
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
			log.info("-- TRANSMITTING --")
			self.transmit()
		elif mode==Mode.CACHE:
			log.info("-- CACHING --")
			self.cache()

	def transmit(self):
		# stop logging acceleromter data to primary cache
		if self.reader_thread is not None:
			log.info("killing cache thread")
			self.reader_thread.kill()
		
		# start acceleromter data logging to secondary cache
		log.info("starting new cache thread")
		self.reader_thread = CacheThread(self.cache_secondary, self.accelerometer)
		self.reader_thread.start()

		# send primary cache over network, then delete it from local filesystem
		log.info("sending primary cache data")
		self.network.upload(self.cache_primary.name, self.cache_primary.writeTimeSpan)
		log.info("emptying cache")
		self.cache_primary.empty()

		# stop logging acceleromter data to secondary cache
		log.info("killing cache thread")
		self.reader_thread.kill()

		# All data from primary cache is now sent
		# instead of actually moving the data in the secondary cache to the primary, let's just swap the references
		log.info("swapping cache data")
		cache_p_name = self.cache_primary.name
		self.cache_primary.name = self.cache_secondary.name
		self.cache_secondary.name = cache_p_name

		# Switch back to caching mode
		self.change_mode(Mode.CACHE)

	def cache(self):
		log.info("starting new cache thread")
		# start reading accelerometer data into primary cache
		self.reader_thread = CacheThread(self.cache_primary, self.accelerometer)
		self.reader_thread.start()
		# self.reader_thread.join()

		# wait 10 sec and transmit 
		sleep(10)
		self.change_mode(Mode.TRANSMIT)
