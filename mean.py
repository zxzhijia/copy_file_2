import cv2
import numpy as np
import os

def align_images_using_cross_correlation(template, images):
    """Align images to the given template using simple cross-correlation."""
    aligned_images = []
    for img in images:
        result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        _, _, _, max_loc = cv2.minMaxLoc(result)
        y_shift, x_shift = max_loc

        if y_shift > template.shape[0] // 2:
            y_shift -= template.shape[0]
        if x_shift > template.shape[1] // 2:
            x_shift -= template.shape[1]

        M = np.float32([[1, 0, x_shift], [0, 1, y_shift]])
        aligned_img = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]))
        aligned_images.append(aligned_img)

    return aligned_images

def get_common_roi(images):
    """Compute the largest common region of interest (ROI) across images."""
    x_min, y_min = 0, 0
    x_max, y_max = images[0].shape[1], images[0].shape[0]

    for img in images:
        x_max = min(x_max, img.shape[1])
        y_max = min(y_max, img.shape[0])

    width = x_max - x_min
    height = y_max - y_min

    return x_min, y_min, width, height

def draw_bbox_and_compute_mean(images, x, y, box_size=10):
    """Draw bounding boxes around a selected point and compute mean values inside."""
    means = []
    half_size = box_size // 2
    for img in images:
        cv2.rectangle(img, (x - half_size, y - half_size), (x + half_size, y + half_size), 255, 1)
        roi = img[y - half_size:y + half_size, x - half_size:x + half_size]
        means.append(np.mean(roi))
    return means

def main():
    folder_path = "./"  # The folder where your images are located. Change accordingly.
    image_filenames = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]

    if not image_filenames:
        print("No images found in the specified directory!")
        return

    template = cv2.imread(os.path.join(folder_path, image_filenames[0]), cv2.IMREAD_GRAYSCALE)
    images = [cv2.imread(os.path.join(folder_path, f), cv2.IMREAD_GRAYSCALE) for f in image_filenames[1:]]

    aligned_images = align_images_using_cross_correlation(template, images)
    x, y, w, h = get_common_roi([template] + aligned_images)
    template = template[y:y+h, x:x+w]
    aligned_images = [img[y:y+h, x:x+w] for img in aligned_images]

    def on_mouse_click(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            means = draw_bbox_and_compute_mean([template] + aligned_images, x, y)
            print(f"Means for the selected location: {means}")
            cv2.imshow("Template", template)

    cv2.imshow("Template", template)
    cv2.setMouseCallback("Template", on_mouse_click)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
