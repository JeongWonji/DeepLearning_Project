import RPi.GPIO as gpio
import time

buzzer = 21
gpio.setmode(gpio.BCM)
gpio.setup(buzzer, gpio.OUT)
gpio.setwarnings(False)

pwm = gpio.PWM(buzzer, 262)
pwm.start(50.0)
time.sleep(1.5)

pwm.stop()
gpio.cleanup()