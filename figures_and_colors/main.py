import matplotlib.pyplot as plt
from skimage.filters import threshold_otsu, sobel
from skimage.measure import label, regionprops
from skimage.segmentation import flood_fill
from skimage.color import rgb2hsv
import numpy as np

image = plt.imread('balls_and_rects.png')
binary = image.mean(2)
binary[binary > 0] = 1
binary = binary[0:400, 0:400]

labeled = label(binary)
regions = regionprops(labeled)

print("Всего фигур:", np.max(labeled))

im_hsv = rgb2hsv(image)

colors = []
figures_colors = {}

def compare(color, region):
    for val in figures_colors.keys():
        if val - 0.05 < color < val + 0.05:
            if region.area == region.area_bbox:
                if 'rectangles' in figures_colors[val]:
                    figures_colors[val]['rectangles'] += 1
                else:
                    figures_colors[val]['rectangles'] = 1
            else:
                if 'circles' in figures_colors[val]:
                    figures_colors[val]['circles'] += 1
                else:
                    figures_colors[val]['circles'] = 1

            return

    figures_colors[round(float(color), 2)] = {}
    if region.area == region.area_bbox:
        figures_colors[round(float(color), 2)]['rectangles'] = 1
    else:
        figures_colors[round(float(color), 2)]['circles'] = 1


for region in regions:
    cy, cx = region.centroid
    color = im_hsv[int(cy), int(cx)][0]
    colors.append(color)
    compare(color, region)


for color, figures in figures_colors.items():
    print(f"Оттенок hsv: {color}:")
    print(figures)
    print()

plt.figure()
plt.imshow(image[0:400, 0:400])
plt.show()