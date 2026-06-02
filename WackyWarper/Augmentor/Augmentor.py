import os
import cv2, shutil
from tqdm import tqdm
from WackyWarper.config import albumentation_custom as alb_c

def _clamp_yolo_bbox(bbox):
    x_c, y_c, w, h = bbox
    x_min = max(0.0, x_c - w / 2)
    y_min = max(0.0, y_c - h / 2)
    x_max = min(1.0, x_c + w / 2)
    y_max = min(1.0, y_c + h / 2)
    new_w = x_max - x_min
    new_h = y_max - y_min
    return [x_min + new_w / 2, y_min + new_h / 2, new_w, new_h]

def Start_Augmentor(list_of_directory:list, header_folder_name:str, images_needed:int):
    '''
    list_of_directory-> list of directories where images and labels are located
    header_folder_name-> output folder name
    images_needed-> how many augmented images per original image
    '''
    print(">>Augmentation started<<")
    folder_name = header_folder_name
    for partition in list_of_directory:
        images_path = os.path.join(partition, 'images')
        if not os.path.exists(images_path):
            continue
        image_list = os.listdir(images_path)
        for image in tqdm(image_list, desc=os.path.basename(partition), unit="img"):
            img = cv2.imread(os.path.join(partition, 'images', image))
            coords_list = []
            class_value = []
            label_path = os.path.join(partition, 'labels', f'{image.split(".")[0]}.txt')
            if os.path.exists(label_path):
                with open(label_path, 'r') as f:
                    content = f.readlines()
                for line in content:
                    label = [float(value) for value in line.strip().split(" ")]
                    class_value.append(int(label[0]))
                    coords_list.append(_clamp_yolo_bbox(label[1:5]))

            partitionl = os.path.basename(partition)

            for x in range(images_needed):
                try:
                    if coords_list:
                        augmented = alb_c.augmentor(image=img, bboxes=coords_list, class_labels=['face'] * len(coords_list))
                    else:
                        augmented = alb_c.augmentor_without_boudingbox(image=img)

                    images_dir = os.path.join(folder_name, partitionl, 'images')
                    os.makedirs(images_dir, exist_ok=True)

                    original_image_path = os.path.join(partition, 'images', image)
                    new_image_path = os.path.join(images_dir, f'{image.split(".")[0]}.jpg')
                    shutil.copyfile(original_image_path, new_image_path)

                    labels_dir = os.path.join(folder_name, partitionl, 'labels')
                    os.makedirs(labels_dir, exist_ok=True)

                    stem = image.split(".")[0]
                    if coords_list:
                        shutil.copyfile(
                            os.path.join(partition, 'labels', f'{stem}.txt'),
                            os.path.join(labels_dir, f'{stem}.txt')
                        )
                    else:
                        with open(os.path.join(labels_dir, f'{stem}.txt'), 'w') as f:
                            f.write("0 0 0 0 0")

                    cv2.imwrite(os.path.join(images_dir, f'{stem}.{x}.jpg'), augmented['image'])

                    annotation = []
                    if os.path.exists(label_path):
                        for i in range(len(coords_list)):
                            if i < len(augmented['bboxes']):
                                annotation.append(class_value[i])
                                annotation.extend(augmented['bboxes'][i])
                            else:
                                annotation.extend([0, 0, 0, 0, 0])
                    else:
                        annotation = [0, 0, 0, 0, 0]

                    with open(os.path.join(labels_dir, f'{stem}.{x}.txt'), 'w') as f:
                        f.write('\n'.join(' '.join(map(str, annotation[i:i+5])) for i in range(0, len(annotation), 5)))

                except Exception as e:
                    print(f"Skipped {image}: {e}")
                    continue
    print(">>Augmentation Ended<<")


def New_Start_Augmentor(list_of_directory:list, header_folder_name:str, images_needed:int):
    '''
    list_of_directory-> list of directories where images and labels are located
    header_folder_name-> output folder name
    images_needed-> how many augmented images per original image
    '''
    print(">>Augmentation started<<")
    folder_name = header_folder_name
    for partition in list_of_directory:
        images_path = os.path.join(partition, 'images')
        if not os.path.exists(images_path):
            continue
        image_list = os.listdir(images_path)
        for image in tqdm(image_list, desc=os.path.basename(partition), unit="img"):
            img = cv2.imread(os.path.join(partition, 'images', image))
            coords_list = []
            class_value = []
            label_path = os.path.join(partition, 'labels', f'{image.split(".")[0]}.txt')

            if os.path.exists(label_path):
                with open(label_path, 'r') as f:
                    content = f.readlines()
                for line in content:
                    label = [float(value) for value in line.strip().split(" ")]
                    class_value.append(int(label[0]))
                    coords_list.append(_clamp_yolo_bbox(label[1:5]))

            partitionl = os.path.basename(partition)

            for x in range(images_needed):
                try:
                    if coords_list:
                        augmented = alb_c.augmentor(image=img, bboxes=coords_list, class_labels=['face'] * len(coords_list))
                    else:
                        augmented = alb_c.augmentor_without_boudingbox(image=img)

                    images_dir = os.path.join(folder_name, partitionl, 'images')
                    os.makedirs(images_dir, exist_ok=True)

                    original_image_path = os.path.join(partition, 'images', image)
                    new_image_path = os.path.join(images_dir, f'{image.split(".")[0]}.jpg')
                    shutil.copyfile(original_image_path, new_image_path)

                    labels_dir = os.path.join(folder_name, partitionl, 'labels')
                    os.makedirs(labels_dir, exist_ok=True)

                    stem = image.split(".")[0]
                    if coords_list:
                        shutil.copyfile(
                            os.path.join(partition, 'labels', f'{stem}.txt'),
                            os.path.join(labels_dir, f'{stem}.txt')
                        )
                    else:
                        with open(os.path.join(labels_dir, f'{stem}.txt'), 'w') as f:
                            f.write("0 0 0 0 0")

                    cv2.imwrite(os.path.join(images_dir, f'{stem}.{x}.jpg'), augmented['image'])

                    annotation = []
                    if os.path.exists(label_path):
                        for i in range(len(coords_list)):
                            if i < len(augmented['bboxes']):
                                annotation.append(class_value[i])
                                annotation.extend(augmented['bboxes'][i])
                            else:
                                annotation.extend([0, 0, 0, 0, 0])
                    else:
                        annotation = [0, 0, 0, 0, 0]

                    with open(os.path.join(labels_dir, f'{stem}.{x}.txt'), 'w') as f:
                        f.write('\n'.join(' '.join(map(str, annotation[i:i+5])) for i in range(0, len(annotation), 5)))

                except Exception as e:
                    print(f"Skipped {image}: {e}")
                    continue
    print(">>Augmentation Ended<<")
