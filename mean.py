import cv2
import os
import numpy as np

def align_image_to_template(image, template):
    # Compute cross-correlation to find the offset for alignment
    result = cv2.matchTemplate(image, template, cv2.TM_CCORR_NORMED)
    _, _, _, max_loc = cv2.minMaxLoc(result)
    return max_loc

def find_common_area(image_shapes):
    # The goal is to find the maximum x,y starting positions and minimum ending x,y positions
    max_start_x, max_start_y = 0, 0
    min_end_x, min_end_y = float('inf'), float('inf')
    for (start_x, start_y), (w, h) in image_shapes:
        max_start_x = max(max_start_x, start_x)
        max_start_y = max(max_start_y, start_y)
        min_end_x = min(min_end_x, start_x + w)
        min_end_y = min(min_end_y, start_y + h)
    return (max_start_x, max_start_y), (min_end_x, min_end_y)

def crop_common_area(image, start, end):
    return image[start[1]:end[1], start[0]:end[0]]

def main():
    path_to_images = './path_to_folder/'  # Specify your path here
    filenames = [f for f in os.listdir(path_to_images) if f.endswith('.png')]  # assuming png images
    template = cv2.imread(os.path.join(path_to_images, filenames[0]), cv2.IMREAD_GRAYSCALE)

    # List to store the bounding boxes of each image after alignment
    image_shapes = []

    for filename in filenames:
        image = cv2.imread(os.path.join(path_to_images, filename), cv2.IMREAD_GRAYSCALE)
        
        # Align the image to template
        dx, dy = align_image_to_template(image, template)
        aligned_image = np.roll(image, shift=dx, axis=1)  # Shift along x
        aligned_image = np.roll(aligned_image, shift=dy, axis=0)  # Shift along y

        # Store the bounding box of the shifted image
        h, w = aligned_image.shape
        image_shapes.append(((dx, dy), (w, h)))

        # Save the aligned image (if needed)
        cv2.imwrite(os.path.join(path_to_images, 'aligned_' + filename), aligned_image)

    # Find the common area across all images
    start, end = find_common_area(image_shapes)
    print(f"Common area starts at: {start} and ends at: {end}")

    for filename in filenames:
        image = cv2.imread(os.path.join(path_to_images, 'aligned_' + filename), cv2.IMREAD_GRAYSCALE)
        cropped = crop_common_area(image, start, end)
        cv2.imwrite(os.path.join(path_to_images, 'cropped_' + filename), cropped)

if __name__ == "__main__":
    main()
