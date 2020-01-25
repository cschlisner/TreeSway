import RPi.GPIO as GPIO
import csv
import numpy as np

P = [23,24,25,8]

SETUP_COMPLETE=False

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(P, GPIO.IN)

def read():
    return [GPIO.input(pin) for pin in P]

def main():
    try:
        cache = [0 for i in range(len(P))]
        while True:
            data = read()
            if (cache != data):
                print(data)
                cache = data
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    setup()
    main()