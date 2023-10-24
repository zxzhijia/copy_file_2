import cv2
import numpy as np

def group_bounding_boxes_by_y(contours, threshold):
    bounding_boxes = [cv2.boundingRect(contour) for contour in contours]
    groups = []
    used = set()

    for i, (x1, y1, w1, h1) in enumerate(bounding_boxes):
        if i in used:
            continue
        group = [(x1, y1, w1, h1)]
        for j, (x2, y2, w2, h2) in enumerate(bounding_boxes):
            if j in used or i == j:
                continue
            if abs(y1 - y2) <= threshold:
                group.append((x2, y2, w2, h2))
                used.add(j)
        used.add(i)
        groups.append(group)

    return groups

# Paths to your images
binary_image_path = "path_to_your_binary_image.png"
other_image_path = "path_to_other_image.png"

binary_img = cv2.imread(binary_image_path, cv2.IMREAD_GRAYSCALE)
other_img = cv2.imread(other_image_path)

# Ensure the images are valid
if binary_img is None or other_img is None:
    raise ValueError("Could not read the image(s).")

# Ensure the images are of the same size
if binary_img.shape != other_img.shape[:2]:
    raise ValueError("The binary image and the other image must be of the same size.")

contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

threshold = 20  # adjust based on your requirement
groups = group_bounding_boxes_by_y(contours, threshold)

font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.5
color = (0, 0, 255)
thickness = 1
offset = 20

for group in groups:
    avg_y = int(sum([y for x, y, w, h in group]) / len(group))
    for x, _, w, h in group:
        cropped_img = other_img[avg_y:avg_y+h, x:x+w]

        if len(cropped_img.shape) == 3:
            cropped_gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
        else:
            cropped_gray = cropped_img

        x_profile = np.sum(cropped_gray, axis=0)
        y_profile = np.sum(cropped_gray, axis=1)

        x_min, x_max = np.min(x_profile), np.max(x_profile)
        y_min, y_max = np.min(y_profile), np.max(y_profile)

        cv2.rectangle(other_img, (x, avg_y), (x + w, avg_y + h), (255, 0, 0), 2)
        cv2.putText(other_img, f"X: {x_min}, {x_max}", (x, avg_y - 2 * offset), font, font_scale, color, thickness, lineType=cv2.LINE_AA)
        cv2.putText(other_img, f"Y: {y_min}, {y_max}", (x, avg_y - offset), font, font_scale, color, thickness, lineType=cv2.LINE_AA)

cv2.imshow("Other Image with Adjusted Bounding Boxes and Profile Values", other_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
