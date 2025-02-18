import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

def load_training_data(data_dir, img_width, img_height):
    train_data = []
    responses = []
    for char_dir in os.listdir(data_dir):
        char_path = os.path.join(data_dir, char_dir)
        if not os.path.isdir(char_path):
            continue

        for img_file in os.listdir(char_path):
            img_path = os.path.join(char_path, img_file)

            img = cv2.imread(img_path)
            if img is None:
                continue

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
            resized = cv2.resize(thresh, (img_width, img_height), interpolation=cv2.INTER_AREA)
            flattened = resized.flatten()
            train_data.append(flattened)
            if len(char_dir) == 2:
                responses.append(ord(char_dir[1]))
            else:
                responses.append(ord(char_dir))

    return np.float32(train_data), np.array(responses, dtype=np.int32)


def train_knn(train_data, responses):
    knn = cv2.ml.KNearest_create()
    knn.train(train_data, cv2.ml.ROW_SAMPLE, responses)
    return knn


def search_i(check_list):
    delete_keys = []
    for i in range(1, len(check_list)):
        if abs(check_list[i - 1][0] - check_list[i][0]) < 15:
            delete_keys.append(i)

    while len(delete_keys) != 0:
        check_list[delete_keys[0] - 1] = (check_list[delete_keys[0] - 1][0],
                                          check_list[delete_keys[0] - 1][1],
                                          check_list[delete_keys[0] - 1][2],
                                          "i")
        del check_list[delete_keys[0]]
        delete_keys.pop(0)
        buffer = np.array(delete_keys)
        buffer = buffer - 1
        delete_keys = list(buffer)



    return check_list


def collect_word(recognized_text, check_img_width):
    final_text = ""

    for i in range(len(recognized_text)):
        final_text += recognized_text[i][-1]

        if i != len(recognized_text) - 1:
            if check_img_width / abs(recognized_text[i][2] - recognized_text[i + 1][0]) < 30:
                final_text += " "

    return final_text


def add_zero_border(img, border_width):
    height, width = img.shape[:2]

    new_array = np.zeros((height + 2 * border_width, width + 2 * border_width),
                         dtype=img.dtype)

    new_array[border_width:height + border_width, border_width:width + border_width] = img

    return new_array


def recognize_text(knn, image_path, img_width, img_height, k=3):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    recognized_text = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 10 and h > 10:
            roi = thresh[y:y + h, x:x + w]
            roi = add_zero_border(roi, 6)
            resized = cv2.resize(roi, (img_width, img_height), interpolation=cv2.INTER_AREA)
            flattened = resized.flatten()
            sample = np.float32(flattened)

            retval, results, neigh_resp, dists = knn.findNearest(sample.reshape(1, img_width * img_height), k)
            recognized_char = chr(int(results[0][0]))

            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            recognized_text.append((x, y, x + w, recognized_char))


    recognized_text = sorted(recognized_text)
    recognized_text = search_i(recognized_text)
    recognized_text = collect_word(recognized_text, img.shape[1])

    print(recognized_text)
    return recognized_text


k = 4
img_width = 200
img_height = 200
train_data, responses = load_training_data(r"./task/train", img_width, img_height)

knn = train_knn(train_data, responses)

recognize_text(knn, "task/0.png", img_width, img_height)
recognize_text(knn, "task/1.png", img_width, img_height)
recognize_text(knn, "task/2.png", img_width, img_height)
recognize_text(knn, "task/3.png", img_width, img_height)
recognize_text(knn, "task/4.png", img_width, img_height)
recognize_text(knn, "task/5.png", img_width, img_height)
recognize_text(knn, "task/6.png", img_width, img_height)

plt.show()