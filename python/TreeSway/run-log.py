from TreeLogger import TreeLogger, Mode

logger = TreeLogger(name="logger1")

logger.start()

def kill():
	logger.stop()
	exit()