from sqlite3.dbapi2 import Cursor
import cv2
import numpy as np
import sqlite3
import os

def insertorupdate(id, name):
    conn = sqlite3.connect('E:/SQLite/Databases/face_data.db')
# kiem tra xem id da ton tai chua, neu ton tai roi thi update, chua thi insert
    query = "SELECT * FROM Face WHERE ID=" + str(id) # query toi cac ban ghi thong qua id 
    cursor = conn.execute(query) # lay ra cac ban ghi 
    isRecordExist = 0 # kiem tra xem da co ID trong databses chua, neu co roi thi isRecorExist = 1
    for row in cursor: # duyet tung hang tren ban ghi
        isRecordExist = 1 # cu co ban ghi la chuyen isRecordExist = 1
    if(isRecordExist == 0): # neu bang 0 chung to la chua co ban ghi nao 
        query = "INSERT INTO Face(ID, Name) VALUES ("+str(id) +",'"+str(name)+"')"
    else: 
        query = "UPDATE Face SET Name = '"+str(name)+"' Where ID = "+str(id)
    conn.execute(query)
    conn.commit()
    conn.close()

# load lirbrary
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(0)

# insert to databases
id = input("Enter your ID: ")
name = input("Enter your Name: ")
insertorupdate(id, name)

sample_number = 0
while (True): 
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3,5)
    for(x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,225,0), 2)
        if not os.path.exists('dataSet'): # kiem tra xem da co folder dataSet hay chua
            os.mkdir('dataSet')           # neu chua tao folder dataSet
        sample_number +=1
        cv2.imwrite('dataSet/User.' +str(id)+'.' +str(sample_number)+'.jpg', gray[y: y+h, x: x+w])

    cv2.imshow('frame', frame)
    cv2.waitKey(1)

    if(sample_number == 200):
        break
cap.release()
cv2.destroyAllWindows()