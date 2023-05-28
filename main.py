from WackyWarper.Augmentor import Augmentor
from WackyWarper import helper_functions

list_of_directory = ['Train']
header_directory_name = "Augmented_Image"
Number_Of_Images_Needed = 3

image_to_look = "" # give the image file path
label_for_that = "" # give the label file path corresponding to the image

if __name__ == "__main__":
    Augmentor.Start_Augmentor(list_of_directory, header_directory_name, Number_Of_Images_Needed)
    # helper_functions.Visualize(image_to_look,label_for_that) # to visualize the image
    pass