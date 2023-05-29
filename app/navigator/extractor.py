"""
0. Extractor extracts map cluster for future comparison

1. Extractor extracts minimap rectangle

2. Transformer transforms size of extracted rectangle

3. Vision searches rectangle in image of map cluster

"""

import cv2 as cv
import numpy as np

from config import settings
from infra.common.entities import Coord, Polygon, Rect
from infra.devices.display.window import WindowHandler
from infra.devices.vision.opencv import opencv

crops = {
    "map": Polygon(
        points=[
            Coord(415, 570),
            Coord(960, 200),
            Coord(1500, 570),
            Coord(960, 950),
        ]
    ),
    "minimap": Rect(left_top=Coord(1661, 863), right_bottom=Coord(1761, 963)),
}

window = WindowHandler()
map_cluster = opencv.load_img("maps/mase_knoll.png")
screen = window.grab_mss()
minimap = opencv.crop_img(screen, crops["minimap"])
minimap = opencv.zoom(minimap, 0.6)
minimap = cv.cvtColor(minimap, cv.COLOR_BGR2RGB)
opencv.save_img(minimap, "maps/minimap.png")

result = opencv.match(opencv.zoom(map_cluster.img, 1.5), "maps/minimap.png")
print(result)

# map_cluster = extractor.extract(extractor.crops["map"])
# opencv.show_img(map_cluster)
# opencv.save_img(map_cluster, "maps/mase_knoll.png")
