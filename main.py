from WackyWarper import Whole_PipeLine 
from WackyWarper.Augmentor import Augmentor

header_directory_name = "Data" # just some name
Number_Of_Images_Needed = 1 # images per each

Whole_PipeLine.Give_Me_Augmented_Data(
                                    IMG_DIR = "train/images/",
                                    LABEL_DIR = "train/labels/",
                                    TRAIN_RATIO = 0.60,
                                    VALID_RATIO = 0.30,
                                    AUGMENTED_HEADER_NAME = header_directory_name,
                                    NUMBER_OF_IMAGES_NEEDED = Number_Of_Images_Needed
                                    )