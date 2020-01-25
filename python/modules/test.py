from NetTransmitter import NetTransmitter as NetT
from CSVCache import CSVCache as Cache
import random as R
import threading
import datetime 
import time

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
