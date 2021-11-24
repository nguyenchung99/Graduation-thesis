
# author: Nguyễn Thành Chung
# date: 13/09/2021

import cv2
import os 
import numpy as np
import sqlite3
from PIL import Image
import speech_recognition
import pyttsx3
from datetime import date, time
from datetime import datetime
import time
import serial


robot_listen = speech_recognition.Recognizer() # khoi tao robot_listen nhu mot cai tai de co the nghe 
robot_speak = pyttsx3.init()
robot_brain = ""

arduino_serial = serial.Serial('COM6', 9600)
s = arduino_serial.readline()

def led_on():
	arduino_serial.write('1'.encode())
	print("led on")
def led_off():
	arduino_serial.write('0'.encode())
	print("led off")
def fan_on():
    arduino_serial.write('3'.encode())
    print("fan on")
def fan_off():
    arduino_serial.write('2'.encode())
    print("fan off")

# ham tro ly ao
def virtual():
    robot_brain = "Hello Boss"
    robot_speak.say(robot_brain)
    robot_speak.runAndWait()
    while True:
        robot_listen = speech_recognition.Recognizer()
        with speech_recognition.Microphone() as mic: 
        # mic = speech_recognition.Microphone()         
            robot_listen.adjust_for_ambient_noise(mic)
            print("Robot: I'm listening")	
            audio = robot_listen.record(mic, duration = 5) # audio = am thanh nghe duoc tu mic 
            # audio = robot_listen.record(mic, duration=3)
            print("...")

        try:
            you = robot_listen.recognize_google(audio, language = 'en-US') # nhan dien am thanh va luu vao bien you
        except:
            you = ""
        print("You: " + you)

        if you == "":
            robot_brain = "I can't hear you, try again"
        elif ("hello" in you) or ("hi" in you):
            robot_brain = "Hello Boss"
        elif ("introduce yourself" in you):
            robot_brain = "I'm Friday, i was born on Semtember 13, 2021. My biological father is Mr.Chung"
        elif ("how old are you" in you): 
            robot_brain = "I'm one year old"
        elif ("what is your name" in you):
            robot_brain = "I'm Friday"
        elif ("today"in you):
            today = date.today()
            robot_brain = today.strftime("%B ,%d, %Y")
        elif("what time" in you):
            now = datetime.now()
            robot_brain =  now.strftime("%H:%M:%S")
        elif ("bye" in you):		
            robot_brain = "bye bye Boss"
            robot_speak.say(robot_brain)
            robot_speak.runAndWait()
            break
 #................... device contro ....................
        elif ("turn on the light" in you):
            led_on()
            robot_brain = "yes sir, led on"
        elif ("turn off the light" in you):
            led_off()
            robot_brain = "yes sir, led off"
        elif ("turn on the fan" in you):
            fan_on()
            robot_brain = "yes sir, fan on"
        elif ("turn off the fan" in you):
            fan_off()
            robot_brain = "yes sir, fan off"

        else:
            robot_brain = "sorry, i don't understand"
        print("Robot: "+ robot_brain)
        robot_speak.say(robot_brain)
        robot_speak.runAndWait()


# tranning hinh anh nhan dien vs thu vien nhan dien khuan mat
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.read('E:/CODE/Python/Face_reconition/recognizer/tranningData.yml')

# truy cap vao databases va lay thong tin thong qua id 
def getProfile(id):
    conn = sqlite3.connect('E:/SQLite/Databases/face_data.db')
    query = "SELECT * FROM Face WHERE ID="+str(id)
    cursor = conn.execute(query)
    profile = None                  # bien profile de luu du lieu lay duoc tu databases ve

    for row in cursor:
        profile = row

    conn.close()
    return profile

# nhan dien khuan mat
def recogniz():
    cap = cv2.VideoCapture(0)
    fontface = cv2.FONT_HERSHEY_SIMPLEX
    cnt_id = 0
    
    while (True): 
        ret,frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray)
        global id
        for(x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
            roi_gray = gray[y: y+h, x: x+w] # cat anh
            id, confidence = recognizer.predict(roi_gray) # nhan dien duoc khuan mat dang co trong Webcam, tra ve id va do tin cay 
            if confidence < 60:             # do tin cay cang cao co nghia la cac buc anh cang it giong nhau, vi vay do tin cay cang thap thi cang tot 
                profile = getProfile(id)    # truyen id vao ham getProfile xem co trung voi id co trong databases khong
                if(profile != None):
                    cv2.putText(frame, ""+str(profile[1]), (x+10, y+h+30), fontface, 1, (0,255,0), 2)
            else:
                cv2.putText(frame, "Unknow", (x+10, y+h+30), fontface, 1, (0,0,255), 2)
                id = 0
        cv2.imshow('img',frame)
        cv2.waitKey(1)

        if(id == 1):
            id = 0
            cnt_id = cnt_id + 1
            if(cnt_id == 10):
                cnt_id = 0
                cap.release()
                cv2.destroyAllWindows()
                virtual()
        else:
            print('Not verify')


# recogniz()  

def input():
    OK2 = 0
    while True:
        robot_listen = speech_recognition.Recognizer()
        with speech_recognition.Microphone() as mic: 
        # mic = speech_recognition.Microphone()         
            robot_listen.adjust_for_ambient_noise(mic)
            print("Robot: I'm listening")
            start = time.time()
            audio = robot_listen.record(mic, duration=3) # audio = am thanh nghe duoc tu mic 
            print("Time listen : {}".format(time.time()-start))
            print("...")
        try:
            start1 = time.time()
            you = robot_listen.recognize_google(audio, language = 'en-US') # nhan dien am thanh va luu vao bien you
            print('Time to translate : {}'.format(time.time()-start1))
        except:
            you = ""
        print("You: " + you)

        if("Hello Friday" in you) or ("Hi Friday" in you) or ("Friday" in you):
            robot_brain = "verifying"
            print("Robot: "+robot_brain)
            robot_speak.say(robot_brain)
            robot_speak.runAndWait()
            OK2 = 1
            break
    if(OK2 == 1):
        recogniz() # goi ham nhan dien khuan mat

input()
