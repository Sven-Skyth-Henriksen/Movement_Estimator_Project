import cv2
import numpy as np
import time

from numpy.lib.function_base import angle
import PoseModule as pm

cap = cv2.VideoCapture('Video/Train/Curl/curl_3.mov')



detector = pm.poseDetector()
count = 0
direction = 0
pTime = 0

while True:
    success, img = cap.read()
    #img = cv2.resize(img, (1280, 720)) # resizing the video window
    #img = cv2.imread('Video/pic1.jpeg')
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    #print(lmList)
    if len(lmList) != 0:
        #Right Arm
        #angle = detector.findAngle(img, 12, 14,16)
        #Left Arm
        angle = detector.findAngle(img, 11, 13,15)
        per = np.interp(angle, (220, 290), (0, 100))
        bar = np.interp(angle, (230, 290), (800, 100))
        #print(angle, per)

        # check for the curls 
        if per == 100:
            if direction == 0:
                count += 0.5
                direction = 1
        if per == 0:
            if direction == 1:
                count += 0.5
                direction = 0
        print(count)
        
        # DRAW Progress bar
        cv2.rectangle(img, (900,100),(600,800),(255, 255, 0),3)
        cv2.rectangle(img, (900,int(bar)),(600,800),(255, 255, 0),cv2.FILLED)
        #cv2.putText(img, f'{int(per)} %' ', (650,900), cv2.FONT_HERSHEY_PLAIN, 4 , (255, 255, 0),4)


        #cv2.rectangle(img, (0,450),(250,720),(255, 255, 0),cv2.FILLED)
        #Show the curl counter
        cv2.putText(img, str(int(count)), (20,1200), cv2.FONT_HERSHEY_PLAIN, 10 , (255, 255, 0),15)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (50,100), cv2.FONT_HERSHEY_PLAIN, 5 , (255, 255, 0),5)


    cv2.imshow('Detector', img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    
    

    
    