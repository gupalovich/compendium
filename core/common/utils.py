import os
import shutil
from time import sleep

from PIL import Image

from core.common.entities import Pixel, Rect


def find_closest(origin: Pixel, positions: list[Pixel] | list[Rect]) -> Pixel:
    """Find the closest position to the origin"""
    min_dist = float("inf")
    closest_pos = None

    for pos in positions:
        if isinstance(pos, Rect):
            pos = pos.center

        dist = abs(origin.x - pos.x) + abs(origin.y - pos.y)
        if dist < min_dist:
            min_dist = dist
            closest_pos = pos
    return closest_pos


def log(msg: str, delay: float = 0):
    print(f"- {msg}")
    if delay:
        sleep(delay)


def organize_annotations(image_dir: str, annotations_dir: str, output_dir: str) -> list:
    """
    Filter neural network class annotations, based on train_data/images placement
    Copy annotations to the appropriate label directory for training and validation set

    ### Parameters
    image_dir : str
        Path to the directory with images
    annotations_dir : str
        Path to the directory with annotations
    output_dir : str
        Path to the directory with labels

    ### Example:
    image_dir = "./ai/albion/train_data/images"
    annotations_dir = "./ai/albion/all_annotations"
    output_dir = "./ai/albion/train_data/labels"

    organize_annotations(image_dir, annotations_dir, output_dir)

    ### TODO:
        - Test
        - Improve automation: Image placement randomization with fixed val_size
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


def replace_annotation_class(directory: str, class_to_replace: int, new_class: int):
    """
    ### Example:
    - replace_annotation_class("/path/to/annotations_directory", 7, 2)
    """

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r+", encoding="utf-8") as file:
                lines = file.readlines()
                file.seek(0)  # Move the file pointer to the beginning
                for line in lines:
                    parts = line.split()
                    annotation_class = int(parts[0])
                    if annotation_class == class_to_replace:
                        parts[0] = str(new_class)
                    updated_line = " ".join(parts)
                    file.write(updated_line + "\n")
                file.truncate()  # Remove any remaining content after the updated lines


def delete_annotation_class_line(directory: str, class_to_delete: int):
    """
    ### Example:
    - delete_annotation_class_line("/path/to/annotations_directory", 4)
    """

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r+", encoding="utf-8") as file:
                lines = file.readlines()
                file.seek(0)  # Move the file pointer to the beginning
                file.truncate()  # Clear the file content
                for line in lines:
                    try:
                        parts = line.split()
                        annotation_class = int(parts[0])
                        if annotation_class != class_to_delete:
                            file.write(line.rstrip("\n") + "\n")
                    except ValueError:
                        print("File contains non-integer values:", filepath)


def mirror_images(image_dir: str) -> None:
    """Flip images horizonally

    ### Example:
    mirror_images("data/test_data")

    ### TODO: Test
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
