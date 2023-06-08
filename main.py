from WackyWarper import Whole_PipeLine 

header_directory_name = "New_Augmented_Data" # just some name
Number_Of_Images_Needed = 1 # images per each


Whole_PipeLine.Give_Me_Augmented_Data(
                                    IMG_DIR = "data/images/",
                                    LABEL_DIR = "data/labels/",
                                    TRAIN_RATIO = 0.80,
                                    VALID_RATIO = 0.15,
                                    AUGMENTED_HEADER_NAME = header_directory_name,
                                    NUMBER_OF_IMAGES_NEEDED = Number_Of_Images_Needed
                                    )



