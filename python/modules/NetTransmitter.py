import socket
import binary
from CSVCache import CSVCache

class NetTransmitter():
	def __init__(self, ip='127.0.0.1', port=5005):
		self.tcp_port=5005
		self.ip=ip

	"""
	Send all data rows in dataset as individual bytes
	"""
	def send(self, dataset):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((self.ip, self.tcp_port))
		for row in dataset:
			# print("sending",row)
			rowstr = ''.join([" "+x for x in row]).strip()+","
			rowbytes = binary.chunk(binary.s2b(rowstr))
			for byte in rowbytes:
				s.send(bytes(byte,encoding='utf'))
		s.close()

	def listen(self):
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