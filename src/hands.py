import cv2
import numpy as np
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks.python import vision, BaseOptions
import time

class Detector:
    def __init__(self):
        model_path = "assets/hand_landmarker.task"
        base_options = BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(base_options=base_options,
                                            running_mode=vision.RunningMode.LIVE_STREAM,
                                            result_callback=self.render_hand_landmarks)
        self.detector = vision.HandLandmarker.create_from_options(options)
        self.annotated_image = np.zeros((640,480,3), np.uint8)

    def render_hand_landmarks(self, detection_result, image, _):
        annotated = np.copy(image.numpy_view())
        hand_landmarks = detection_result.hand_landmarks

        for i in range(len(hand_landmarks)):
            hand_landmark = hand_landmarks[i]

            proto_landmark = landmark_pb2.NormalizedLandmarkList()
            points = [landmark_pb2.NormalizedLandmark(x=hl.x, y=hl.y, z=hl.z) for hl in hand_landmark]
            proto_landmark.landmark.extend(points)

            mp.solutions.drawing_utils.draw_landmarks(
                annotated, proto_landmark, mp.solutions.hands.HAND_CONNECTIONS,
                mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
                mp.solutions.drawing_styles.get_default_hand_connections_style(),
            )

        self.annotated_image = annotated

    def run(self):
        video = cv2.VideoCapture(0)

        while True:
            _, frame = video.read()

            timestamp = int(round(time.time() * 1000))
            mp_image = mp.Image(data=frame, image_format=mp.ImageFormat.SRGB)
            self.detector.detect_async(mp_image, timestamp)

            cv2.imshow("Hands", self.annotated_image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            time.sleep(0.01)

        video.release()
        cv2.destroyAllWindows()

Detector().run()