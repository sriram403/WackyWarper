import cv2
import os
import random
import shutil
from tqdm import tqdm
from sklearn.model_selection import train_test_split

def Visualize(image_path, label_path):
    '''
    ONLY ONE IMAGE PATH AND LABEL PATH!
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    image_path-> needs to be a image file path
    label_path-> needs to be your yolo label path
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    '''
    image = cv2.imread(image_path)
    scale_percent = 50
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    image = cv2.resize(image, (width, height))

    with open(label_path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        label = line.strip().split(" ")
        class_id = int(label[0])
        x_center = float(label[1]) * image.shape[1]
        y_center = float(label[2]) * image.shape[0]
        width = float(label[3]) * image.shape[1]
        height = float(label[4]) * image.shape[0]

        x_min = int(x_center - width / 2)
        y_min = int(y_center - height / 2)
        x_max = int(x_center + width / 2)
        y_max = int(y_center + height / 2)

        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
        cv2.putText(image, f"{class_id}", (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)

    cv2.imshow("Image with Bounding Boxes", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def Custom_Split_Dataset(image_dir, label_dir, train_ratio, valid_ratio):
    '''
    image_dir-> Your image directory
    label_dir-> Your label directory
    train_ratio-> training data ratio eg: 0.80
    valid_ratio-> validation data ratio eg: 0.20
    Remaining images (if any) go to Test.
    '''
    train_dir = os.path.join("Splitted", "Train")
    valid_dir = os.path.join("Splitted", "valid_test")
    test_dir  = os.path.join("Splitted", "Test")

    for d in [train_dir, valid_dir, test_dir]:
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d, exist_ok=True)

    image_files = os.listdir(image_dir)
    random.shuffle(image_files)

    total_images = len(image_files)
    train_split = int(total_images * train_ratio)
    valid_split = int(total_images * valid_ratio)

    for i, img_fle in enumerate(tqdm(image_files, desc="Splitting", unit="img")):
        if i < train_split:
            split_dir = train_dir
        elif i < train_split + valid_split:
            split_dir = valid_dir
        else:
            split_dir = test_dir

        image_src = os.path.join(image_dir, img_fle)
        image_dst = os.path.join(split_dir, "images", img_fle)
        os.makedirs(os.path.dirname(image_dst), exist_ok=True)
        shutil.copy(image_src, image_dst)

        label_file = os.path.splitext(img_fle)[0] + ".txt"
        label_path = os.path.join(label_dir, label_file)
        label_dst  = os.path.join(split_dir, "labels", label_file)
        os.makedirs(os.path.dirname(label_dst), exist_ok=True)
        if os.path.exists(label_path):
            shutil.copy(label_path, label_dst)


def SkLearn_Split_Dataset(image_dir, label_dir, valid_ratio, test_ratio):
    image_files = os.listdir(image_dir)

    for img in image_files:
        label_file = os.path.splitext(img)[0] + ".txt"
        label_path = os.path.join(label_dir, label_file)
        if not os.path.exists(label_path):
            with open(label_path, "w") as f:
                f.write("0 0 0 0 0")

    label_files = os.listdir(label_dir)

    X_train, X_valid, y_train, y_valid = train_test_split(image_files, label_files, test_size=valid_ratio, random_state=42)
    X_valid, X_test, y_valid, y_test   = train_test_split(X_valid, y_valid, test_size=test_ratio, random_state=42)

    for split_name, img_files, lbl_files in [("Train", X_train, y_train),
                                              ("valid_test", X_valid, y_valid),
                                              ("Test",   X_test,  y_test)]:
        split_dir = os.path.join("Splitted", split_name)

        if os.path.exists(split_dir):
            shutil.rmtree(split_dir)
        os.makedirs(split_dir, exist_ok=True)

        for img in tqdm(img_files, desc=f"Splitting {split_name} images", unit="img"):
            src = os.path.join(image_dir, img)
            dst = os.path.join(split_dir, "images", img)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy(src, dst)

        for lbl in tqdm(lbl_files, desc=f"Splitting {split_name} labels", unit="lbl"):
            src = os.path.join(label_dir, lbl)
            dst = os.path.join(split_dir, "labels", lbl)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy(src, dst)
