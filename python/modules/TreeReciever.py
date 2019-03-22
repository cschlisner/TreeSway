# from TreeTransmitter import TreeTransmitter
from NetTransmitter import NetTransmitter
from CSVCache import CSVCache
import csv
import threading
import socket
import binary

class CSVLogThread(threading.Thread):
	def __init__(self, cache, data):
		threading.Thread.__init__(self)
		self.cache = cache
		self.data = data

	def run(self):
		csvfile = self.cache.begin_write()
		writer = csv.writer(csvfile, delimiter=' ')

		# write all supplied data (rows of rows of data) to the cache file
		for row in self.data:
			print("writing", row)
			writer.writerow(row)
		self.cache.end_write()

class NetListenThread(threading.Thread):

	def __init__(self, cache, ip='127.0.0.1', port=5005):
		threading.Thread.__init__(self)
		self.tcp_port=5005
		self.ip=ip
		self.cache = cache
		self.stopped = False
		self.writethreads = []

	def kill(self):
		self.stopped = True
		for thread in self.writethreads:
			thread.join()

	"""
	Decodes binary string to ascii character 
	b is a (8-digit) binary string without the prefix '0b'
	"""
	def bin2str(self,b):
		try: 
			if b=='101100': return ","
			return int('0b'+b[:-2],2).to_bytes(1, 'big').decode()
		except:
			print("what the fuck")
			print(sys.exc_info()[0])

	def run(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((self.ip, self.tcp_port))
		s.listen(5)

		recv_buff = ""
		recv_row = [""]
		recv_data = [] # array of rows of data
		while not self.stopped:
			try:
				conn, addr = s.accept()
				print('New client address:', addr)
				data = conn.recv(1024)
				print("recieved data", data)
				
				while not self.stopped and (data or recv_buff!=""):
					if data:
						decoded=data.decode() # "binary" data
						print("decoded data", decoded)
					else: decoded=""
					
					# data can be partial -- only process first 8 bytes and put the remainder in buffer
					decoded=recv_buff+decoded
					recv_buff = decoded[8:]
					decoded=decoded[:8]
					print("decoded data[:8]", decoded)


					char=binary.b2s(decoded)
					print("recieved char '%s'"%char)
					
					# end of a row of data -- add the last row to the list
					if (char == ","):
						recv_data.append(recv_row)
						recv_row = [""]
					elif (char == " "):
						recv_row.append("")
					else:
						recv_row[-1]+=str(char)

					data = conn.recv(1024)
				
				if self.stopped:
					break
				
				print("All data received:", recv_data)
				conn.close()

				# write out received data to cache
				write_thread = CSVLogThread(self.cache, recv_data)
				write_thread.start()
				self.writethreads.append(write_thread)
				recv_data = []
			except:
				continue
		if conn:
			conn.close()		
		s.close()

class TreeReciever():
	def __init__(self):
		self.cache = CSVCache(threading.Lock(), name="ListenerCache.csv")	

	def start(self):
		print("starting listener thread")
		# listen on network for new data
		self.listener = NetListenThread(self.cache)
		self.listener.start()
		# self.listener.join()

	def stop(self):
		self.listener.kill()
