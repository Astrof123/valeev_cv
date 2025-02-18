import os

data_dir = "./task/train"


def duplicate_file(source_path, destination_path):
    with open(source_path, 'rb') as source_file:
        content = source_file.read()

    with open(destination_path, 'wb') as dest_file:
        dest_file.write(content)


for char_dir in os.listdir(data_dir):
    char_path = os.path.join(data_dir, char_dir)
    if not os.path.isdir(char_path):
        continue

    for img_file in os.listdir(char_path):
        img_path = os.path.join(char_path, img_file)
        duplicate_file(img_path, os.path.join(char_path, "10" + img_file))