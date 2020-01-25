# from TreeTransmitter import TreeTransmitter
from NetTransmitter import NetTransmitter, NetListenThread
from CSVCache import CSVCache
import csv
import threading
import socket
import binary


def cmd(cmd):
	if cmd == "1":
		print("Recieved Command #1")
	if cmd == "1":
		print("Recieved Command #2")

class TreeReceiver():
	def __init__(self):
		self.cache = CSVCache(threading.Lock(), name="ListenerCache.csv")	

	def start(self):
		print("starting listener thread")
		# listen on network for new data
		self.listener = NetListenThread(cache=self.cache, cmdfn=self, port=5005)
		self.listener.start()
		# self.listener.join()
		self.network = NetTransmitter(port=5006)

	def stop(self):
		self.listener.kill()
