import cv2
import numpy as np

def select_roi(image_path):
    # Read the image
    img = cv2.imread(image_path)
    img_copy = img.copy()

    # Resize the image for easier selection (4 times larger)
    img_resized = cv2.resize(img, (img.shape[1]*4, img.shape[0]*4))

    # Let the user select the ROI on the resized image
    roi_resized = cv2.selectROI("Select ROI", img_resized, False, False)
    cv2.destroyAllWindows()

    # Convert the ROI coordinates back to the original image size
    roi = (roi_resized[0]//4, roi_resized[1]//4, roi_resized[2]//4, roi_resized[3]//4)

    # Crop the selected ROI from the original image
    cropped_roi = img_copy[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]

    return img, cropped_roi

def find_similar_rois(img, cropped_roi):
    # Match the ROI throughout the image
    result = cv2.matchTemplate(img, cropped_roi, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8  # You can adjust this threshold as needed
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
