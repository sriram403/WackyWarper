from WackyWarper.Augmentor import Augmentor
from WackyWarper import helper_functions

list_of_directory = ["test"]
header_directory_name = "New_Augmented_Image"
Number_Of_Images_Needed = 1 # images per each

image_chosen = "a4_16.0"
image_to_look = f"ImageData/train/images/{image_chosen}.jpg" # give the image file path to visualize
label_for_that = f"ImageData/train/labels/{image_chosen}.txt" # give the label file path corresponding to the image

if __name__ == "__main__":
    Augmentor.Start_Augmentor(list_of_directory, header_directory_name, Number_Of_Images_Needed)
    # helper_functions.Visualize(image_to_look,label_for_that) # to visualize the image
    pass