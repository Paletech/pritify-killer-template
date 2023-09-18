import cv2
import numpy as np
from pathlib import Path


def get_image_with_overlay(image_path, overlay_path):
    image_name = Path(image_path).name
    base_image_path = f"static/img/{image_name}"

    base_image = cv2.imread(base_image_path)
    overlay_image = cv2.imread(overlay_path)

    hsv_base_image = cv2.cvtColor(base_image, cv2.COLOR_BGR2HSV)

    lower_green = np.array([50, 100, 100])
    upper_green = np.array([70, 255, 255])

    mask = cv2.inRange(hsv_base_image, lower_green, upper_green)

    green_pixels = np.where(mask > 0)

    x, y, w, h = cv2.boundingRect(np.array(list(zip(green_pixels[1], green_pixels[0]))))

    src_pts = np.array([[0, 0], [overlay_image.shape[1] - 1, 0], [0, overlay_image.shape[0] - 1]], dtype=np.float32)
    dst_pts = np.array([[x, y], [x + w - 1, y], [x, y + h - 1]], dtype=np.float32)
    affine_matrix = cv2.getAffineTransform(src_pts, dst_pts)

    warped_overlay_image = cv2.warpAffine(
        overlay_image,
        affine_matrix,
        (base_image.shape[1], base_image.shape[0]),
    )

    base_image[mask > 0] = warped_overlay_image[mask > 0]

    new_directory_path = Path("static/new_images")
    new_directory_path.mkdir(parents=True, exist_ok=True)
    result_path = f"{new_directory_path}/{image_name}"

    cv2.imwrite(result_path, base_image)

    return result_path
