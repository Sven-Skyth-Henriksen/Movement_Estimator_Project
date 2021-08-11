import cv2
import numpy as np 
import mediapipe as mp 
import time 


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

## Angle detection

def calcAngle(p1,p2,p3):
    a = np.array(p1) # Fist
    b = np.array(p2) # Mid
    c = np.array(p3) # End

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0/np.pi)

    if angle > 180.0:
        angle = 360 -angle
    
    return angle

cap = cv2.VideoCapture(0)

#Curl Counter variable
counter = 0
stage = None


## set mediapip instance: 
with mp_pose.Pose(min_detection_confidence=0.6, min_tracking_confidence=0.6) as pose:  ##confidence means how accurat the detection is but                                                                                             to high could mean no detection...
    while cap.isOpened():
        
        ret, frame = cap.read()

        #Recolor Image from BGR to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        #Make Detection
        results = pose.process(image)

        # Recolor Image from RGB back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        #Extract Landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            
            # Get coordinats
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            # Calc Angle
            angle = calcAngle(left_shoulder,left_elbow,left_wrist)

            #Progress bar
            bar = np.interp(angle, (30, 160), (160, 600))
            cv2.rectangle(image,(1100, 160),(1175,600),(7,85,175), 3)
            cv2.rectangle(image,(1100,int(bar)),(1175, 600),(7,85,175), cv2.FILLED)


            # Visualization angle
            cv2.putText(image, str(int(angle)), 
                        tuple(np.multiply(left_shoulder, [640,480]).astype(int))
                        ,cv2.FONT_HERSHEY_PLAIN, 5,(255,255,255), 2, cv2.LINE_AA
                        )
            
            #Triceps Counter Logic
            if angle > 30:
                stage = 'down'
            if angle < 160 and stage == 'down':
                stage='up'
                counter +=1
                #print(counter)


        except:
            pass

        #Render curl counter 
        #Setup status box
        cv2.rectangle(image,(0,0),(225,120),(7,85,175), cv2.FILLED)
        cv2.rectangle(image,(1400,0),(1000,120),(7,85,175), cv2.FILLED)
        cv2.rectangle(image,(0,1400),(225,50),(7,85,175), cv2.FILLED)

        # Lines (Design)
        cv2.line(image, (0,150),(225,150),(255,255,255),3)
        cv2.line(image, (0,300),(225,300),(255,255,255),3)

        #Rep data
        cv2.putText(image, 'REPS', (20,30), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter), (40,100), cv2.FONT_HERSHEY_PLAIN, 3, (255,255,255), 2, cv2.LINE_AA)

        #Stage data
        cv2.putText(image, 'Stage', (20, 200), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(image, str(stage), (20,250), cv2.FONT_HERSHEY_PLAIN, 3, (255,255,255), 2, cv2.LINE_AA)

        #Text
        cv2.putText(image, 'AI-Trainer', (45,650), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 2, cv2.LINE_AA)
        cv2.putText(image, 'Made by', (75,680), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(image, 'Sven Skyth Henriksen', (20,700), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(image, 'Exercise: ', (1050,30), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2, cv2.LINE_AA)
        cv2.putText(image, 'Biceps Curls', (1030,100), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2, cv2.LINE_AA)


        #Render Detections --> Showing landmarks and dots
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, 
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), #Giving the DOTS another color
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)  #Giving the LINES another color 
                                )

        cv2.imshow('Mediapipe Feed', image)
        

        if cv2.waitKey(10) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()