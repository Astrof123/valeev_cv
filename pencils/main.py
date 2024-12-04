import numpy as np
import os
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops

directory = "./images/"
files = os.listdir(directory)

count_pencils = 0
pencils = []

for i, file in enumerate(files):
    pencils.append(0)
    image = plt.imread(directory + file)
    binary = image.mean(2)
    binary[binary <= 110] = 1
    binary[binary > 110] = 0
    labeled = label(binary)
    regions = regionprops(labeled)

    for j, region in enumerate(regions):
        if region.area > 250000 and region.eccentricity > 0.97:
            count_pencils += 1
            pencils[i] += 1

    print(f"Кол-во карандашей на картинке {file}: {pencils[i]}")

print("Всего карандашей:", count_pencils)


