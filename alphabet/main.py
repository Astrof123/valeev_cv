import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops, euler_number
from collections import defaultdict
from pathlib import Path
from skimage.morphology import closing

def recognize(region):
    if region.image.mean() == 1.0:
        return "-"
    else: # B or 8
        image = closing(region.image.copy(), np.array([[1, 1], [1, 1]]))
        enumber = euler_number(image, 2)
        if enumber == -1:
            have_vl = np.sum(np.mean(region.image[:, :region.image.shape[1] // 2], 0) == 1) > 3

            if have_vl:
                return "B"
            else:
                return "8"

        elif enumber == 0: # A or 0 or D or P
            image = region.image.copy()
            image[-1, :] = 1
            enumber = euler_number(image)

            if enumber == -1:
                return "A"
            else:
                if 0.40 <= region.eccentricity <= 0.60:
                    return "D"
                elif 0.68 <= region.eccentricity <= 0.75:
                    return "P"
                elif 0.60 < region.eccentricity < 0.68:
                    return "0"

                return "@"

        else: # /, W, X, *, 1
            have_vl = np.sum(np.mean(region.image, 0) == 1) > 3

            if have_vl:
                return "1"
            else:
                if region.eccentricity < 0.45:
                    return "*"
                else:
                    image = region.image.copy()
                    image[0, :] = 1
                    image[-1, :] = 1
                    image[:, 0] = 1
                    image[:, -1] = 1
                    enumber = euler_number(image)

                    if enumber == -1:
                        return "/"
                    elif enumber == -3:
                        return "X"
                    else:
                        return "W"
    return "@"


image = plt.imread('symbols.png')[:, :, :3].mean(2)
image[image > 0] = 1
labeled = label(image)
regions = regionprops(labeled)

result = defaultdict(lambda: 0)
# path = Path('images')
# path.mkdir(exist_ok=True)

for i, region in enumerate(regions):
    symbol = recognize(region)
    result[symbol] += 1
    # print(f"{i}) {symbol}")
    # plt.cla()
    # plt.title(f"Symbol - {symbol}")
    # plt.imshow(region.image)
    # plt.savefig(path/ f"image_{i:03d}.png")

print(result)
