from WackyWarper import Whole_PipeLine

header_directory_name = "V16_5_batch_ncatr2706_Data" # just some name
Number_Of_Images_Needed = 3 # images per each

Whole_PipeLine.Give_Me_Augmented_Data(
    IMG_DIR="/home/ubuntu/training/WackyWarper/nc_at_r_27_06/images", LABEL_DIR="/home/ubuntu/training/WackyWarper/nc_at_r_27_06/labels",
    OLD_IMG_DIR="/home/ubuntu/training/WackyWarper/old_training_data/images", OLD_LABEL_DIR="/home/ubuntu/training/WackyWarper/old_training_data/labels",
    VALID_RATIO=0.20, TEST_RATIO=0.05,
    SKLEARN_SPLIT=False,
    AUGMENTED_HEADER_NAME=header_directory_name,
    NUMBER_OF_IMAGES_NEEDED=Number_Of_Images_Needed,
    SPLIT=True,
    AUGMENT=True
)
