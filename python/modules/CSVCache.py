import csv 
import threading
import os


"""
Class for caching accelerometer data. 
A CSV cache consists of a single csv file, able to be read from and written to by different threads (using locks)
"""
class CSVCache():

	# amount of columns in cache
	ROW_SIZE = 4
	# character signalling end of row in bytestreams DO NOT CHANGE -- comma needed for ascii conversion
	ROW_TERM = ","
	# character deliminating columns
	ROW_DELIM = " "

	def __init__(self, lock, name="TreeSwayCache.csv", directory="log/"):
		self.time="0"
		self.name=directory+name
		self.dataset = []
		self.lock = lock
		if not os.path.isdir(directory):
			os.mkdir(directory)

	"""
	Read data from cache into cached_data -- this consumes the cache
	"""
	def read(self):
		# aquire the thread lock; block any other operations on the cache file
		self.lock.acquire()
		print("Lock aquired for %s reading by %s"%(self.name,threading.currentThread().getName()))
		
		# read all data into memory
		with open(self.name, newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter=' ')
			for row in reader:
				self.dataset.append(row)
				#print(row)
        
        # empty the cache
		f = open(self.name, "w+")
		f.close()

		# release the lock so other threads can use cache
		self.lock.release()

	def empty(self):
		# empty the cache
		f = open(self.name, "w+")
		f.close()

	"""
	Get lock on CSV file for writing, returns opened file
	"""
	def begin_write(self):
		# aquire the thread lock; block any other operations on the cache file
		self.lock.acquire()
		print("Lock aquired for %s writing by %s"%(self.name,threading.currentThread().getName()))
		self.csvfile = open(self.name, 'a+', newline='') 
		return self.csvfile
		
	def end_write(self):
		# release the lock so other threads can use cache
		self.csvfile.close()
		self.lock.release()