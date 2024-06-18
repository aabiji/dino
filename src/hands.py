import cv2
import numpy as np
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks.python import vision, BaseOptions
import time

model_path = "assets/hand_landmarker.task"

base_options = BaseOptions(model_asset_path=model_path)
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=1)
detector = vision.HandLandmarker.create_from_options(options)

def render_hand_landmarks(hand_landmarks, image):
    annotated = np.copy(image)

    for i in range(len(hand_landmarks)):
        hand_landmark = hand_landmarks[i]

        proto_landmark = landmark_pb2.NormalizedLandmarkList()
        points = [landmark_pb2.NormalizedLandmark(x=point.x, y=point.y, z=point.z) for point in hand_landmark]
        proto_landmark.landmark.extend(points)

        mp.solutions.drawing_utils.draw_landmarks(
            annotated, proto_landmark, mp.solutions.hands.HAND_CONNECTIONS,
            mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
            mp.solutions.drawing_styles.get_default_hand_connections_style(),
        )

    return annotated

video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()

    mp_image = mp.Image(data=frame, image_format=mp.ImageFormat.SRGB)
    detection_result = detector.detect(mp_image)
    annotated = render_hand_landmarks(detection_result.hand_landmarks, frame)

    cv2.imshow("Hands", annotated)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(0.01)

video.release()
cv2.destroyAllWindows()