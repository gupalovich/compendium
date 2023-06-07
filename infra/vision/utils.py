import os
import shutil

import cv2 as cv
import numpy as np
from PIL import Image

from config import settings
from infra.common.entities import Img, Polygon, Rect

from .enums import ColorFormat


def load_img(
    img_path: str,
    static_path: str = None,
    fmt: ColorFormat = ColorFormat.BGR,
) -> Img:
    if static_path is None:
        static_path = settings.STATIC_PATH
    path = static_path + img_path
    img = cv.imread(path, fmt)
    if not img.any():
        raise FileNotFoundError(f"File {path} not found")
    return Img(img)


def save_img(img: Img, img_path: str, static_path: str = None) -> None:
    if static_path is None:
        static_path = settings.STATIC_PATH
    cv.imwrite(static_path + img_path, img.data)


def show_img(img: Img, window_name: str = "Window") -> None:
    cv.imshow(window_name, img.data)
    cv.waitKey(0)


def resize_img(img: Img, zoom_factor: float = 2) -> Img:
    """Zoom in/out image by x = zoom_factor"""
    new_img = cv.resize(img.data, None, fx=zoom_factor, fy=zoom_factor)
    return Img(new_img)


def crop_img(img: Img, region: Rect) -> Img:
    """Crop out rectangle from image"""
    new_img = img.data[
        region.left_top.y : region.right_bottom.y,
        region.left_top.x : region.right_bottom.x,
    ]
    return Img(new_img)


def crop_polygon_img(img: Img, region: Polygon) -> Img:
    """Crop out polygon from image and fill background"""
    points = region.as_np_array()
    # Create a binary mask with the polygon shape
    mask = np.zeros(img.data.shape[:2], dtype=np.uint8)
    cv.fillPoly(mask, [points], 255)
    # Apply the mask to the image
    masked_img = cv.bitwise_and(img.data, img.data, mask=mask)
    # Crop out the masked region
    cropped_img = masked_img[
        min(points[:, 1]) : max(points[:, 1]), min(points[:, 0]) : max(points[:, 0])
    ]
    return Img(cropped_img)


def convert_img_color(img: Img, fmt: ColorFormat) -> Img:
    """Create new instance with converted color"""
    return Img(cv.cvtColor(img.data, fmt))


def draw_rectangles(img: Img, rectangles: list[Rect]):
    """Draw rectangles on image in place"""
    color = (0, 255, 0)  # BGR
    line_type = cv.LINE_4

    for rect in rectangles:
        left_top = list(rect.left_top)
        right_bottom = list(rect.right_bottom)
        cv.rectangle(img.data, left_top, right_bottom, color, lineType=line_type)
    return img


def draw_crosshairs(img: Img, rectangles: list[Rect]):
    color = (255, 0, 255)  # BGR
    marker_type = cv.MARKER_CROSS

    for rect in rectangles:
        center = tuple(rect.center)
        cv.drawMarker(img.data, center, color, marker_type)
    return img


def draw_circles(img: Img, rectangles: list[Rect], radius: int = 1):
    color = (0, 0, 255)  # BGR
    line_type = cv.LINE_4
    thickness = 2

    for rect in rectangles:
        center = list(rect.center)
        cv.circle(
            img.data, center, radius, color, thickness=thickness, lineType=line_type
        )
    return img


def draw_lines(img: Img, rectangles: list[Rect]):
    color = (0, 0, 255)  # BGR
    thickness = 2

    for rect in rectangles:
        start = list(rect.left_top)
        end = list(rect.right_bottom)
        # Draw the line
        cv.line(img.data, start, end, color, thickness=thickness)
    return img


def organize_annotations(image_dir: str, annotations_dir: str, output_dir: str) -> list:
    """
    Filter neural network class annotations, based on train_data/images placement
    Copy annotations to the appropriate label directory for training and validation set

    Parameters
    ---
    image_dir : str
        Path to the directory with images
    annotations_dir : str
        Path to the directory with annotations
    output_dir : str
        Path to the directory with labels

    Example:
    ---
    image_dir = "./data/train_data/images"
    annotations_dir = "./data/annotations"
    output_dir = "./data/train_data/labels"

    organize_annotations(image_dir, annotations_dir, output_dir)

    TODO:
    ---
        - Make it a class, Split into smaller functions
        - Improve automation: Image placement randomization with fixed val_size
        - Test
    """

    # Get the list of images in the train and val directories
    train_images = {
        os.path.splitext(image)[0]: os.path.join("train", image)
        for image in os.listdir(os.path.join(image_dir, "train"))
    }
    val_images = {
        os.path.splitext(image)[0]: os.path.join("val", image)
        for image in os.listdir(os.path.join(image_dir, "val"))
    }

    print(f"Train images size: {len(train_images)}")
    print(f"Val images size: {len(val_images)}")

    # Filter annotations based on the presence of corresponding images
    annotations = os.listdir(annotations_dir)
    filtered_annotations = {"train": [], "val": []}
    print("Filtering ...")

    for annotation in annotations:
        image_name = os.path.splitext(annotation)[0]
        if image_name in train_images:
            filtered_annotations["train"].append(annotation)
            # Copy annotation to the appropriate label directory for training set
            label_dir = os.path.join(f"{output_dir}/train", annotation)
            shutil.copy(os.path.join(annotations_dir, annotation), label_dir)
        elif image_name in val_images:
            filtered_annotations["val"].append(annotation)
            # Copy annotation to the appropriate label directory for validation set
            label_dir = os.path.join(f"{output_dir}/val", annotation)
            shutil.copy(os.path.join(annotations_dir, annotation), label_dir)

    print(f"Filtered Train annotations size {len(filtered_annotations['train'])}")
    print(f"Filtered Val annotations size: {len(filtered_annotations['val'])}")

    return filtered_annotations


def mirror_images(image_dir: str) -> None:
    """Flip images horizonally

    Example:
    ---
    mirror_images("data/test_data")

    TODO:
    ---
    - Test
    """

    image_files = os.listdir(image_dir)

    for image_file in image_files:
        # Open the image using PIL
        image = Image.open(os.path.join(image_dir, image_file))
        # Mirror the image horizontally
        mirrored_image = image.transpose(Image.FLIP_LEFT_RIGHT)
        file_extension = os.path.splitext(image_file)[1]
        # Create the output file path with the correct file extension
        output_file_path = os.path.join(
            image_dir, f"{os.path.splitext(image_file)[0]}{file_extension}"
        )
        # Save the mirrored image
        mirrored_image.save(output_file_path)
