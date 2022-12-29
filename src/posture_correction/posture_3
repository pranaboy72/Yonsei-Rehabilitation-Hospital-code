import cv2
import mediapipe as mp
import numpy as np
import winsound as ws
import matplotlib.pyplot as plt
from time import perf_counter

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
counter_neck = 0
counter_waist = 0
i = 0
count_posture_ref = 50
irr_height_ref = []
irr_distance_ref = []

stage = None
start_time = perf_counter()

graph_time = []
graph_neck = []
graph_waist = []

# Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        print(i)
        i += 1
        end_time = perf_counter()
        during_time = (end_time - start_time)
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
        stage1 = "okay"
        stage2 = "okay"
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

            if i < count_posture_ref:
                irr_height_ref.append(height_sho)
                irr_distance_ref.append(distance_sho_to_eye)

            height_ref = np.median(irr_height_ref)
            distance_ref = np.median(irr_distance_ref)

            # Visualize angle
            # cv2.putText(image, str(distance),
            #                tuple(np.multiply(elbow, [640, 480]).astype(int)),
            #                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
            #                     )

            check_neck = 0
            check_waist = 0

            print(f"NECK: {(distance_ref - distance_sho_to_eye) / length_sho}")
            print(f"WAIST: {(height_sho - height_ref) / length_sho}")

            # Curl counter logic
            if i < count_posture_ref:
                stage1 = "take the right posture.."
            else:
                if (distance_ref - distance_sho_to_eye) / length_sho < 0.05:
                    stage1 = "Okay"
                else:
                    stage1 = "Up!!"
                    print(beepsound1())
                    counter_neck += 1
                    check_neck = 2
                    # print(counter)

            if i < count_posture_ref:
                stage2 = "take the right posture.."
            else:
                if (height_sho - height_ref) / length_sho < 0.03:
                    stage2 = "Okay"
                # 왼쪽 위 끝점을 원점으로 생각 / height는 원점으로 부터 y축 방향의 거리

                else:
                    stage2 = "Up!!"
                    print(beepsound2())
                    counter_waist += 1
                    check_waist = 1

            graph_time.append(during_time)
            graph_neck.append(check_neck)
            graph_waist.append(check_waist)

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

        cv2.imshow('Posture Estimation', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            fig = plt.figure("Posture Analysis", figsize=(12, 4))
            plt.yticks([0, 1, 2], labels=["Correct", "Waist", "Neck"])
            plt.xlabel("Time[s]")
            plt.ylabel("Posture")
            plt.scatter(graph_time, graph_neck, color='red', alpha=0.3)
            plt.scatter(graph_time, graph_waist, color='blue', alpha=0.3)
            plt.show()
            break

    cap.release()
    cv2.destroyAllWindows()
