import numpy as np
import os
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops

def get_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

directory = "./out/"
files = os.listdir(directory)

files = sorted(files, key=lambda x: int(x.split('_')[1].split('.')[0]))

trajectory = []
for i, file in enumerate(files):
    image = np.load(directory + file)

    labeled = label(image)
    regions = regionprops(labeled)

    if i == 0:
        trajectory.append([regions[0].centroid, regions[1].centroid, regions[2].centroid])
    else:
        trajectory.append([0, 0, 0])
        for region in regions:
            minimum_distance = 10000000
            minumum_index = 0
            for j in range(3):
                if trajectory[i][j] != 0:
                    continue

                distance = get_distance(trajectory[i - 1][j], region.centroid)
                if distance < minimum_distance:
                    minimum_distance = distance
                    minumum_index = j

            trajectory[i][minumum_index] = region.centroid


trajectory = np.array(trajectory)

plt.xlabel('x')
plt.ylabel('y')
plt.plot(trajectory[:, 0, 0], trajectory[:, 0, 1], label='Линия кружочка №1')
plt.plot(trajectory[:, 1, 0], trajectory[:, 1, 1], '--', label='Линия кружочка №2')
plt.plot(trajectory[:, 2, 0], trajectory[:, 2, 1], '--', label='Линия кружочка №3')
plt.legend()
plt.show()
