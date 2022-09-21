import RPi.GPIO as GPIO
import time
import random
 
R_pin = 26
G_pin = 19
B_pin = 13
 
def setup():
    global pwmR, pwmG, pwmB
    GPIO.setmode(GPIO.BOARD)
      # iterate on the RGB pins, initialize each and set to HIGH to turn it off (COMMON ANODE)
    GPIO.setup(R_pin, GPIO.OUT)
    GPIO.output(R_pin, GPIO.HIGH)
    GPIO.setup(G_pin, GPIO.OUT)
    GPIO.output(G_pin, GPIO.HIGH)
    GPIO.setup(B_pin, GPIO.OUT)
    GPIO.output(B_pin, GPIO.HIGH)
    
    pwmR = GPIO.PWM(R_pin, 2000)  # set each PWM pin to 2 KHz
    pwmG = GPIO.PWM(G_pin, 2000)
    pwmB = GPIO.PWM(B_pin, 2000)
    pwmR.start(0)   # initially set to 0 duty cycle
    pwmG.start(0)
    pwmB.start(0)
     
def setColor(r, g, b):  # 0 ~ 100 values since 0 ~ 100 only for duty cycle
    pwmR.ChangeDutyCycle(r)
    pwmG.ChangeDutyCycle(g)
    pwmB.ChangeDutyCycle(b)
     
def displayColors():
    setColor(100, 0, 0) #   red color
    time.sleep(1)   # 1s
    setColor(0, 100, 0) # green
    time.sleep(1)   # 1s
    setColor(0, 0, 100) # blue
    time.sleep(1)   # 1s
    setColor(100, 100, 0) # yellow
    time.sleep(1)   # 1s
    setColor(0, 100, 100) # cyan
    time.sleep(1)   # 1s
    setColor(100, 0, 100) # magenta
    time.sleep(1)   # 1s
    setColor(50, 0, 0) # maroon
    time.sleep(1)   # 1s
    setColor(50, 0, 50) # purple
    time.sleep(1)   # 1s
    setColor(0, 0, 50) # navy
    time.sleep(1)   # 1s
     
def destroy():
    pwmR.stop()
    pwmG.stop()
    pwmB.stop()
    GPIO.cleanup()
     
if __name__ == '__main__':
    setup()
    displayColors()
    destroy()