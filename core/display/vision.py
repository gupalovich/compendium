from time import time
from typing import List

import cv2 as cv
import numpy as np
import pytesseract
import torch

from core.common.entities import Img, ImgLoader, Pixel, Rect, SearchResult
from core.common.enums import ColorFormat
from core.display.utils import draw_rectangles
from core.display.window import WindowHandler

from .utils import draw_rectangles


class Vision:
    method = cv.TM_CCOEFF_NORMED

    def match_template(
        self, ref_img: Img, search_img: Img, confidence: float = 0.65
    ) -> List[tuple[int, int]]:
        """cv2 match template based on confidence value"""

        result = cv.matchTemplate(search_img.data, ref_img.data, self.method)
        locations = np.where(result >= confidence)
        locations = list(zip(*locations[::-1]))  # removes empty arrays
        return locations

    def find(self, ref_img: Img, search_img: Img, crop: Rect = None) -> SearchResult:
        ref_width, ref_height = ref_img.width, ref_img.height
        ref_img.cvt_color(ColorFormat.BGR_GRAY)
        search_img.cvt_color(ColorFormat.BGR_GRAY)

        if crop:
            search_img.crop(crop)

        locations = self.match_template(ref_img, search_img, ref_img.confidence)
        mask = np.zeros(search_img.data.shape[:2], dtype=np.uint8)
        # reset images for next search
        ref_img.reset()
        search_img.reset()

        result = SearchResult(ref_img, search_img)

        for loc_x, loc_y in locations:
            center_x = loc_x + ref_width // 2
            center_y = loc_y + ref_height // 2

            if mask[center_y, center_x] != 255:
                # Mask out detected object
                mask[loc_y : loc_y + ref_height, loc_x : loc_x + ref_width] = 255

                if crop:
                    loc_x += crop.left_top.x
                    loc_y += crop.left_top.y

                loc = Rect(
                    left_top=Pixel(loc_x, loc_y), width=ref_width, height=ref_height
                )
                result.add(loc)

        return result

    def find_color(self):
        """
        TODO
        """

    def find_text(self, search_img: Img, crop: Rect) -> str:
        search_img.crop(crop)
        return pytesseract.image_to_string(search_img.data)


class YoloVision:
    classes = [
        "Heretic",
        "Elemental",
        "Sandstone",
        "Rough Stone",
        "Limestone",
        "Birch",
        "Chestnut",
        "Logs",
        "Copper Ore",
        "Tin Ore",
    ]
    resolution = Rect(left_top=Pixel(0, 0), width=1920, height=1080)
    confidence = 0.65

    def __init__(self, model_path: str, classes: list[str] = None):
        self.model = None
        self.model_path = model_path
        self.classes = classes or self.classes
        self.window = WindowHandler()
        self._init_model()

    def _init_model(self):
        self.model = torch.hub.load("ultralytics/yolov5", "custom", self.model_path)
        self.model.cuda()
        self.model.multi_label = False

    def find(self, search_img: Img):
        search_img.cvt_color(ColorFormat.BGR_RGB)
        search_img.resize(Pixel(640, 640))

        results = self.model(search_img.data)
        labels, cord = (
            results.xyxyn[0][:, -1].cpu().numpy(),
            results.xyxyn[0][:, :-1].cpu().numpy(),
        )

        filtered_result = []
        n = len(labels)
        for i in range(n):
            row = cord[i]
            if row[4] >= self.confidence:
                label = self.classes[int(labels[i])]
                x1, y1, x2, y2 = (
                    int(row[0] * self.resolution.width),
                    int(row[1] * self.resolution.height),
                    int(row[2] * self.resolution.width),
                    int(row[3] * self.resolution.height),
                )
                filtered_result.append(
                    Rect(
                        left_top=Pixel(x1, y1), right_bottom=Pixel(x2, y2), label=label
                    ),
                )
        search_img.reset()
        return filtered_result

    def start(self):
        loop_time = time()
        while True:
            search_img = self.window.grab()
            result = self.find(search_img)

            print("FPS {}".format(1.0 / (time() - loop_time)))
            loop_time = time()

            draw_rectangles(search_img, result, with_label=True)
            cv.imshow("YOLOv5", search_img.data)

            key = cv.waitKey(1)
            if key == ord("q"):
                cv.destroyAllWindows()
                break


class LiveVision:
    exit_key = "q"
    to_log = True
    resize = Pixel(1200, 675)

    def __init__(self, ref: ImgLoader, crop: Rect = None):
        self.ref = ref
        self.crop = crop

    def start(self) -> None:
        vision = Vision()
        window = WindowHandler()
        loop_time = time()
        while True:
            search_img = window.grab()
            result = vision.find(self.ref, search_img, self.crop)
            show_img = draw_rectangles(search_img, result.locations)
            show_img.resize(self.resize)
            if self.to_log:
                print("Found objects: ", len(result.locations))

            print("FPS {}".format(1.0 / (time() - loop_time)))
            loop_time = time()

            cv.imshow("Debug Screen", result.search_img.data)
            if cv.waitKey(1) == ord(self.exit_key):
                cv.destroyAllWindows()
                break
