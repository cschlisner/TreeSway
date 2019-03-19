import csv 
import threading

"""
Class for caching accelerometer data. 
A CSV cache consists of a single csv file, able to be read from and written to by different threads (using locks)
"""
class CSVCache():
	def __init__(self, lock, name="TreeSwayCache.csv"):
		self.name=name
		self.cahched_data = set()
		self.lock = lock
	"""
	Read data from cache into cached_data -- this consumes the cache
	"""
	def read(self):
		# aquire the thread lock; block any other operations on the cache file
		self.lock.aquire()
		print("Lock aquired for reading by %s"%threading.currentThread().getName())
		
		# read all data into memory
		with open(self.name, newline='') as csvfile:
		    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		    for row in reader:
		    	cached_data.add(row)
		        print(row)
        
        # empty the cache
		f = open(filename, "w+")
		f.close()

		# release the lock so other threads can use cache
		self.lock.release()

	"""
	Write rows of data to cache
	row format: TIME XAXIS YAXIS ZAXIS
	"""
	def write(self, data):
		# aquire the thread lock; block any other operations on the cache file
		self.lock.aquire()
		print("Lock aquired for writing by %s"%threading.currentThread().getName())
		
		# write all supplied data (rows) to the cache file
		with open(self.name, newline='') as csvfile:
		    writer = csv.writer(csvfile, delimiter=' ', quotechar='|')
		    writer.writerows(data)

		# release the lock so other threads can use cache
		self.lock.release()