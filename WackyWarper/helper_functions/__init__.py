import cv2

def Visualize(image_path,label_path):
    
    '''
    ONLY ONE IMAGE PATH AND LABEL PATH!
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    image_path-> needs to be a image file path
    for eg:
    "A:augmentor\Image_Augmentor_YOLO\helper_functions\elon_musk.jpg"
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    label_path-> needs to be your yolo label path
    for eg:
    "A:augmentor\Image_Augmentor_YOLO\helper_functions\elon_musk.txt"
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    '''

    image = cv2.imread(image_path)
    # Resize image for display
    scale_percent = 50  # Adjust the value as needed
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    image = cv2.resize(image, (width, height))

    with open(label_path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        label = line.strip().split(" ")
        class_id = int(label[0])
        x_center = float(label[1]) * image.shape[1]
        y_center = float(label[2]) * image.shape[0]
        width = float(label[3]) * image.shape[1]
        height = float(label[4]) * image.shape[0]

        x_min = int(x_center - width / 2)
        y_min = int(y_center - height / 2)
        x_max = int(x_center + width / 2)
        y_max = int(y_center + height / 2)

        # Draw bounding box rectangle
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

        # Display class label
        class_label = f"Class: {class_id}"
        cv2.putText(image, class_label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the image with bounding box annotations
    cv2.imshow("Image with Bounding Boxes", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()