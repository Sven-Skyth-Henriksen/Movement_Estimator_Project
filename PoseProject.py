import cv2
import time
import PoseModule as pm

cap = cv2.VideoCapture('Video/vid2.mov')
pTime = 0
detector = pm.poseDetector()

while True:
    success, img = cap.read()
    img = detector.findPose(img)
    lmList = detector.findPosition(img)
    print(lmList)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (70, 60 ), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 235), 3)

    cv2.imshow('Image', img)
    cv2.waitKey(1)