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
# cv2.namedWindow(window_name, cv2.WINDOW_GUI_NORMAL)
# cv2.setMouseCallback(window_name, on_mouse_callback)

target_color = np.array([83, 83, 83])
time.sleep(1)
monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
first = True
start_time = time.time()
wait_coef = 1
jump_coef = 1
counter = 0

while True:

    with mss.mss() as sct:
        sct_img = sct.grab(monitor)
        img = np.array(sct_img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        mask = np.all(img == target_color, axis=-1)

        binary_image = mask.astype(np.uint8) * 255
        binary_image = cv2.dilate(binary_image, None, iterations=2)

        contours, _ = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        dino = None
        dino_area = 0
        dino_index = 0
        all_moments = []

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

        if first:
            monitor = {"top": dino_centroid[1] - 140, "left": dino_centroid[0] - 40, "width": 650, "height": 180}
            first = False

        min_distance = float('inf')
        nearest_contour = 0
        nearest_area = 0
        nearest_index = 0
        nearest_y = 0

        for i in range(len(contours)):
            if i == dino_index:
                continue

            if all_moments[i]['m00'] == 0:
                continue

            centroid = (int(all_moments[i]['m10'] / all_moments[i]['m00']), int(all_moments[i]['m01'] / all_moments[i]['m00']))
            area = cv2.contourArea((contours[i]))

            if area > 300 and centroid[0] - 30 > dino_centroid[0]:
                distance = np.linalg.norm(np.array(centroid) - np.array(dino_centroid))
                if distance < min_distance:
                    min_distance = distance
                    nearest_contour = contours[i]
                    nearest_area = area
                    nearest_index = i
                    nearest_y = centroid[1]

        end_time = time.time()
        if 5 < end_time - start_time < 6:
            start_time = time.time()
            wait_coef *= 0.95
            counter += 1
            if counter % 2 == 0:
                jump_coef *= 1.05
            # jump_coef *= 1.01


        afk = False
        # print(nearest_y)
        # cv2.drawContours(img, contours, dino_index, (0, 0, 255), 3)
        # cv2.drawContours(img, contours, nearest_index, (255, 0, 0), 3)
        if min_distance < 1000:
            jump_ration = 15
            wait = 0.02
            cactus_ratio = dino_area / nearest_area
            if 1.25 < cactus_ratio < 1.45:
                jump_ration = 15
                wait = 0.055
            elif 2 < cactus_ratio < 4:
                jump_ration = 10
                wait = 0.02
            elif 1.44 < cactus_ratio < 1.55:
                jump_ration = 15
                wait = 0.04

            elif 1.55 < cactus_ratio < 2:
                if 55 < nearest_y < 100:
                    afk = True
                    jump_ration = 60
                else:
                    jump_ration = 60

                wait = 0.1
            elif 0.5 < cactus_ratio < 0.6:
                jump_ration = 35
                wait = 0.09
            elif cactus_ratio <= 0.50:
                jump_ration = 50
                wait = 0.12
            elif 0.6 < cactus_ratio < 0.9:
                jump_ration = 30
                wait = 0.09
            elif 1.00 < cactus_ratio < 1.26:
                jump_ration = 15
                wait = 0.03

            jump_distance = min_distance - jump_ration * jump_coef
            if afk:
                continue
            if jump_distance < 85:
                pyautogui.hotkey("space")
                time.sleep(wait * wait_coef)
                pyautogui.hotkey("down")

            # print(wait_coef)

        # key = cv2.waitKey(10)

        # cv2.imshow(window_name, img)

# cv2.destroyAllWindows()
