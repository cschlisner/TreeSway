import RPi.GPIO as GPIO
from time import sleep

"""
Handles all communication via GPIO pins.

Pins for communication are available via TreeTransmitter.pins -- numbered 0 through n

"""
class TreeTransmitter():
    DELAY = .5

    def __init__(self, opins=[23,24,25,8], ipins=[]):
        self.opins=opins
        self.ipins=ipins
        self.pinc=len(opins)
        self.setup()

    def setup(self):
        print("Available output pins:", self.opins)
        print("Available input pins:", self.ipins)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.opins, GPIO.OUT, initial=GPIO.LOW)
        if (self.ipins != [])
            GPIO.setup(self.ipins, GPIO.IN)

    """
    Set the ith output pin to HIGH (1)
    """
    def on(self, i):
        GPIO.output(self.opins[i], GPIO.HIGH)

    """
    Set the ith output pin to LOW (0)
    """
    def off(self, i):
        GPIO.output(self.opins[i], GPIO.LOW)

    """
    Turn all output pins off
    """
    def clear(self):
        GPIO.output(self.opins, GPIO.LOW)

    """
    Close the GPIO pins, perform other cleanup actions
    """
    def destroy(self):
        GPIO.cleanup()

    """
    Transmit a word ($pinc bits)
    """
    def send(self, word):
        bn = bin(word)[2:(2+self.pinc)]
        for i, bt in enumerate(bn):
            if bt:
                self.on(i)
        self.clear()

    """
    Reads data from input pins, returns list of pin statuses
    """
    def recieve(self):
        return [GPIO.input(pin) for pin in self.ipins]

    """
    Cycle through all output pins turning each on and off
    """
    def test_output(self):
        try:
            for i in range(100):
                on(P[i%self.pinc])
                sleep(DELAY)
                off(P[i%self.pinc])
        except KeyboardInterrupt:
            destroy()
