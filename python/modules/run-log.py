from TreeLogger import TreeLogger, Mode
import binary

logger = TreeLogger(name="logger1")

logger.start()

def kill():
	logger.stop()
	exit()