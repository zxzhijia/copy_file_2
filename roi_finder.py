import cv2
import numpy as np

import cv2
import numpy as np
import matplotlib.pyplot as plt

def select_roi(image_path):
    # Read the image with OpenCV
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Use Matplotlib to visualize the image and select the ROI
    fig, ax = plt.subplots(1)
    ax.imshow(img_rgb)

    roi = plt.ginput(2)  # User selects two points (top-left and bottom-right)
    plt.close()

    # Convert the selected ROI coordinates to integer format
    roi_coords = [(int(roi[0][0]), int(roi[0][1])), (int(roi[1][0]), int(roi[1][1]))]
    cropped_roi = img[roi_coords[0][1]:roi_coords[1][1], roi_coords[0][0]:roi_coords[1][0]]

    return img, cropped_roi

def find_similar_rois(img, cropped_roi):
    # Match the ROI throughout the image
    result = cv2.matchTemplate(img, cropped_roi, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8  # Adjust this threshold as needed
    loc = np.where(result >= threshold)

    for pt in zip(*loc[::-1]):
        cv2.rectangle(img, pt, (pt[0] + cropped_roi.shape[1], pt[1] + cropped_roi.shape[0]), (0, 0, 255), 2)

    cv2.imshow('Detected ROIs', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    image_path = "path_to_your_image.jpg"
    img, cropped_roi = select_roi(image_path)
    find_similar_rois(img, cropped_roi)
