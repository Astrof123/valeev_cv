import numpy as np
import matplotlib.pyplot as plt

image = np.load("starsnpy.txt").astype("int")


def neighbours2(y, x):
    return (y, x - 1), (y - 1, x)


def exist(B, nbs):
    left, top = nbs

    if left[0] >= 0 and left[0] <= B.shape[0] and left[1] >= 0 and left[1] < B.shape[1]:
        if B[left] == 0:
            left = None
    else:
        left = None


    if top[0] >= 0 and top[0] <= B.shape[0] and top[1] >= 0 and top[1] < B.shape[1]:
        if B[top] == 0:
            top = None
    else:
        top = None

    return left, top

def find(label, linked):
    j = label
    while linked[j] != 0:
        j = linked[j]

    return j


def union(label1, label2, linked):
    j = find(label1, linked)
    k = find(label2, linked)

    if j != k:
        linked[k] = j


def two_pass(B):
    LB = np.zeros_like(B)
    linked = np.zeros(B.size // 2 + 1, dtype="uint")
    label = 1

    for y in range(LB.shape[0]):
        for x in range(LB.shape[1]):
            if B[y, x] != 0:
                nbs = neighbours2(y, x)
                existed = exist(B, nbs)
                if existed[0] is None and existed[1] is None:
                    m = label
                    label += 1
                else:
                    lbs = [LB[n] for n in existed if n is not None]
                    m = min(lbs)

                LB[y, x] = m

                for n in existed:
                    if n is not None:
                        lb = LB[n]
                        if lb != m:
                            union(m, lb, linked)


    for y in range(LB.shape[0]):
        for x in range(LB.shape[1]):
            if B[y, x] != 0:
                new_label = find(LB[y, x], linked)
                if new_label != LB[y, x]:
                    LB[y, x] = new_label

    uniques = np.unique(LB)[1:]

    for i, v in enumerate(uniques):
        LB[LB == v] = i + 1

    return LB


struct_star = [ [1, 0, 0, 0, 1],
                [0, 1, 0, 1, 0],
                [0, 0, 1, 0, 0],
                [0, 1, 0, 1, 0],
                [1, 0, 0, 0, 1]]

struct_star = np.array(struct_star)

struct_cross = [[0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [1, 1, 1, 1, 1],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0]]

struct_cross = np.array(struct_cross)


def special_erosion(B):

    result = np.zeros_like(B)

    for y in range(2, B.shape[0] - 2):
        for x in range(2, B.shape[1] - 2):
            sub = B[y-2:y+3, x-2:x+3]

            if np.all(sub == struct_star) or np.all(sub == struct_cross):
                result[y, x] = 1

    return result

colored_images = two_pass(special_erosion(image))

countParts = np.amax(colored_images)

print(countParts)

plt.subplot(121)
plt.imshow(image)

plt.subplot(122)
plt.imshow(colored_images)

plt.show()