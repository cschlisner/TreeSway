import socket
import os
import binary
from CSVCache import CSVCache
import ftplib

class NetTransmitter():
	def __init__(self, ip='167.99.161.157', port_tcp=5005, port_ftp=21):
		self.tcp_port=port_tcp
		self.ftp_port=port_ftp
		self.ip=ip

	"""
	upload file to ftp server
	"""
	def uploadftp(self, cache, name):
		session = ftplib.FTP(self.ip, 'treelogger', 'treesway')
		# session.login()
		file = open(cache,'rb')                
		session.storbinary('STOR %s.csv'%name, file) 
		file.close()                                   
		session.quit()

	"""
	Send all data rows in dataset as individual bytes
	"""
	def sendtcp(self, dataset):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((self.ip, self.tcp_port))
		for row in dataset:
			# print("sending",row)
			rowstr = ''.join([" "+x for x in row]).strip()+","
			rowbytes = binary.chunk(binary.s2b(rowstr))
			for byte in rowbytes:
				s.send(bytes(byte,encoding='utf'))
		s.close()

	def listentcp(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((self.ip, self.tcp_port))
		s.listen(5)

		
		while True:
			try:
				conn, addr = s.accept()
				print('New client address:', addr)
				data = conn.recv(1024)
				if not data: 
					conn.close()
					continue
				while data:
					print("received data:", data.decode())
					data = conn.recv(1024)

				conn.send(bytes("aknowledged",encoding='utf'))  # echo
				conn.close()
			except:
				continue
		s.close()