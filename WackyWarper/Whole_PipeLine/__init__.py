from WackyWarper.Augmentor import Augmentor
from WackyWarper import helper_functions
import shutil

def Give_Me_Augmented_Data(IMG_DIR:dir, 
                           LABEL_DIR:dir, 
                           TRAIN_RATIO:float, 
                           VALID_RATIO:float,
                           AUGMENTED_HEADER_NAME:str, 
                           NUMBER_OF_IMAGES_NEEDED:int):
    
    helper_functions.Split_Dataset(IMG_DIR, LABEL_DIR, TRAIN_RATIO, VALID_RATIO)

    list_of_directory = ["Splitted/Train"]

    Augmentor.New_Start_Augmentor(list_of_directory, AUGMENTED_HEADER_NAME, NUMBER_OF_IMAGES_NEEDED)

    source_folder = ["Splitted/Valid","Splitted/Test"]
    for i in source_folder:
        shutil.move(i, AUGMENTED_HEADER_NAME)
    print(">>I Finished All the Process<<")
    