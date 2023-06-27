from WackyWarper import Whole_PipeLine 
from WackyWarper.Augmentor import Augmentor

header_directory_name = "Data" # just some name
Number_Of_Images_Needed = 1 # images per each

Whole_PipeLine.Give_Me_Augmented_Data(
                                    IMG_DIR = "i/",
                                    LABEL_DIR = "l/",
                                    VALID_RATIO = 0.20,# it will split from the train/original data 
                                    TEST_RATIO = 0.05, # it will split from the valid split
                                    SKLEARN_SPLIT=True,
                                    AUGMENTED_HEADER_NAME = header_directory_name,
                                    NUMBER_OF_IMAGES_NEEDED = Number_Of_Images_Needed
                                    )
