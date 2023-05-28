import os
import cv2
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
                if coords_list:
                    augmented = alb_c.augmentor(image=img, bboxes=coords_list, class_labels=['face'] * len(coords_list))
                else:
                    augmented = alb_c.augmentor_without_boudingbox(image=img)
                directory_path = os.path.join(folder_name, partition, 'images')
                os.makedirs(directory_path, exist_ok=True)
                cv2.imwrite(os.path.join(folder_name, partition, 'images', f'{image.split(".")[0]}.{x}.jpg'),augmented['image'])
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
        
                directory_path_labels = os.path.join(folder_name, partition, 'labels')
                os.makedirs(directory_path_labels, exist_ok=True)
                with open(os.path.join(folder_name, partition, 'labels', f'{image.split(".")[0]}.{x}.txt'),'w') as f:
                    f.write('\n'.join(' '.join(map(str, annotation[i:i+5])) for i in range(0, len(annotation), 5)))
