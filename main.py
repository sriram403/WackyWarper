from WackyWarper import Whole_PipeLine 

header_directory_name = "V16_dlt_Data" # just some name
Number_Of_Images_Needed = 1 # images per each

Whole_PipeLine.Give_Me_Augmented_Data(
    IMG_DIR="output/images/", LABEL_DIR="output/labels/",
    VALID_RATIO=0.20, TEST_RATIO=0.05,
    SKLEARN_SPLIT=False,
    AUGMENTED_HEADER_NAME=header_directory_name,
    NUMBER_OF_IMAGES_NEEDED=Number_Of_Images_Needed,
    SPLIT=True,
    AUGMENT=False
)
