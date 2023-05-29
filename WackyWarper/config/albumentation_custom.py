import albumentations as alb

'''
RandomCrop: 
Randomly crops the image and adjusts the bounding boxes accordingly. 
This can simulate varying camera perspectives and object scales.

HorizontalFlip/VerticalFlip: 
Flips the image horizontally or vertically, 
along with adjusting the bounding box coordinates. 
This augmentation can help increase the diversity of training data.

RandomBrightnessContrast: 
Adjusts the brightness and contrast of the image randomly. 
This augmentation can simulate varying lighting conditions.

Rotate: 
Rotates the image by a specified angle, 
adjusting the bounding boxes accordingly. 
This can be useful for scenarios where objects may appear at different orientations.

Blur: 
Applies blur to the image, 
which can be helpful in mimicking motion blur or other image distortions.

ColorJitter: 
Adjusts the brightness, 
contrast, and saturation of the image. 
This augmentation can simulate changes in lighting conditions.

RandomGamma: 
Applies gamma correction to the image by modifying pixel values based on a randomly chosen gamma parameter, 
allowing for brightness and contrast adjustments and simulating different lighting conditions.

RGBShift: Randomly shifts the color channels (red, green, and blue) of the image 
by adding a small random value to each channel's pixel intensity, 
introducing color variations and simulating changes in lighting conditions or color imbalances.
'''

W = 1000 # Crop_Width
H = 1000 # Crop_Height
HF = 0.5 # HorizontalFlip probability value
RBC = 0.2 # RandomBrightnessContrast probability value
LIMIT,VALUE_TO_ROTATE = 10,0.2 # Rotate maximum rotation angle, magnitude of rotation
B = 0.2 # Blur probability value
CJ_BRIGHTNESS,CJ_CONTRAST,CJ_SATURATION,CJ_VALUE = 0.2,0.2,0.2,0.2 # ColorJitter
RG = 0.2 # RandomGamma probability value
RGBS = 0.2 # RGBShift probability value
VF = 0.8 # VerticalFlip probability value

augmentor_without_boudingbox = alb.Compose([
        #     alb.RandomCrop(width=W, height=H), 
            alb.HorizontalFlip(p=HF),
            alb.RandomBrightnessContrast(p=RBC),
            alb.Rotate(limit=LIMIT, p=VALUE_TO_ROTATE),
            alb.Blur(p=B),
            alb.ColorJitter(brightness=CJ_BRIGHTNESS, contrast=CJ_CONTRAST, saturation=CJ_SATURATION, p=CJ_VALUE),
            alb.RandomGamma(p=RG), 
            alb.RGBShift(p=RGBS), 
            alb.VerticalFlip(p=VF)])

augmentor = alb.Compose([            
        #     alb.RandomCrop(width=W, height=H), 
            alb.HorizontalFlip(p=HF),
            alb.RandomBrightnessContrast(p=RBC),
            alb.Rotate(limit=LIMIT, p=VALUE_TO_ROTATE),
            alb.Blur(p=B),
            alb.ColorJitter(brightness=CJ_BRIGHTNESS, contrast=CJ_CONTRAST, saturation=CJ_SATURATION, p=CJ_VALUE),
            alb.RGBShift(p=RGBS), 
            alb.VerticalFlip(p=VF)], 
                    bbox_params=alb.BboxParams(format='yolo', 
                                                label_fields=['class_labels']))