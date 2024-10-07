import numpy as np
import matplotlib.pyplot as plt

def lerp(v0, v1, t):
    return (1 - t) * v0 + t * v1

size = 1000
image = np.zeros((size, size, 3), dtype="uint8")


assert image.shape[0] == image.shape[1]

color1 = [255, 128, 0]
color2 = [0, 128, 255]

for i, v in enumerate(np.linspace(0, 1, image.shape[0] * 2 - 1)):
    if i >= size:
        buf_i = size - 1
        j = i - buf_i
        border = j
    else:
        buf_i = i
        j = 0
        border = j

    r = lerp(color1[0], color2[0], v)
    g = lerp(color1[1], color2[1], v)
    b = lerp(color1[2], color2[2], v)

    image[buf_i, j, :] = [r, g, b]

    while buf_i != border:
        buf_i -= 1
        j += 1
        image[buf_i, j, :] = [r, g, b]


plt.figure(1)
plt.imshow(image)
plt.show()