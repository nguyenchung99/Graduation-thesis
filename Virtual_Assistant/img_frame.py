import cv2
import numpy as np

# thu vien nhan dien khuan mat mac dinh trong openCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(0)
while (True):
    ret,frame = cap.read() # ret = true, neu truy cap webcam thanh cong
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # chuyen anh sang anh xam
# phat hien cac doi tuong co kich thuoc khac nhau trong hinh anh dau vao va tra ve duoi dang danh sach
    faces = face_cascade.detectMultiScale(gray)
# ve hinh vuong bao quanh khuan mat
    for(x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,225,0), 2)
        # frame: la hinh anh lay tu webcam
        # (x,y): toa do diem dau tien de ve len hinh vuong
        # (x+w, y+h): toa do tinh tien 
        # (0,0,225): la mau RGB
        # 2: do day cua hinh vuong 
    cv2.imshow('Detecting face', frame)
    if(cv2.waitKey(1) & 0xFF == ord('q')): # waiKey(1): khi ket thuc chuong trinh or an phim 'q' de thoat khoi chuwong trinh
        break
cap.release() # giai phong bo nho
cv2.destroyAllWindows() # huy giai phong bo nho

 