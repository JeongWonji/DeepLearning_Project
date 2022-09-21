import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

RUNNING = True

R_pin = 26
G_pin = 19
B_pin = 13

GPIO.setup(R_pin, GPIO.OUT)

GPIO.setup(G_pin, GPIO.OUT)

GPIO.setup(B_pin, GPIO.OUT)

Freq = 100

RED = GPIO.PWM(R_pin,Freq)
GREEN = GPIO.PWM(G_pin,Freq)
BLUE = GPIO.PWM(B_pin,Freq)

try:
    while RUNNING:
        RED.start(100)
        GREEN.start(1)
        BLUE.start(1)
        for x in range(1,101):
            GREEN.ChangeDutyCycle(x)
            time.sleep(0.05)
        for x in range(1,101):
            RED.ChangeDutyCycle(101-x)
            time.sleep(0.05)
        for x in range(1,101):
            GREEN.ChangeDutyCycle(101-x)
            BLUE.ChangeDutyCycle(x)
            time.sleep(0.05)
        for x in range(1,101):
            RED.ChangeDutyCycle(x)
            time.sleep(0.05)
except KeyboardInterrupt:
    RUNNING = False
    GPIO.cleanup()