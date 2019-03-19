import csv

import RPi.GPIO as GPIO
from time import sleep

delay = .5

P = [23,24,25,8]

print("Available pins:", P)

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(P, GPIO.OUT, initial=GPIO.LOW)

def on(p):
    GPIO.output(p, GPIO.HIGH)

def off(p):
    GPIO.output(p, GPIO.LOW)

def clean():
    GPIO.cleanup()

def main():
    setup()
    try:
        for i in range(100):
            on(P[i%4])
            sleep(.3)
            off(P[i%4])
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    main()