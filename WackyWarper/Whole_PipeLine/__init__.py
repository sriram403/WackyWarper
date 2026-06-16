from WackyWarper.Augmentor import Augmentor
from WackyWarper import helper_functions
import shutil
import os

def check_and_fill_txt_file(file_path):
    if os.path.exists(file_path):
        if os.stat(file_path).st_size == 0:
            with open(file_path, 'w') as file:
                file.write("0 0 0 0 0")

def Give_Me_Augmented_Data(IMG_DIR:dir,
                           LABEL_DIR:dir,
                           VALID_RATIO:float,
                           AUGMENTED_HEADER_NAME:str,
                           NUMBER_OF_IMAGES_NEEDED:int,
                           SKLEARN_SPLIT:bool,
                           TRAIN_RATIO:float=0.8,
                           TEST_RATIO:float=0.05,
                           SPLIT:bool=True,
                           AUGMENT:bool=True):

    list_of_directory = [os.path.join("Splitted", "Train"),os.path.join("Splitted","valid_test")]

    if SPLIT:
        print(">>Data Split Started<<")
        if SKLEARN_SPLIT:
            helper_functions.SkLearn_Split_Dataset(IMG_DIR, LABEL_DIR, VALID_RATIO, TEST_RATIO)
        else:
            helper_functions.Custom_Split_Dataset(IMG_DIR, LABEL_DIR, TRAIN_RATIO, VALID_RATIO)
        print(">>Dataset split completed successfully.<<")

    if AUGMENT:
        Augmentor.New_Start_Augmentor(list_of_directory, AUGMENTED_HEADER_NAME, NUMBER_OF_IMAGES_NEEDED)

    print(">>I Finished All the Process<<")
    