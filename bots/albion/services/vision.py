from time import time

import cv2 as cv
import torch

from core.common.entities import Img, Pixel
from core.common.enums import ColorFormat
from core.display.window import WindowHandler


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
        search_img.reset()
        return results

    def start(self):
        loop_time = time()
        while True:
            search_img = self.window.grab()
            results = self.find(search_img)

            labels, cord = (
                results.xyxyn[0][:, -1].cpu().numpy(),
                results.xyxyn[0][:, :-1].cpu().numpy(),
            )

            n = len(labels)

            for i in range(n):
                row = cord[i]
                if row[4] >= 0.65:
                    x1, y1, x2, y2 = (
                        int(row[0] * 1920),
                        int(row[1] * 1080),
                        int(row[2] * 1920),
                        int(row[3] * 1080),
                    )
                    bgr = (0, 255, 0)
                    cv.rectangle(search_img.data, (x1, y1), (x2, y2), bgr, 2)
                    cv.putText(
                        search_img.data,
                        self.classes[int(labels[i])],
                        (x1, y1),
                        cv.FONT_HERSHEY_SIMPLEX,
                        0.9,
                        bgr,
                        2,
                    )

            cv.imshow("YOLOv5", search_img.data)

            print("FPS {}".format(1.0 / (time() - loop_time)))
            loop_time = time()

            key = cv.waitKey(1)
            if key == ord("q"):
                cv.destroyAllWindows()
                break
