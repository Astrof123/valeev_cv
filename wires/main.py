import numpy as np
from pathlib import Path

files = Path("./").glob("*.txt")
images = [np.load(str(path)).astype(int) for path in files]


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

def special_erosion(B, mark):
    struct = [[mark],
              [mark],
              [mark]]
    struct = np.array(struct)


    result = np.zeros_like(B)

    for y in range(0, B.shape[0]):
        for x in range(0, B.shape[1]):
            if B[y, x] == mark and B[y - 1, x] == mark and B[y + 1, x] == mark:
                sub = B[y-1:y+2, x]

                if np.all(sub == struct):
                    result[y, x] = mark

    return result


for image in images:

    colored_image = two_pass(image)

    countCabels = np.amax(colored_image)

    for i in range(1, countCabels + 1):
        print("Кабель:", i, ':')
        image_erosed = special_erosion(colored_image, i)
        countParts = np.amax(two_pass(image_erosed))

        if countParts == 1:
            print("Кабель цел")
        elif countParts == 0:
            print("Кабель аннигилирован")
        else:
            print(f"Разорван на {countParts} частей")

    print("------------------------------")