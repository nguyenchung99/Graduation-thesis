import cv2
import numpy as np
import os
from PIL import Image

recognizer = cv2.face.LBPHFaceRecognizer_create() # thu vien defaut cua open CV cho nhan dien hinh anh
path = 'dataSet' # bien lay duong dan 

def getImageWithId(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)] # truy cap vao tat ca cac file trong folder dataSet

    # print(imagePaths)
    faces = []
    IDs = []
    for imagePath in imagePaths:
        faceImg = Image.open(imagePath).convert('L') # doi ve dung dinh dang de tranning
        faceNp = np.array(faceImg, 'uint8')          # lay ma tran diem anh 
        print(faceNp)
        Id = int(imagePath.split('\\')[1].split('.')[1])  # cat bo dau '/' va '.' de lay Id
        faces.append(faceNp) # add faceNp vao mang
        IDs.append(Id)       # add id vao mang
        cv2.imshow('tranning', faceNp)
        cv2.waitKey(10)
    return faces, IDs
getImageWithId(path)
faces, Ids = getImageWithId(path)
recognizer.train(faces, np.array(Ids))
if not os.path.exists('recognizer'):
    os.mkdir('recognizer')
recognizer.save('recognizer/tranningData.yml')
cv2.destroyAllWindows()