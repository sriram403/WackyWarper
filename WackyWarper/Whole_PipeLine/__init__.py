from WackyWarper.Augmentor import Augmentor
from WackyWarper import helper_functions

def Give_Me_Augmented_Data(IMG_DIR:dir, 
                           LABEL_DIR:dir, 
                           TRAIN_RATIO:float, 
                           VALID_RATIO:float,
                           AUGMENTED_HEADER_NAME:str, 
                           NUMBER_OF_IMAGES_NEEDED:int):
    
    helper_functions.Split_Dataset(IMG_DIR, LABEL_DIR, TRAIN_RATIO, VALID_RATIO)

    list_of_directory = ["Splitted/Train","Splitted/Valid","Splitted/Test"]

    Augmentor.Start_Augmentor(list_of_directory, AUGMENTED_HEADER_NAME, NUMBER_OF_IMAGES_NEEDED)
    