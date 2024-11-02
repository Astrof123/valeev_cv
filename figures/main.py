import numpy as np
import matplotlib.pyplot as plt

image = np.load("ps.npy.txt").astype("int")

struct_c_bottom = [[1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1],
                   [1, 1, 0, 0, 1, 1],
                   [1, 1, 0, 0, 1, 1]]

struct_c_bottom = {"array": np.array(struct_c_bottom), "count": 0}

struct_c_right = {"array": np.rot90(struct_c_bottom["array"]), "count": 0}

struct_c_top = {"array": np.rot90(struct_c_right["array"]), "count": 0}

struct_c_left = {"array": np.rot90(struct_c_top["array"]), "count": 0}

struct_rect = {"array": np.ones_like(struct_c_bottom["array"]), "count": 0}

structs = [struct_c_bottom, struct_c_right, struct_c_top, struct_c_left, struct_rect]


def counting_figures(B, structs):
    for y in range(0, B.shape[0] - 6):
        print(y)
        for x in range(0, B.shape[1] - 6):
            if B[y, x] != 0:
                sub = B[y:y + 4, x:x + 6]
                sub2 = B[y:y + 6, x:x + 4]

                len_structs = len(structs)
                for i in range(len_structs):
                    if structs[i]["array"].shape[0] == 6:
                        if np.all(sub2 == structs[i]["array"]):
                            structs[i]["count"] += 1
                            break
                    elif structs[i]["array"].shape[0] == 4:
                        if np.all(sub == structs[i]["array"]):
                            structs[i]["count"] += 1
                            break


counting_figures(image, structs)

summ = 0
for struct in structs:
    summ += struct["count"]

    print("Фигура: ")
    print(struct["array"])
    print(f"Количество этих фигур {struct["count"]}")
    print()

print(f"Всего фигур на картинке: {summ}")

plt.imshow(image)

plt.show()
