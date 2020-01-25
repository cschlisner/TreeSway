import os
import re
import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

cahched_data = set()

def save(data):
	cahched_data.append(data)
	return

def send(f):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT))
	s.send(f)
	data = s.recv(BUFFER_SIZE)
	print "response:", data
	s.close()

DEVICE_NAME = "cp210x";
DEVICE_REGEX = re.compile("^.*cp210x converter now attached.*$")
def find_acc_port():
    try:
    	syslog = open("/var/log/syslog");
    	for line in syslog:
	        if DEVICE_REGEX.match(line):
	            print("FOUND DEVICE AT: "+line.split(" ")[-1]);
	            return line.split(" ")[-1].strip();
    except: 
    	return ""
    

accPort = "/dev/"+find_acc_port();
if (accPort == "/dev/"):
    print("NO ACCELEROMETER FOUND. USING DUMMY DATA");
    accPort = "/dev/urandom"
dev = os.open(accPort, os.O_RDWR);

while(True):
	ok = os.read(dev,40);
	readb = bytes(ok)
	save(ok)
	print();	