import cv2
import os
import random
import shutil

def Visualize(image_path,label_path):
    
    '''
    ONLY ONE IMAGE PATH AND LABEL PATH!
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    image_path-> needs to be a image file path
    for eg:
    "A:augmentor\Image_Augmentor_YOLO\helper_functions\elon_musk.jpg"
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    label_path-> needs to be your yolo label path
    for eg:
    "A:augmentor\Image_Augmentor_YOLO\helper_functions\elon_musk.txt"
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    '''
    image = cv2.imread(image_path)
    # Resize image for display
    scale_percent = 50  # Adjust the value as needed
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    image = cv2.resize(image, (width, height))
    label_path = label_path.replace("/","\\")
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

        # Draw bounding box rectangle
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

        # Display class label
        class_label = f"{class_id}"
        cv2.putText(image, class_label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)

    # Display the image with bounding box annotations
    cv2.imshow("Image with Bounding Boxes", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def Split_Dataset(image_dir, label_dir, train_ratio,  valid_ratio):

    '''
    image_dir-> Your image directory
    
    label_dir-> Your label directory
    
    train_ratio-> training data ratio like eg:(.80)
    
    valid_ratio-> validation data ratio like eg:(.15)
    
    test_ratio -> (automatically done for you!)

    output:
    You would just get a folder of Train, Valid, Test 
    which contains subfolders of images, labels
    '''
    print(">>Data Split Started<<")
    # Create directories for train, test, and validation sets
    train_dir = "Splitted/Train"
    valid_dir = "Splitted/Valid"
    test_dir = "Splitted/Test"

    if os.path.exists(train_dir):
        shutil.rmtree(train_dir)
        shutil.rmtree(valid_dir)
        shutil.rmtree(test_dir)
    
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)
    os.makedirs(valid_dir, exist_ok=True)

    # Get a list of all image file names with the .jpg extension in the image directory
    image_files = [f for f in os.listdir(image_dir)]

    # Shuffle the list of image files randomly
    image_file = random.sample(image_files,len(image_files))

    # Calculate the number of images for each split based on the ratios
    total_images = len(image_file)
    train_split = int(total_images * train_ratio)
    valid_split = int(total_images * valid_ratio)

    # Move images to the respective split directories
    random.shuffle(image_file)
    for i, img_fle in enumerate(image_file):
        if i < train_split:
            split_dir = train_dir
        elif i < train_split + valid_split:
            split_dir = valid_dir
        else:
            split_dir = test_dir

        # Copy the image file to the split directory
        image_src = os.path.join(image_dir, img_fle)
        image_dst = os.path.join(split_dir, "images", img_fle)
        os.makedirs(os.path.dirname(image_dst), exist_ok=True)
        shutil.copy(image_src, image_dst)

        # Get the corresponding label file
        label_prefix = os.path.splitext(img_fle)[0]
        label_file = label_prefix + ".txt"

        # Copy the label file to the split directory
        label_src = os.path.join(label_dir, label_file)
        label_dst = os.path.join(split_dir, "labels", label_file)
        os.makedirs(os.path.dirname(label_dst), exist_ok=True)
        shutil.copy(label_src, label_dst)

    print(">>Dataset split completed successfully.<<")

# Under construction...
# def Rename_Files(Image_Dir_List,Label_Dir_List,New_Name):
#     '''
#     Image_Dir_List-> Your Image directory
#     Label_Dir_List-> Your Label directory
#     New_Name-> What your files to be renamed after
#     '''
#     folder_images_path = Image_Dir_List
#     folder_label_path = Label_Dir_List
#     Give_Me_Name = New_Name

#     for dir in folder_images_path:
#         file_list = os.listdir(dir)

#         for i, filename in enumerate(file_list):
#             new_filename = f"{Give_Me_Name}{i+1}.jpg"
#             old_filepath = os.path.join(dir, filename)
#             new_filepath = os.path.join(dir, new_filename)
#             os.rename(old_filepath, new_filepath)
            
#             print(f"Renamed {filename} to {new_filename}")
#     for dir in folder_label_path:
#         file_list = os.listdir(dir)

#         for i,filename in enumerate(file_list):
#             new_filename = f"{Give_Me_Name}{i+1}.txt"
#             old_filepath = os.path.join(dir,filename)
#             new_filepath = os.path.join(dir,new_filename)
#             os.rename(old_filepath,new_filepath)

#             print(f"Renamed {filename} to {new_filename}")