import os
import cv2,shutil
from WackyWarper.config import albumentation_custom as alb_c

def Start_Augmentor(list_of_directory:list, header_folder_name:str,images_needed:int):
    '''
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    list_of_directory-> list of directory your images and labels are located 
    eg: ['train','valid','test'] or just only ['train']
    the folder structure needs to be like this.
    (YOU HAVE TO CREATE IT AND PUT THE IMAGES AND LABELS ACCORDING TO THIS STRUCTURE!):
    train->images
         ->labels
    valid->images
         ->labels
    test->images
        ->labels
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    header_folder-> this is what your folder is going to be called
    eg: "Augmented_Images" the structure would be like this after created
    (AUTOMATICALLY CREATED FOR YOU!)
        Augmented_Images
                    train
                        images
                            augmented_images......
                        labels
                            augmented_labels.....
                    and for valid and test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    images_needed-> How many augmented_images do you need per image
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    '''
    print(">>Augmentation started<<")
    folder_name = header_folder_name
    for partition in list_of_directory:
        for image in os.listdir(os.path.join(partition, 'images')):
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
                    coords = label[1:5]
                    coords_list.append(coords)
            for x in range(images_needed):
                try:
                    if coords_list:
                        augmented = alb_c.augmentor(image=img, bboxes=coords_list, class_labels=['face'] * len(coords_list))
                    else:
                        augmented = alb_c.augmentor_without_boudingbox(image=img)
                    partitionl = partition.split("/")[1]    
                    directory_path = os.path.join(folder_name, partitionl, 'images')
                    os.makedirs(directory_path, exist_ok=True)
                    # Copy the original image to the augmented folder
                    original_image_path = os.path.join(partition, 'images', image)
                    new_image_path = os.path.join(folder_name, partitionl, 'images', f'{image.split(".")[0]}.jpg')
                    shutil.copyfile(original_image_path, new_image_path)

                    directory_path_labels = os.path.join(folder_name, partitionl, 'labels')
                    os.makedirs(directory_path_labels, exist_ok=True)

                    # Move the original label file to the augmented label folder
                    original_label_path = os.path.join(partition, 'labels', f'{image.split(".")[0]}.txt')
                    new_label_path = os.path.join(folder_name, partitionl, 'labels', f'{image.split(".")[0]}.txt')
                    shutil.copyfile(original_label_path, new_label_path)

                    cv2.imwrite(os.path.join(folder_name, partitionl, 'images', f'{image.split(".")[0]}.{x}.jpg'), augmented['image'])
                    annotation = []
                    if os.path.exists(label_path):
                        for i in range(len(coords_list)):
                            if i < len(augmented['bboxes']):
                                annotation.append(class_value[i])
                                annotation.extend(augmented['bboxes'][i])
                            else:
                                annotation.append(0)
                                annotation.extend([0, 0, 0, 0])
                    else:
                        annotation.append(0)
                        annotation.append(0)
                        annotation.append(0)
                        annotation.append(0)
                        annotation.append(0)

                    with open(os.path.join(folder_name, partitionl, 'labels', f'{image.split(".")[0]}.{x}.txt'), 'w') as f:
                        f.write('\n'.join(' '.join(map(str, annotation[i:i+5])) for i in range(0, len(annotation), 5)))
                except:
                    continue
    print(">>Augmentation Ended<<")