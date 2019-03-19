import os
import re
import socket
import RPi.GPIO as GPIO
from time import sleep

from CSVCache import CSVCache
from TreeTransmitter import TreeTransmitter

"""
Chaches and trasmits accelerometer data depending on the current operating mode. 

"""

class TreeLogger():
	"""
	Accelerometer Info
	"""
	ACC_NAME = "cp210x"
	ACC_REGEX = re.compile("^.*cp210x converter now attached.*$")
	ACC_PORT = "/dev/"

	def find_acc_port():
	    try:
	    	syslog = open("/var/log/syslog")
	    	for line in syslog:
		        if ACC_REGEX.match(line):
		            print("FOUND ACCELEROMETER AT: "+line.split(" ")[-1])
		            return line.split(" ")[-1].strip()
	    except: 
	    	return ""

	def __init__(self, name=socket.gethostname()):
		lock_primary = threading.Lock()
		lock_secondary = threading.Lock()
		self.cache_primary = CSVCache(lock_primary, name="TS_PRIMARY.csv")
		self.cache_secondary = CSVCache(lock_secondary, name="TS_SECONDARY.csv")
		self.transmitter = TreeTransmitter()
		ACC_PORT += find_acc_port()


	"""
	State of data logger 

	Mode.TRASMIT: Logger sends all data in cache while caching sensor data in secondary cache, then transitions to CACHE mode.
	Mode.CACHE: Logger adds all new sensor data to cache.
	"""
	class Mode(Enum):
		TRANSMIT = 1
		CACHE = 2

	"""
	Change operating state of logger 
	"""
	def change_mode(self, mode):
		self.opmode = mode
		if mode==Mode.TRANSMIT:
			# load all data from primary cache into memory (expensive, may be problematic)
			# Thread 1: send primary cache data over RF
			# Thread 2: send sensor data to secondary cache to avoid gaps in data
		elif mode==Mode.CACHE:
			# kill threads 1 and 2
			# swap primary and secondary caches
			# begin writing sensor data to primary cache

	def open_accelerometer(self):
		self.ACC_DEV = os.open(ACC_PORT, os.O_RDWR);



	

	
