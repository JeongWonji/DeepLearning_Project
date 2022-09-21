from cgi import test
import threading
import paho.mqtt.client as mqtt
from threading import Thread, Event
from mysensor import HC_SR04
from device import SERVO
import carmycamera
import RPi.GPIO as gpio
import paho.mqtt.publish as publisher
import time
import pygame
import I2C_LCD_driver
import device
import pigpio

class MqttWorker:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.camera = carmycamera.MyCamera()
        
        self.rgbled = device.RGBLED()
        
        
        self.exit_event = Event()
        # self.DHT11 = DHT11(self.client)
        # self.DHT11.start()
        
        self.HC_SR04 = HC_SR04(self.client)
        self.HC_SR04.start()
        
        # self.camera =  MyCamera(self.client)
        # self.camera.start(self.client)
        self.servo = 16
        self.pwm = pigpio.pi() 
        self.pwm.set_mode(self.servo, pigpio.OUTPUT)
 
        self.pwm.set_PWM_frequency( self.servo, 50 )
    
    def signal_handler(self,signum,frame):
        print("signal_handler===================================")
        self.exit_event.set() # 이벤트객체가 갖고 있는 플래그 변수가 True로 셋팅
        self.led.clean()
        # 현재 이벤트 발생을 체크하고 다른 작업을 수행하기 위한 코드 - 다른 메소드에서 처리
        if self.exit_event.is_set():
            print("이벤트객체의 플래그변수가 Ture로 바뀜 - 이벤트가 발생하면 어떤 작업을 실행하기 위해서(다른 메소드 내부에서 반복문 빠져나오기~....)")
            exit(0)
        
    def mymqtt_connect(self): # 사용자정의 함수 - mqtt서버연결과 쓰레드생성 및 시작을 사용자정의 함수로 정의
        try:
            print("브로커 연결 시작하기")
            self.client.connect("3.25.85.102",1883,60)
            mythreadobj = Thread(target=self.client.loop_forever)
            mythreadobj.start()
        except KeyboardInterrupt:
            pass
        finally:
            print("종료") 
               
    def on_connect(self,client, userdata, flags, rc): # broker접속에 성공하면 자동으로 호출되는 callback함수
        print("connect..."+str(rc)) # rc가 0이면 성공 접속, 1이면 실패
        if rc==0 : #연결이 성공하면 구독신청
            client.subscribe("iot/#")
            client.subscribe("web/carnumber")
            client.subscribe("web/carhandicap")
            client.subscribe("web/carimg")
            client.subscribe("web")
            client.subscribe("picamera:one")
            client.subscribe("parking/#")
            
            # client.subscribe("picture")
            
        else:
            print("연결실패.....")   
            
    # 라즈베리파이가 메시지를 받으면 호출되는 함수이므로 받은 메시지에 대한 처리를 구현
    def on_message(self,client, userdata, message): 
        try:
            print("message_on")
            myval = message.payload.decode("utf-8")
            print(message.topic+"-----"+myval)
            myval2 = myval.split(":")
            if myval == "led_red":
                self.rgbled.led_RED()
            elif myval == "led_green":
                self.rgbled.led_GREEN()
            elif myval == "led_blue":
                self.rgbled.led_BLUE()
            elif myval == "led_off":
                self.rgbled.led_clean()
            elif myval == "fail":
                mylcd = I2C_LCD_driver.lcd()
                mylcd.lcd_display_string("illegal parking",1)
                mylcd.lcd_display_string("",2)
                print("failtest")
                self.rgbled.led_RED()
                speakerfailthread = threading.Thread(target=self.speakfail)
                speakerfailthread.start()
                print("test:fail")
                time.sleep(3)
                mylcd2 = I2C_LCD_driver.lcd()
                mylcd2.lcd_display_string("",1)
                mylcd2.lcd_display_string("",2)
                self.rgbled.led_clean()
                
            elif myval == "ok":
                mylcd = I2C_LCD_driver.lcd()
                mylcd.lcd_display_string("good time",1)
                mylcd.lcd_display_string("",2)
                self.rgbled.led_BLUE()
                speakerokthread = threading.Thread(target=self.speakok)
                speakerokthread.start()
                print("test:ok")
                time.sleep(3)
                mylcd2 = I2C_LCD_driver.lcd()
                mylcd2.lcd_display_string("",1)
                mylcd2.lcd_display_string("",2)
                self.rgbled.led_clean()
            elif myval == "servo_on":
                self.pwm.set_servo_pulsewidth( self.servo, 1500 ) ;
            elif myval == "servo_off":
                self.pwm.set_servo_pulsewidth( self.servo, 2500 )
                
            elif myval2[1] == "start":
                camerathread = threading.Thread(target=self.cameratest)
                camerathread.start()
            elif message.topic == "picamera:one":
                print("test-----shot")
                f = open("output.jpg","wb")
                f.write(message.payload)
                print("메시지 수신완료 - 파일 저장하기 완료")
                f.close()
            
                
        except:
            pass
        finally:
            pass
        
    def cameratest(self):
        print("================================")
        while True:
            frame = self.camera.getStreaming()
            publisher.single("picamera:mycamera",frame,hostname="3.25.85.102")
            
    def failpicture(self):
        print("!!!!!!!!!!!!!!!")
        shot = self.camera.oneshot()
        publisher.single("picamera:fail",shot,hostname="3.25.85.102")
        
    def speakfail(self):
        pygame.mixer.init()
        pygame.mixer.music.load("/home/pi/mywork/basic/cameratest/ttstest/noparking.mp3")
        pygame.mixer.music.play()
        time.sleep(2)
        
    def speakok(self):
        pygame.mixer.init()
        pygame.mixer.music.load("/home/pi/mywork/basic/cameratest/ttstest/goodtime.mp3")
        pygame.mixer.music.play()
        time.sleep(2)
        
         
        
        

        