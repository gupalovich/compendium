"""
0. Extractor extracts map cluster for future comparison

1. Extractor extracts minimap rectangle

2. Transformer transforms size of extracted rectangle

3. Vision searches rectangle in image of map cluster

"""

import cv2 as cv
import numpy as np

from config import settings
from infra.common.entities import Location, Polygon
from infra.display.window import Window
from infra.vision.opencv import opencv


class Extractor:
    def __init__(self):
        self.window = Window(process_name=settings.PROCESS_NAME)
        self.crops = {
            "map": Polygon(
                points=[
                    Location(415, 570),
                    Location(960, 200),
                    Location(1500, 570),
                    Location(960, 950),
                ]
            ),
            "minimap": Polygon(
                points=[
                    Location(1550, 910),
                    Location(1710, 795),
                    Location(1880, 910),
                    Location(1720, 1020),
                ]
            ),
        }

    def extract(self, region: Polygon) -> np.ndarray:
        """Extract polygon from screen and fill background"""

        screen = self.window.grab_mss()
        points = region.as_np_array()
        # Create a binary mask with the polygon shape
        mask = np.zeros(screen.shape[:2], dtype=np.uint8)
        cv.fillPoly(mask, [points], 255)
        # Apply the mask to the image
        masked_image = cv.bitwise_and(screen, screen, mask=mask)
        # Crop out the masked region
        cropped_image = masked_image[
            min(points[:, 1]) : max(points[:, 1]), min(points[:, 0]) : max(points[:, 0])
        ]
        cropped_image = opencv.cvt_img_color(cropped_image, fmt="rgb")
        return cropped_image


extractor = Extractor()
# minimap = extractor.extract(extractor.crops["minimap"])
# opencv.show_img(minimap)
# opencv.save_img(minimap, "minimap.png")

# map_cluster = extractor.extract(extractor.crops["map"])
# opencv.show_img(map_cluster)
# opencv.save_img(map_cluster, "maps/mase_knoll.png")
