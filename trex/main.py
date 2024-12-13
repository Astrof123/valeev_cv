import mss
import numpy as np
import cv2
import matplotlib.pyplot as plt
import time
from skimage.measure import label, regionprops
import pyautogui


target_color = np.array([83, 83, 83])
time.sleep(1)
monitor = {"top": 200, "left": 200, "width": 1920, "height": 1080}
while True:
    # time.sleep(0.05)
    with mss.mss() as sct:

        # monitor = sct.monitors[0]
        sct_img = sct.grab(monitor)

        img = np.array(sct_img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        mask = np.all(img == target_color, axis=-1)

        binary_image = mask.astype(np.uint8) * 255
        binary_image = cv2.dilate(binary_image, None, iterations=2)

        labeled = label(binary_image)
        regions = regionprops(labeled)
        dino = max(regions, key=lambda region: region.area if 0.5 < (
                region.area / region.area_bbox) < 0.60 and region.area > 200 else 0)

        if dino == 0:
            exit()

        min_distance = float('inf')
        nearest_region = 0
        for i, region in enumerate(regions):
            if region == dino:
                continue
            elif region.area > 100 and region.centroid[1] - 30 > dino.centroid[1]:
                distance = np.linalg.norm(np.array(region.centroid) - np.array(dino.centroid))
                if distance < min_distance:
                    min_distance = distance
                    nearest_region = region

        # print(nearest_region)
        if nearest_region:
            jump_ration = 15
            wait = 0.03
            cactus_ratio = dino.area / nearest_region.area
            if 1.10 < cactus_ratio < 1.4:
                jump_ration = 44
                wait = 0.05
            elif 2 < cactus_ratio < 4:
                jump_ration = 37
                wait = 0.03
            elif 0.5 < cactus_ratio < 0.6:
                jump_ration = 60
                wait = 0.08
            elif cactus_ratio <= 0.50:
                jump_ration = 77
                wait = 0.09
            elif 0.6 < cactus_ratio < 0.9:
                jump_ration = 55
                wait = 0.08
            elif 1.00 < cactus_ratio < 1.11:
                jump_ration = 45
                wait = 0.06

            jump_distance = min_distance - jump_ration
            if jump_distance < 100:
                pyautogui.hotkey("space")
                time.sleep(wait)
                pyautogui.hotkey("down")