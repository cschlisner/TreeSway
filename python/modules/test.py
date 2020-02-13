from NetTransmitter import NetTransmitter as NetT
from CSVCache import CSVCache as Cache
import random as R
import threading
import datetime 
import time
import os, logging
import usb.core
import usb.util
import serial, sys, glob
import serial.tools
import serial.tools.list_ports

def ftp_test():
    cache = Cache(threading.Lock())
    cache.empty()

    t = NetT(ip='localhost')

    m = 10
    n = 10000
    cache.log_time()
    cache.write_data([[R.randint(0,255) for x in range(m)] for y in range(n)])
    cache.log_time()

    t.uploadftp(cache.name, cache.writeTimeSpan)

    cache.read()




###########         PYUSB ##################

# def usbs():

# root = logging.getLogger()
# root.setLevel(os.environ.get("PYUSB_ERROR", "DEBUG"))
# root.setLevel(os.environ.get("LIBUSB_DEBUG", 4))
os.environ['PYUSB_ERROR']="DEBUG"
os.environ['LIBUSB_DEBUG']="4"


# find our device
dev = usb.core.find(idVendor=0x10C4, idProduct=0xEA60)
interface = 0
epout = dev[0][(0,0)][0]
epin = dev[0][(0,0)][1]

# was it found?
if dev is None:
    raise ValueError('Device not found')
else:
    print(dev)
    # alt = usb.util.find_descriptor(dev[0], find_all=True, bInterfaceNumber=0) #alternate settings for configuration -- only one for cp1205

if dev.is_kernel_driver_active(interface) is True:
    # tell the kernel to detach
    dev.detach_kernel_driver(interface)
    print("Detaching kernel driver")
    # claim the device
    usb.util.claim_interface(dev, interface)

def dispose(d):
    usb.util.dispose_resources(d)



# print([comport.device for comport in serial.tools.list_ports.comports(include_links=True)])

# def serial_ports():
#     """ Lists serial port names

#         :raises EnvironmentError:
#             On unsupported or unknown platforms
#         :returns:
#             A list of the serial ports available on the system
#     """
#     if sys.platform.startswith('win'):
#         ports = ['COM%s' % (i + 1) for i in range(256)]
#     elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
#         # this excludes your current terminal "/dev/tty"
#         ports = glob.glob('/dev/tty[A-Za-z]*')
#     elif sys.platform.startswith('darwin'):
#         ports = glob.glob('/dev/tty.*')
#     else:
#         raise EnvironmentError('Unsupported platform')

#     result = []
#     for port in ports:
#         try:
#             s = serial.Serial(port)
#             s.close()
#             result.append(port)
#         except (OSError, serial.SerialException) as e:
#             print(e)
#             pass
#     return result

