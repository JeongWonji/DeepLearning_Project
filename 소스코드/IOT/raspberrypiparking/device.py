
import time
import paho.mqtt.client as mqtt
import RPi.GPIO as gpio
import pigpio



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
        # gpio.setup(self.servo_pin, gpio.OUT)
        self.pwm_servo.ChangeDutyCycle(duty)
        time.sleep(0.3)
        # gpio.setup(self.servo_pin, gpio.IN)
        
class pigioSERVO:
    def __init__(self):
        
        self.servo_pin = 16
        self.pwm = pigpio.pi() 
        self.pwm.set_mode(self.servo_pin, pigpio.OUTPUT)
        self.pwm.set_PWM_frequency( self.servo_pin, 50 )
        
        
    def zeroDuty(self):
        self.pwm.set_servo_pulsewidth( self.servo_pin, 500 ) ;
        self.pwm.set_PWM_dutycycle(self.servo_pin, 0)
        self.pwm.set_PWM_frequency( self.servo_pin, 0 )
    
    def nineDuty(self):
        self.pwm.set_servo_pulsewidth( self.servo_pin, 1500 ) ;
        self.pwm.set_PWM_dutycycle(self.servo_pin, 0)
        self.pwm.set_PWM_frequency( self.servo_pin, 0 )
        
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
        
# class CARMOTOR:
#     def __init__(self):
#         # 모터 상태
#         self.STOP  = 0
#         self.FORWARD  = 1
#         self.BACKWORD = 2

#         # 모터 채널
#         self.CH1 = 0
#         self.CH2 = 1

#         # PIN 입출력 설정
#         self.OUTPUT = 1
#         self.INPUT = 0

#         # PIN 설정
#         self.HIGH = 1
#         self.LOW = 0

#         # 실제 핀 정의
#         #PWM PIN
#         self.ENA = 26  #37 pin
#         self.ENB = 0   #27 pin
#         #GPIO PIN
#         self.IN1 = 19  #37 pin
#         self.IN2 = 13  #35 pin
#         self.IN3 = 6   #31 pin
#         self.IN4 = 5   #29 pin
        
#         gpio.setmode(gpio.BCM)
#         self.pwmA = self.setPinConfig(self.ENA, self.IN1, self.IN2)
#         self.pwmB = self.setPinConfig(self.ENB, self.IN3, self.IN4)
        
        
#     # 핀 설정 함수
#     def setPinConfig(self, EN, INA, INB):        
#         gpio.setup(EN, gpio.OUT)
#         gpio.setup(INA, gpio.OUT)
#         gpio.setup(INB, gpio.OUT)
#         # 100khz 로 PWM 동작 시킴 
#         pwm = gpio.PWM(EN, 100) 
#         # 우선 PWM 멈춤.   
#         pwm.start(0) 
#         return pwm

#     # 모터 제어 함수
#     def setMotorContorl(self, pwm, INA, INB, speed, stat):

#         #모터 속도 제어 PWM
#         pwm.ChangeDutyCycle(speed)  
        
#         if stat == self.FORWARD:
#             gpio.output(INA, gpio)
#             gpio.output(INB, gpio)
            
#         #뒤로
#         elif stat == self.BACKWORD:
#             gpio.output(INA, self.LOW)
#             gpio.output(INB, self.HIGH)
            
#         #정지
#         elif stat == self.STOP:
#             gpio.output(INA, self.LOW)
#             gpio.output(INB, self.LOW)

            
#     # 모터 제어함수 간단하게 사용하기 위해 한번더 래핑(감쌈)
#     def setMotor(self, ch, speed, stat):
#         if ch == self.CH1:
#             #pwmA는 핀 설정 후 pwm 핸들을 리턴 받은 값이다.
#             self.setMotorContorl(self.pwmA, self.IN1, self.IN2, speed, stat)
#         else:
#             #pwmB는 핀 설정 후 pwm 핸들을 리턴 받은 값이다.
#             self.setMotorContorl(self.pwmB, self.IN3, self.IN4, speed, stat)
            
#     def carforward(self,spd):
#         self.setMotor(self.CH1, spd, self.FORWARD)
#         self.setMotor(self.CH2, spd, self.FORWARD)
        
        