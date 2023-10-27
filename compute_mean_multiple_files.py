import cv2
import os
import pandas as pd
import numpy as np

def select_subarea(image_path):
    # Read the image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Resize the image for display only
    display_img = cv2.resize(img, (img.shape[1]*4, img.shape[0]*4))
    
    # Let the user select the subarea on the displayed image
    roi = cv2.selectROI("Select subarea", display_img, False, False)
    cv2.destroyAllWindows()

    # Convert the ROI coordinates back to the original image size
    roi = (roi[0]//4, roi[1]//4, roi[2]//4, roi[3]//4)

    # Crop the selected subarea from the original image
    cropped_roi = img[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]
    return roi, cropped_roi.mean()
  
def get_means_of_subareas_in_folder(folder_path, roi):
    means = {}

    for file_name in sorted(os.listdir(folder_path)):
        if file_name.endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
            image_path = os.path.join(folder_path, file_name)
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            
            cropped_roi = img[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]
            means[file_name] = cropped_roi.mean()

    return means

if __name__ == "__main__":
    src_directory = "."  # Current directory
    results = {}

    for folder_name in os.listdir(src_directory):
        folder_path = os.path.join(src_directory, folder_name)
        
        if os.path.isdir(folder_path):
            # Get the image in the folder with filename starting with "0_"
            first_image = next((file_name for file_name in os.listdir(folder_path) 
                                if file_name.startswith('0_') and file_name.endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp'))), None)
            
            if first_image:
                first_image_path = os.path.join(folder_path, first_image)
                
                roi, _ = select_subarea(first_image_path)
                means = get_means_of_subareas_in_folder(folder_path, roi)
                
                results[folder_name] = means

    # Convert results to pandas DataFrame and save to Excel
    df = pd.DataFrame(results).T  # Transpose so that folders are rows
    df.to_excel("results.xlsx")
