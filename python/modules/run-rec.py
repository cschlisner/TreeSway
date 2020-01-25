from TreeLogger import TreeLogger, Mode
from TreeReciever import TreeReciever
import binary

receiver = TreeReciever()

receiver.start()

def kill():
	receiver.stop()
	exit()
	