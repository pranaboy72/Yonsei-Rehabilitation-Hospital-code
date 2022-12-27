import cv2
import mediapipe as mp
import numpy as np
import winsound as ws

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def f_length(a, b):
    a = np.array(a)

    length = np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

    return length

def f_height(a):
    a = np.array(a)

    height = a[1]

    return height

def f_distance(a, b):  # shoulder, mouth
    a = np.array(a)  # Shoulder
    b = np.array(b)  # mouth

    distance = b[1] - a[1]
    # print(distance)

    return distance


def f_angle(a, b):  # shoulder, wrist #change a,b if the cam is caputring right of your body (default: left side)
    a = np.array(a)
    b = np.array(b)

    radians = np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = abs(radians * 180.0 / np.pi)
    # print(angle)
    if angle > 180.0:
        angle = 360 - angle

    return angle


def beepsound1():
    freq = 2000
    dur = 100
    ws.Beep(freq, dur)


def beepsound2():
    freq = 500
    dur = 100
    ws.Beep(freq, dur)


cap = cv2.VideoCapture(0)  # To use ivcam, use cv2.VideoCapture(1)

# Curl counter variables
counter = 0
i = 0
stage = None


## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        print(i)
        i += 1
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

            shoulder_l = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            shoulder_r = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            shoulder = [(shoulder_l[0]+shoulder_r[0])/2, (shoulder_l[1]+shoulder_r[1]) / 2]

            eye_l = [landmarks[mp_pose.PoseLandmark.LEFT_EYE.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_EYE.value].y]
            eye_r = [landmarks[mp_pose.PoseLandmark.RIGHT_EYE.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_EYE.value].y]
            eye = [(eye_l[0] + eye_r[0]) / 2, (eye_l[1] + eye_r[1]) / 2]

            # Calculate angle
            length_sho = abs(f_length(shoulder_l, shoulder_r))
            distance_sho_to_eye = abs(f_distance(shoulder, eye))
            height_sho = abs(f_height(shoulder))

            # Visualize angle
            # cv2.putText(image, str(distance),
            #                tuple(np.multiply(elbow, [640, 480]).astype(int)),
            #                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
            #                     )

            # Curl counter logic
            if distance_sho_to_eye / length_sho > 0.72:
                stage1 = "Okay"
            else:
                stage1 = "Up!!"
                print(beepsound1())
                counter += 1
                # print(counter)

            if height_sho / length_sho > 1.5:
                stage2 = "Okay"

            else:
                stage2 = "Up!!"
                print(beepsound2())
                counter += 1

        except:
            pass

        # Render curl counter
        # Setup status box
        cv2.rectangle(image, (0, 0), (225, 73), (245, 117, 16), -1)
        cv2.rectangle(image, (0, 73), (225, 155), (245, 117, 16), -1)

        # Rep data
        # cv2.putText(image, 'Posture', (15,12),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1,q cv2.LINE_AA)
        # cv2.putText(image, str(counter),
        #             (10,60),
        #             cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)

        # # Stage data
        cv2.putText(image, 'NECK', (10, 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, stage1,
                    (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(image, 'WAIST', (10, 85),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, stage2,
                    (10, 143),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                  )

        cv2.imshow('Mediapipe Feed', image)
        print(f"NECK: {distance_sho_to_eye / length_sho}")
        print(f"WAIST: {height_sho / length_sho}")

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
