import cv2
import numpy as np

def align_images_using_cross_correlation(template, images):
    """
    Align images to the given template using simple cross-correlation.
    Return aligned images.
    """
    aligned_images = []

    for img in images:
        # Compute cross-correlation
        result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        _, _, _, max_loc = cv2.minMaxLoc(result)

        # Calculate translational offset
        y_shift, x_shift = max_loc

        # Adjust the shift values if they are beyond half the image dimensions
        if y_shift > template.shape[0] // 2:
            y_shift -= template.shape[0]
        if x_shift > template.shape[1] // 2:
            x_shift -= template.shape[1]

        # Translate the image
        M = np.float32([[1, 0, x_shift], [0, 1, y_shift]])
        aligned_img = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]))

        aligned_images.append(aligned_img)

    return aligned_images

# Other functions remain unchanged...

def main():
    # Load template and other images
    template = cv2.imread("template.jpg", cv2.IMREAD_GRAYSCALE)
    image_filenames = ["img1.jpg", "img2.jpg", ...]  # Add your image paths here
    images = [cv2.imread(f, cv2.IMREAD_GRAYSCALE) for f in image_filenames]

    # Align all images to template using simple cross-correlation
    aligned_images = align_images_using_cross_correlation(template, images)
    
    # Crop to common ROI
    x, y, w, h = get_common_roi([template] + aligned_images)
    template = template[y:y+h, x:x+w]
    aligned_images = [img[y:y+h, x:x+w] for img in aligned_images]

    # Display template and wait for a user click
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
