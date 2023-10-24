import cv2
import numpy as np

# Read the binary image (for finding the blobs)
binary_image_path = "path_to_your_binary_image.png"
binary_img = cv2.imread(binary_image_path, cv2.IMREAD_GRAYSCALE)

# Read the other image (for extracting profiles and drawing bounding boxes and annotations)
other_image_path = "path_to_other_image.png"
other_img = cv2.imread(other_image_path)

# Check if the images are valid
if binary_img is None or other_img is None:
    raise ValueError("Could not read the image(s).")

# Ensure the images are of the same size
if binary_img.shape != other_img.shape[:2]:
    raise ValueError("The binary image and the other image must be of the same size.")

# Ensure it's a binary image (values are only 0 or 255)
unique_vals = np.unique(binary_img)
if not np.array_equal(unique_vals, [0, 255]):
    raise ValueError("Image is not binary.")

# Find contours in the binary image
contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.5
color = (0, 0, 255)  # Red color for text
thickness = 1
offset = 20  # Vertical offset for displaying profile values

for contour in contours:
    # Get bounding box for each contour
    x, y, w, h = cv2.boundingRect(contour)
    
    # Crop the other image using the bounding box
    cropped_img = other_img[y:y+h, x:x+w]
    
    # Convert cropped_img to grayscale if it's a color image for profile measurement
    if len(cropped_img.shape) == 3:
        cropped_gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
    else:
        cropped_gray = cropped_img
    
    # Generate x-profile and y-profile
    x_profile = np.sum(cropped_gray, axis=0)  # Sum along rows
    y_profile = np.sum(cropped_gray, axis=1)  # Sum along columns
    
    # Compute min and max values for x and y profiles
    x_min, x_max = np.min(x_profile), np.max(x_profile)
    y_min, y_max = np.min(y_profile), np.max(y_profile)
    
    # Draw bounding box on the other image
    cv2.rectangle(other_img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    
    # Write profile values near the bounding box on the other image
    cv2.putText(other_img, f"X: {x_min}, {x_max}", (x, y - 2 * offset), font, font_scale, color, thickness, lineType=cv2.LINE_AA)
    cv2.putText(other_img, f"Y: {y_min}, {y_max}", (x, y - offset), font, font_scale, color, thickness, lineType=cv2.LINE_AA)

# Show the other image with bounding boxes and annotations
cv2.imshow("Other Image with Bounding Boxes and Profile Values", other_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
