import base64
from threading import Thread
from paho.mqtt import publish
import time
import RPi.GPIO as gpio
import threading
import paho.mqtt.publish as publisher
import carmycamera
import time
from device import SERVO, pigioSERVO
import pigpio
import I2C_LCD_driver

            
class HC_SR04(Thread):
    def __init__(self,client):
        super().__init__() #상속받은 클래스의 매개변수 없는 생성자를 호출
        gpio.setmode(gpio.BCM)
        self.TRIGER = 5
        self.ECHO = 6 
        gpio.setup(self.TRIGER,gpio.OUT)
        gpio.setup(self.ECHO,gpio.IN)
        self.client = client
        self.camera = carmycamera.MyCamera()
        self.takepictureval = False
        self.servo = 16
        self.pwm = pigpio.pi() 
        self.pwm.set_mode(self.servo, pigpio.OUTPUT)
 
        self.pwm.set_PWM_frequency( self.servo, 50 )
        
    def getDistance(self):
        gpio.output(self.TRIGER,False)
        time.sleep(1)
        gpio.output(self.TRIGER,True)
        time.sleep(0.00001)
        gpio.output(self.TRIGER,False)

        while gpio.input(self.ECHO) == 0 :
            pulse_start = time.time() # 현재 시간을 측정
            
        while gpio.input(self.ECHO) == 1 :
            pulse_end= time.time() # ECHO가 LOW
            
        pulse_duration = pulse_end - pulse_start
        
        distance = pulse_duration*340*100/2
        distance = round(distance,2)
        
        return distance
    
    def run(self):
        try:
            while True:
                distance_value = HC_SR04.getDistance(self)
                if 2 < distance_value < 400:
                    print("distance: %.2f cm" % distance_value)
                if distance_value < 30 and self.takepictureval == False:
                    print("사진 찍음")
                    # cameraone = threading.Thread(target=self.takepicture)
                    # cameraone.start() 
                    cameraone2 = threading.Thread(target=self.takepicturenum)
                    cameraone2.start() 
                    time.sleep(3) 
                    self.takepictureval = True
                if distance_value > 30:
                    self.takepictureval = False
                if self.takepictureval == True:
                    self.pwm.set_servo_pulsewidth( self.servo, 1500 ) ;
                elif self.takepictureval == False: 
                    self.pwm.set_servo_pulsewidth( self.servo, 2500 ) ;
                else:
                    print("범위가 벗어남")
                
        except KeyboardInterrupt:
            pass
        finally:
            gpio.cleanup()
    
    def takepicture(self): # 주차 공간에서 촬영한 사진 퍼브
        print("!!!!!!!!!!!!!!!")
        shot = self.camera.oneshot()
        publisher.single("mydata/number",shot,hostname="3.25.85.102")
    
    def takepicturenum(self):  # 주차장 입구에서 촬영한 사진 퍼브
        print("number!!!!!")
        shot = self.camera.oneshot()
        publisher.single("mydata/number",shot,hostname="3.25.85.102")
        publisher.single("mydata/faile",shot,hostname="3.25.85.102")
        shot = base64.b64encode(shot)
        shot = shot.decode("utf-8")
        publisher.single("web/img",shot,hostname="3.25.85.102") 
            

