from threading import Thread
from paho.mqtt import publish
import time
import RPi.GPIO as gpio
import adafruit_dht
import board
import io
import picamera
import threading
import paho.mqtt.publish as publisher
import carmycamera
import time


class PirSensor(Thread):
    def __init__(self):
        super().__init__() #상속받은 클래스의 매개변수 없는 생성자를 호출
        gpio.setmode(gpio.BCM)
        self.pir_pin = 17
        gpio.setup(self.pir_pin,gpio.IN)
        # self.client = client
        
    def run(self):
        try:
            while True:
                if gpio.input(self.pir_pin) == 1:             
                    print("motion detected....")
                    publish.single("iot/pir","motion detected",hostname="3.25.85.102") # ,hostname="172.30.1.55"
                else:                   
                    print("no motion....")
                time.sleep(1) 
        
        except KeyboardInterrupt:
            pass
        finally:
            pass
        
class DHT11(Thread):
    def __init__(self,client):
        super().__init__() #상속받은 클래스의 매개변수 없는 생성자를 호출
        self.mydht11 = adafruit_dht.DHT11(board.D12)
        self.client = client
        
    def run(self):
        while True:
            try:
                humidity_data = self.mydht11.humidity
                temperature_data = self.mydht11.temperature
                # self.client.publish([{"iot/DHT11/humidity",humidity_data},{"iot/DHT11/temperature",temperature_data}])
                self.client.publish("iot:humidity",humidity_data)
                self.client.publish("iot:temperature",temperature_data)
                print(humidity_data,temperature_data)
                time.sleep(2) # 대기시간이 2초 필요 - 센서 내부에서 초기화작업시 필요한 시간
            
            except RuntimeError as error:
                print(error.args[0])
            
            finally:
                pass
            
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
                #     self.client.publish("iot:HC_SR04","distance:"+str(distance_value))
                    print("distance: %.2f cm" % distance_value)
                # if distance_value < 20:
                if distance_value < 20 and self.takepictureval == False:
                    print("사진 찍음")
                    cameraone = threading.Thread(target=self.takepicture)
                    cameraone.start()  
                    time.sleep(3) 
                    self.takepictureval = True
                if distance_value > 20:
                    self.takepictureval = False
                if self.takepictureval == True:
                    self.servo.getDuty(int(90))
                elif self.takepictureval == False:
                    self.servo.getDuty(int(180))
                else:
                    print("범위가 벗어남")
                
        except KeyboardInterrupt:
            pass
        finally:
            gpio.cleanup()
    
    def takepicture(self):
        print("!!!!!!!!!!!!!!!")
        shot = self.camera.oneshot()
        publisher.single("mydata/faile",shot,hostname="3.25.85.102") 
            

