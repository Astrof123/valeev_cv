import zmq
import cv2
import numpy as np
import matplotlib.pyplot as plt

def on_mouse_callback(event, x, y, *params):
    global position
    if event == cv2.EVENT_LBUTTONDOWN:
        position = [y, x]


context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"")
port = 5555
socket.connect(f"tcp://192.168.0.100:{port}")

window_name = "client"
cv2.namedWindow(window_name, cv2.WINDOW_GUI_NORMAL)
cv2.setMouseCallback(window_name, on_mouse_callback)

flimit = 100
slimit = 200


def fupdate(value):
    global flimit
    flimit = value

def supdate(value):
    global slimit
    slimit = value



lower = (0, 70, 120)
upper = (255, 255, 255)

while True:
    msg = socket.recv()
    frame = cv2.imdecode(np.frombuffer(msg, np.uint8), -1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    thresh = cv2.bitwise_and(frame, frame, mask=mask)

    gray = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)


    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    count_cube = 0
    count_all = 0
    for i, contour in enumerate(contours):
        if cv2.contourArea((contour)) > 3000:
            (x, y), rad = cv2.minEnclosingCircle(contour)
            center = int(x), int(y)
            rad = int(rad)
            cv2.circle(frame, center, rad, (0, 255, 0), 2)

            circle_area = np.pi * (rad ** 2)

            _, (w, h), _ = cv2.minAreaRect(contour)


            if cv2.contourArea((contour)) / (w*h) > 0.8:
                count_cube += 1

            # if cv2.contourArea((contour)) / circle_area < 0.75:
            #     count_cube += 1

            count_all += 1

    cv2.putText(frame, f"Count objects: {count_all}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.putText(frame, f"Count sphere: {count_all - count_cube}", (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.putText(frame, f"Count cubes: {count_cube}", (10, 170),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    key = cv2.waitKey(100)
    if key == ord('q'):
        break

    cv2.imshow(window_name, frame)
    # cv2.imshow("Mask", contours)

cv2.destroyAllWindows()
