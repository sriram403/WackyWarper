from WackyWarper import Whole_PipeLine

header_directory_name = "V17_Data" # just some name
Number_Of_Images_Needed = 1 # images per each

old_and_new_mix = True # if True, old dirs below get mixed in with the new data before splitting

old_img_dir = "/home/ec2-user/Training_Model/Sachin/Actual_Training_Images" if old_and_new_mix else None
old_label_dir = "/home/ec2-user/Training_Model/Sachin/Actual_Training_Labels" if old_and_new_mix else None

Whole_PipeLine.Give_Me_Augmented_Data(
    IMG_DIR="output/images", LABEL_DIR="output/labels",
    VALID_RATIO=0.20, TEST_RATIO=0.00,
    SKLEARN_SPLIT=False,
    AUGMENTED_HEADER_NAME=header_directory_name,
    NUMBER_OF_IMAGES_NEEDED=Number_Of_Images_Needed,
    SPLIT=True,
    AUGMENT=True,
    OLD_IMG_DIR=old_img_dir, OLD_LABEL_DIR=old_label_dir,
)
