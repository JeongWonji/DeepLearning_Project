
import time
import paho.mqtt.client as mqtt
import RPi.GPIO as gpio



class LED:
    def __init__(self):
        gpio.setmode(gpio.BCM)
        self.led_pin = 24
        gpio.setup(self.led_pin,gpio.OUT) 
        
    def led_on(self):
        gpio.output(self.led_pin,gpio.HIGH)
        
    def led_off(self):
        gpio.output(self.led_pin,False)
        
    def clean(self):
        gpio.cleanup()

class RGBLED:
    def __init__(self):
        gpio.setmode(gpio.BCM)
        self.R_pin = 26
        self.G_pin = 19
        self.B_pin = 13
        self.Freq = 100
        gpio.setup(self.R_pin,gpio.OUT) 
        gpio.setup(self.G_pin,gpio.OUT) 
        gpio.setup(self.B_pin,gpio.OUT)
        
        self.RED = gpio.PWM(self.R_pin,self.Freq)
        self.GREEN = gpio.PWM(self.G_pin,self.Freq)
        self.BLUE = gpio.PWM(self.B_pin,self.Freq) 
        
    def led_RED(self):
        self.RED.start(100)
        self.GREEN.start(0)
        self.BLUE.start(0)
        
    def led_GREEN(self):
        self.RED.start(0)
        self.GREEN.start(100)
        self.BLUE.start(0)
        
    def led_BLUE(self):
        self.RED.start(0)
        self.GREEN.start(0)
        self.BLUE.start(100)
        
    def led_clean(self):
        self.RED.start(0)
        self.GREEN.start(0)
        self.BLUE.start(0)
        
class WATERMOTOR:
    def __init__(self):
        gpio.setmode(gpio.BCM)
        self.BA_pin = 20
        self.BB_pin = 21
        gpio.setup(self.BA_pin,gpio.OUT) 
        gpio.setup(self.BB_pin,gpio.OUT) 
        
    def watermotor_on(self):
        gpio.output(self.BA_pin,gpio.HIGH)
        gpio.output(self.BB_pin,gpio.LOW)
        
    def watermotor_off(self):
        gpio.output(self.BA_pin,gpio.LOW)
        gpio.output(self.BB_pin,gpio.LOW)
        
    def clean(self):
        gpio.cleanup()
        
class SERVO:
    def __init__(self):
        gpio.setmode(gpio.BCM)
        self.servo_pin = 16
        gpio.setup(self.servo_pin,gpio.OUT)
        self.pwm_servo = gpio.PWM(self.servo_pin, 50)
        self.pwm_servo.start(2.5) 
        
        
    def getDuty(self,degree):
        # 각도는 최소0, 최대 180으로 설정
        if degree > 180:
            degree = 180
        elif degree < 0:
            degree = 0
        duty = 2.5 + degree*10/180
        gpio.setup(self.servo_pin, gpio.OUT)
        self.pwm_servo.ChangeDutyCycle(duty)
        time.sleep(0.3)
        gpio.setup(self.servo_pin, gpio.IN)
        
class CARMOTOR:
    def __init__(self):
         
        gpio.setmode(gpio.BCM)
        self.RIGHT_FORWARD = 19
        self.RIGHT_BACKWARD = 13
        self.RIGHT_PWM = 26
        self.LEFT_FORWARD = 6
        self.LEFT_BACKWARD = 5
        self.LEFT_PWM = 0
        
        gpio.setup(self.RIGHT_FORWARD,gpio.OUT)
        gpio.setup(self.RIGHT_BACKWARD,gpio.OUT)
        gpio.setup(self.RIGHT_PWM,gpio.OUT)
        gpio.output(self.RIGHT_PWM,0)
        self.RIGHT_MOTOR = gpio.PWM(self.RIGHT_PWM,100)
        self.RIGHT_MOTOR.start(0)
        self.RIGHT_MOTOR.ChangeDutyCycle(0)
        
        gpio.setup(self.LEFT_FORWARD,gpio.OUT)
        gpio.setup(self.LEFT_BACKWARD,gpio.OUT)
        gpio.setup(self.LEFT_PWM,gpio.OUT)
        gpio.output(self.LEFT_PWM,0)
        self.LEFT_MOTOR = gpio.PWM(self.LEFT_PWM,100)
        self.LEFT_MOTOR.start(0)
        self.LEFT_MOTOR.ChangeDutyCycle(0)
        
    #RIGHT Motor control
    def rightMotor(self, forward, backward, pwm):
        gpio.output(self.RIGHT_FORWARD,forward)
        gpio.output(self.RIGHT_BACKWARD,backward)
        self.RIGHT_MOTOR.ChangeDutyCycle(pwm)
        
    #Left Motor control
    def leftMotor(self,forward, backward, pwm):
        gpio.output(self.LEFT_FORWARD,forward)
        gpio.output(self.LEFT_BACKWARD,backward)
        self.LEFT_MOTOR.ChangeDutyCycle(pwm)
            
    #Forward Car
    def forward(self):
        self.rightMotor( 1, 0, 70)
        self.leftMotor(1, 0, 70)
        time.sleep(1)

    #Left Car
    def left(self):
        self.rightMotor(1, 0, 70)
        self.leftMotor(0, 0, 70)
        time.sleep(1)
    
    #ForwardLeft Car
    def forwardleft(self):
        self.rightMotor(1, 0, 70)
        self.leftMotor(1, 0, 30)
        time.sleep(1)

    #Right Car
    def right(self):
        self.rightMotor(0, 0, 70)
        self.leftMotor(1, 0, 70)
        time.sleep(1)
    
    #ForwardRight Car
    def forwardright(self):
        self.rightMotor(1, 0, 30)
        self.leftMotor(1, 0, 70)
        time.sleep(1)

    #Backward Car
    def backward(self):
        self.rightMotor(0, 1, 70)
        self.leftMotor(0, 1, 70)
        time.sleep(1)
        
    #BackwardLeft Car
    def backwardleft(self):
        self.rightMotor(0, 1, 70)
        self.leftMotor(0, 0, 70)
        time.sleep(1)
    
    #BackwardRight Car
    def backwardright(self):
        self.rightMotor(0, 0, 70)
        self.leftMotor(0, 1, 70)
        time.sleep(1)

    #Stop Car
    def stop(self):
        self.rightMotor(0, 0, 0)
        self.leftMotor(0, 0, 0)
        
