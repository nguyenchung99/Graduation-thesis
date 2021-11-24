import cv2
import os 
import numpy as np
import sqlite3
from PIL import Image

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
cap = cv2.VideoCapture(0)
fontface = cv2.FONT_HERSHEY_SIMPLEX
cnt_id = 0
while (True): 
    ret,frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)
    for(x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
        roi_gray = gray[y: y+h, x: x+w] # cat anh
        id, confidence = recognizer.predict(roi_gray) # nhan dien duoc khuan mat dang co trong Webcam, tra ve id va do tin cay 
        if confidence < 50:             # do tin cay cang cao co nghia la cac buc anh cang it giong nhau, vi vay do tin cay cang thap thi cang tot 
            profile = getProfile(id)    # truyen id vao ham getProfile xem co trung voi id co trong databases khong
            if(profile != None):
                cv2.putText(frame, ""+str(profile[1]), (x+10, y+h+30), fontface, 1, (0,255,0), 2)
        else:
            cv2.putText(frame, "Unknow", (x+10, y+h+30), fontface, 1, (0,0,255), 2)
            id = 0
    print(id)
    cv2.imshow('img',frame)
    cv2.waitKey(1)
    if(id == 1):
        id = 0
        cnt_id = cnt_id + 1
        if(cnt_id == 10):
            cnt_id = 0
            break
    
cap.release()
cv2.destroyAllWindows()