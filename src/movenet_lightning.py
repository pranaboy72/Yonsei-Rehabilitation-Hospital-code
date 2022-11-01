import tensorflow as tf
# import tensorflow_hub as hub
# from tensorflow_docs.vis import embed
import numpy as np
import cv2

# # Import matplotlib libraries
# from matplotlib import pyplot as plt
# from matplotlib.collections import LineCollection
# import matplotlib.patches as patches

# # Some modules to display an animation using imageio.
# import imageio
# from IPython.display import HTML, display


 # Initialize the TFLite interpreter
interpreter = tf.lite.Interpreter(model_path="/Users/jusuklee/Desktop/2022-2/movenet/lite-model_movenet_singlepose_thunder_3.tflite")
interpreter.allocate_tensors()


def draw_keypoints(frame, keypoints, confidence_threshold):
    y, x, c = frame.shape  # y coord, x coord, channel coordinates
    shaped = np.squeeze(
        np.multiply(keypoints, [y, x, 1]))  # multiply our frame shape를 해줘서 실제 좌표값 confidence는 transform 해주기 싫으니 1 곱하구

    for kp in shaped:
        ky, kx, kp_conf = kp
        if kp_conf > confidence_threshold:
            cv2.circle(frame, (int(kx), int(ky)), 4, (0, 255, 0), -1)

EDGES = {
    (0, 1): 'm',
    (0, 2): 'c',
    (1, 3): 'm',
    (2, 4): 'c',
    (0, 5): 'm',
    (0, 6): 'c',
    (5, 7): 'm',
    (7, 9): 'm',
    (6, 8): 'c',
    (8, 10): 'c',
    (5, 6): 'y',
    (5, 11): 'm',
    (6, 12): 'c',
    (11, 12): 'y',
    (11, 13): 'm',
    (13, 15): 'm',
    (12, 14): 'c',
    (14, 16): 'c'
}


def draw_connections(frame, keypoints, edges, confidence_threshold):
    y, x, c = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y, x, 1]))

    for edge, color in edges.items():
        p1, p2 = edge
        y1, x1, c1 = shaped[p1]
        y2, x2, c2 = shaped[p2]

        if (c1 > confidence_threshold) & (c2 > confidence_threshold):
            cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)


cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()

    # Reshape image
    img = frame.copy()
    img = tf.image.resize_with_pad(np.expand_dims(img, axis=0), 256, 256)
    input_image = tf.cast(img, dtype=tf.float32)

    # Setup input and output
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Make predictions
    interpreter.set_tensor(input_details[0]['index'], np.array(input_image))
    interpreter.invoke()
    keypoints_with_scores = interpreter.get_tensor(output_details[0]['index'])
    print(keypoints_with_scores)
    # Rendering
    draw_connections(frame, keypoints_with_scores, EDGES, 0.4)
    draw_keypoints(frame, keypoints_with_scores, 0.4)

    cv2.imshow('MoveNet Lightning', frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllwindows()
