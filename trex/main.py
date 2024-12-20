import mss
import numpy as np
import cv2
import matplotlib.pyplot as plt
import time
from skimage.measure import label, regionprops
import pyautogui

def on_mouse_callback(event, x, y, *params):
    global position
    if event == cv2.EVENT_LBUTTONDOWN:
        position = [y, x]

window_name = "client"
cv2.namedWindow(window_name, cv2.WINDOW_GUI_NORMAL)
cv2.setMouseCallback(window_name, on_mouse_callback)

target_color = np.array([83, 83, 83])
time.sleep(1)
monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
first = True
prev_time = time.time()
score = 0
speed_px=8
speed = 1
jump = True

dino = None
dino_area = 0
dino_index = 0

while True:
    with mss.mss() as sct:
        sct_img = sct.grab(monitor)
        img = np.array(sct_img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        mask = np.all(img == target_color, axis=-1)

        binary_image = mask.astype(np.uint8) * 255
        binary_image = cv2.dilate(binary_image, None, iterations=2)

        contours, _ = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        all_moments = []

        if first:
            for i, contour in enumerate(contours):
                area = cv2.contourArea((contour))
                all_moments.append(cv2.moments(contour))
                x, y, w, h = cv2.boundingRect(contour)
                if area > dino_area and area < 1500 and 0.45 < (area / w / h) < 0.55:
                    dino_area = area
                    dino = contour
                    dino_index = i

            if dino is None:
                break

            dino_moment = all_moments[dino_index]
            dino_centroid = (int(dino_moment['m10'] / dino_moment['m00']), int(dino_moment['m01'] / dino_moment['m00']))

            monitor = {"top": dino_centroid[1] - 140, "left": dino_centroid[0] - 40, "width": 650, "height": 180}
            dino_centroid = (40, 140)

            first = False
        else:
            for i, contour in enumerate(contours):
                all_moments.append(cv2.moments(contour))


        min_distance = float('inf')
        nearest_contour = 0
        nearest_area = 0
        nearest_index = 0
        nearest_y = 0
        nearest_x = 0

        for i in range(len(contours)):
            if all_moments[i]['m00'] == 0:
                continue

            centroid = (
            int(all_moments[i]['m10'] / all_moments[i]['m00']), int(all_moments[i]['m01'] / all_moments[i]['m00']))
            area = cv2.contourArea((contours[i]))
            if area > 300:
                distance = np.linalg.norm(np.array(centroid) - np.array(dino_centroid))

                if distance == 0:
                    continue

                if distance < min_distance and (centroid[0] - 10) - dino_centroid[0] > 0:
                    min_distance = distance
                    nearest_contour = contours[i]
                    nearest_area = area
                    nearest_index = i
                    nearest_y = centroid[1]
                    nearest_x = centroid[0]

        if nearest_x == 0:
            continue

        afk = False
        # cv2.circle(img, (nearest_x, nearest_y), 5, (255, 0, 0), 2)
        # cv2.circle(img, (dino_centroid[0], dino_centroid[1]), 5, (0, 0, 255), 2)

        score += (time.time() - prev_time) * speed_px * speed  # Формула величайшего Демида
        prev_time = time.time()

        if score < 1000:
            speed = (speed_px + 0.5 * (score // 100)) / 8
        else:
            speed = (speed_px + (5 + 0.5 * ((score - 1000) // 200))) / 8

        # print("Min_distance:", min_distance)
        if min_distance < 1000:
            jump_ration = 15
            wait = 0.1
            cactus_ratio = dino_area / nearest_area
            if 1.25 < cactus_ratio < 1.45:
                jump_ration = 15
                wait = 0.15
            elif 2 < cactus_ratio < 4:
                jump_ration = 10
                wait = 0.1
            elif 1.44 < cactus_ratio < 1.55:
                jump_ration = 15
                wait = 0.1

            elif 1.55 < cactus_ratio < 2:
                if 55 < nearest_y < 100:
                    afk = True
                    jump_ration = 40
                else:
                    jump_ration = 40

                wait = 0.14
            elif 0.5 < cactus_ratio < 0.6:
                jump_ration = 35
                wait = 0.18
            elif cactus_ratio <= 0.50:
                jump_ration = 50
                wait = 0.18
            elif 0.6 < cactus_ratio < 0.9:
                jump_ration = 30
                wait = 0.15
            elif 1.00 < cactus_ratio < 1.26:
                jump_ration = 15
                wait = 0.1

            if afk:
                continue

            if (min_distance - jump_ration) < 85 * speed:
                pyautogui.hotkey("space")
                time.sleep(wait)
                pyautogui.keyDown("down")
                pyautogui.keyUp("down")


        # cv2.imshow(window_name, img)

    # key = cv2.waitKey(10)

# cv2.destroyAllWindows()
