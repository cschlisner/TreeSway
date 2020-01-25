import RPi.GPIO as GPIO
from time import sleep

DELAY = .5
P = [23,24,25,8]

def setup():
    print("Available pins:", P)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(P, GPIO.OUT, initial=GPIO.LOW)

def on(p):
    GPIO.output(p, GPIO.HIGH)

def off(p):
    GPIO.output(p, GPIO.LOW)

def destroy():
    GPIO.cleanup()

def main():
    setup()
    try:
        for i in range(100):
            on(P[i%4])
            sleep(DELAY)
            off(P[i%4])
    except KeyboardInterrupt:
        destroy()

if __name__ == "__main__":
    main()