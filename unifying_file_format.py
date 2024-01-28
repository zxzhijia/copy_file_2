import os
import cv2
from PIL import Image

def convert_to_grayscale_tiff(root_folder):
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.lower().endswith(('.png', '.tif')):
                original_file_path = os.path.join(root, file)
                # Change the file extension to .tif
                output_file_path = os.path.splitext(original_file_path)[0] + '.tif'
                
                # Read the image in grayscale with OpenCV
                img = cv2.imread(original_file_path, 0)
                # Convert the OpenCV image to a PIL Image
                img_pil = Image.fromarray(img)

                # Remove the original file
                os.remove(original_file_path)

                # Save the new image as an uncompressed TIFF using PIL
                img_pil.save(output_file_path, format='TIFF', compression=None)

# Example usage
root_folder = 'path/to/your/folder'  # Replace with your folder path
convert_to_grayscale_tiff(root_folder)
