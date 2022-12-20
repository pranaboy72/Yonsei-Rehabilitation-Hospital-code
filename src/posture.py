import cv2
import mediapipe as mp
import numpy as np
import winsound as ws

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_neck(a,b): #shoulder, mouth
    a = np.array(a) # Shoulder
    b = np.array(b) # mouth

    distance = b[1]-a[1]
    #print(distance)
        
    return distance

def calculate_back(a,b):    #shoulder, wrist #change a,b if the cam is caputring right of your body (default: left side)
    a = np.array(a)
    b = np.array(b)

    radians = np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = abs(radians*180.0/np.pi)
    #print(angle)
    if angle > 180.0:
        angle = 360-angle

    return angle

def beepsound1():
    freq = 2000
    dur = 100
    ws.Beep(freq, dur)

def beepsound2():
    freq = 500
    dur = 100
    ws.Beep(freq, dur)

cap = cv2.VideoCapture(0)   #To use ivcam, use cv2.VideoCapture(1)

# Curl counter variables
counter = 0 
stage = None

## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        # Make detection
        results = pose.process(image)
    
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            
            # Get coordinates
            shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            mouth = [landmarks[mp_pose.PoseLandmark.MOUTH_LEFT.value].x, landmarks[mp_pose.PoseLandmark.MOUTH_LEFT.value].y]
            #elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

            # Calculate angle
            distance = abs(calculate_neck(shoulder, mouth))
            angle = abs(calculate_back(shoulder,wrist))
            
            # Visualize angle
            # cv2.putText(image, str(distance), 
            #                tuple(np.multiply(elbow, [640, 480]).astype(int)), 
            #                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
            #                     )
            
            # Curl counter logic
            if distance > 0.13:
                stage1 = "Okay"
            else:
                stage1 ="Up!!"
                print(beepsound1())
                counter +=1
                # print(counter)
            
            if angle < 85.0:
                stage2 = "Okay" 
                
            else:
                stage2 = "Up!!"
                print(beepsound2())
                counter+=1
                       
        except:
            pass
        
        # Render curl counter
        # Setup status box
        cv2.rectangle(image, (0,0), (225,73), (245,117,16), -1)
        cv2.rectangle(image, (0,73), (225,155), (245,117,16), -1)
        
        # Rep data
        # cv2.putText(image, 'Posture', (15,12), 
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1,q cv2.LINE_AA)
        # cv2.putText(image, str(counter), 
        #             (10,60), 
        #             cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        # # Stage data
        cv2.putText(image, 'HEAD', (10,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, stage1, 
                    (10,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        cv2.putText(image, 'BACK', (10,85), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, stage2, 
                    (10,143), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                 )               
        
        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
