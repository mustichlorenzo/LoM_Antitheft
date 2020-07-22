import os
import telegram

from picamera import PiCamera
from time import sleep

import RPi.GPIO as GPIO 
import serial 

from threading import Thread, Lock
import ffmpeg

#onoff.py
import onoff

TOKEN = "YOUR_TOKEN"

bot = telegram.Bot(TOKEN)

camera = PiCamera()

#Initialize Raspberry's pinMode and pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)

#Initialize Raspberry serial
ser = serial.Serial("/dev/ttyUSB0", 9600)

#Initialize variables for threads
activated = False
numState = 0
mutex = Lock()

#Activation by serial Thread
class activateSerialThread(Thread):
    def run(self):
        global activated, numState

        while True:
            if ser.read().decode('ascii') == 'y':
                mutex.acquire()
                
                if numState % 2 == 0:
                    print("ATTIVATO SERIALE!")
                    activated = True
                else:
                    print("DISATTIVATO SERIALE!")
                    activated = False
                
                numState = numState + 1
              
                for i in range(3):
                    GPIO.output(17, GPIO.HIGH)
                    sleep(0.1)
                    GPIO.output(17, GPIO.LOW)
                    sleep(0.1)
                
                mutex.release()

#Activation by bot Thread
class activateBotThread(Thread):
    def run(self):
        global activated, numState

        while True:
            if onoff.telegram_act is not None:
                if onoff.telegram_act:
                    mutex.acquire()
         
                    print("ATTIVATO!")
                    activated = True
                    onoff.telegram_act = None
               
                    numState = numState + 1
               
                elif not onoff.telegram_act:
                    mutex.acquire()
                   
                    print("DISATTIVATO!")
                    activated = False
                    onoff.telegram_act = None
                    
                    numState = numState + 1
               
                for i in range(3):
                    GPIO.output(17, GPIO.HIGH)
                    sleep(0.1)
                    GPIO.output(17, GPIO.LOW)
                    sleep(0.1)
                
                mutex.release()

#Initialize PIR variables
pirState = GPIO.LOW
val = 0

activateST = activateSerialThread()
activateBT = activateBotThread()

activateST.start()
activateBT.start()

onoff.update_bot()


while True:
    if activated:
        val = GPIO.input(26)

        if val == GPIO.HIGH:
            if pirState == GPIO.LOW:
                print("Motion detected\n")
                pirState = GPIO.HIGH
  
                GPIO.output(27, GPIO.HIGH)
                GPIO.output(22, GPIO.HIGH)
    
                #PiCamera records only in .mjpeg or .h264
                camera.start_recording("/home/pi/video.h264")
                sleep(10)
                camera.stop_recording()
        
                if bot.get_updates():
                    chat_id = bot.get_updates()[-1].message.chat_id
                    
                    #The version of Telegram for smartphone is unable to read file .mjpeg or .h264
                    #In order to achieve this, it is important to convert the video file in .mp4
                    os.system("ffmpeg -y -r 15 -i /home/pi/video.h264 -an -c:v copy /home/pi/video.mp4 > /dev/null 2>&1")
                    bot.send_video(chat_id, video = open("/home/pi/video.mp4", 'rb'), supports_streaming = True)
                else: 
                    print("Errore")
        
        else:
            GPIO.output(27, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)

            if pirState == GPIO.HIGH:
                print("Motion ended\n")
                pirState = GPIO.LOW

    else:
        GPIO.output(27, GPIO.LOW)
        GPIO.output(22, GPIO.LOW)

        if pirState == GPIO.HIGH:
            pirState = GPIO.LOW


            
