import math
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
from pathlib import Path
import cv2
import time
import numpy as np

def angle(a, b, c):
    d = np.arctan2(c[1] - b[1], c[0] - b[0])
    e = np.arctan2(a[1] - b[1], a[0] - b[0])
    angle_ = np.rad2deg(d - e)
    angle_ = angle_ + 360 if angle_ < 0 else angle_
    return 360 - angle_ if angle_ > 180 else angle_

def process(image, keypoints):
    nose_seen = keypoints[0][0] > 0 and keypoints[0][1] > 0
    left_ear_seen = keypoints[3][0] > 0 and keypoints[3][1] > 0
    right_ear_seen = keypoints[4][0] > 0 and keypoints[4][1] > 0
    left_shoulder = keypoints[5]
    right_shoulder = keypoints[6]
    right_elbow = keypoints[7]
    left_elbow = keypoints[8]
    right_fist = keypoints[9]
    left_fist = keypoints[10]

    try:
        if left_ear_seen and not right_ear_seen:
            angle_knee = angle(left_shoulder, left_elbow, left_fist)
        else:
            angle_knee = angle(right_shoulder, right_elbow, right_fist)

        x, y = int(left_elbow[0]), int(left_elbow[1])
        cv2.putText(image, f"{int(angle_knee)}", (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (25, 25, 255), 2)

        return angle_knee

    except ZeroDivisionError:
        pass

    return None

model_path = "yolo11n-pose.pt"
model = YOLO(model_path)

cap = cv2.VideoCapture(0)


last_time = time.time()
flag = False
count = 0
writer = cv2.VideoWriter("out.mp4", cv2.VideoWriter_fourcc(*"avc1"), 10, (640, 480))

angles = []

while cap.isOpened():
    ret, frame = cap.read()
    writer.write(frame)
    cur_time = time.time()
    cv2.putText(frame, f"FPS: {1 / (cur_time - last_time):.1f}", (10, 20), cv2.FONT_HERSHEY_PLAIN, 1.5, (25, 255, 25), 1)
    last_time = cur_time
    cv2.imshow('YOLO', frame)

    results = model(frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

    if not results:
        continue

    result = results[0]
    keypoints = result.keypoints.xy.tolist()
    if not keypoints:
        continue

    keypoints = keypoints[0]
    if not keypoints:
        continue

    annotator = Annotator(frame)
    annotator.kpts(result.keypoints.data[0], result.orig_shape, 5, True)
    annotated = annotator.result()

    angle_ = process(annotated, keypoints)

    print(angles)
    if len(angles) >= 5:
        angles.append(angle_)
        angles.pop(0)
        mean = sum(angles) / len(angles)

        if flag and mean >= 100:
            count += 1
            flag = False
        elif mean < 100:
            flag = True
    else:
        angles.append(angle_)



    cv2.putText(annotated, f"Count: {count}", (10, 50), cv2.FONT_HERSHEY_PLAIN, 1.5, (25, 255, 25), 1)
    cv2.imshow("Pose", annotated)

writer.release()
cap.release()
cv2.destroyAllWindows()
