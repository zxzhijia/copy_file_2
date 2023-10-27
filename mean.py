import cv2
import numpy as np

def align_images(base_img_path, align_img_path, save_path):
    # Read the images in grayscale mode
    base_img = cv2.imread(base_img_path, cv2.IMREAD_GRAYSCALE)
    align_img = cv2.imread(align_img_path, cv2.IMREAD_GRAYSCALE)
    
    # Ensure both images are of the same size
    if base_img.shape != align_img.shape:
        raise ValueError("Both images should have the same dimensions.")
    
    # Compute the correlation coefficient match of the two images
    result = cv2.matchTemplate(base_img, align_img, cv2.TM_CCORR_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    # Compute the x and y shift from the peak correlation
    y_shift, x_shift = max_loc

    # Translate the align_img to align it to base_img
    transformation_matrix = np.float32([[1, 0, x_shift], [0, 1, y_shift]])
    aligned_img = cv2.warpAffine(align_img, transformation_matrix, align_img.shape[::-1])

    # Crop the aligned image to get the common overlapping area
    y1, y2 = max(-y_shift, 0), min(base_img.shape[0] - y_shift, base_img.shape[0])
    x1, x2 = max(-x_shift, 0), min(base_img.shape[1] - x_shift, base_img.shape[1])

    cropped_base_img = base_img[y1:y2, x1:x2]
    cropped_aligned_img = aligned_img[y1 + y_shift:y2 + y_shift, x1 + x_shift:x2 + x_shift]

    # Save the cropped images
    cv2.imwrite(save_path + '_base_aligned.jpg', cropped_base_img)
    cv2.imwrite(save_path + '_align_aligned.jpg', cropped_aligned_img)



if __name__ == "__main__":
    # Sample file paths, adjust as per your requirement
    base_img_path = 'base_image.jpg'
    align_img_path = 'align_image.jpg'
    save_path = 'aligned'  # saves as aligned_base_aligned.jpg and aligned_align_aligned.jpg

    align_images(base_img_path, align_img_path, save_path)
