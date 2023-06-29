import logging

from config import settings


def main():
    from core.display.vision import YoloVision

    model_file_path = "ai/albion/models/best_albion3.0.engine"
    classes = [
        "Monster",
        "Logs",
        "Sandstone",
        "Limestone",
        "Rough Stone",
        "Copper Ore",
        "Tin Ore",
        "Birch",
        "Chestnut",
    ]
    vision = YoloVision(model_file_path, classes)
    vision.start()

    # from bots.albion.bots.gatherer import GathererStateManager

    # gatherer = GathererStateManager()
    # gatherer.start()

    # from core.display.window import WindowHandler

    # window_handler = WindowHandler()
    # window_handler.live_screenshot()

    # import cv2 as cv
    # from bots.albion.bots.children import Navigator
    # from core.common.enums import State
    # from core.display.window import WindowHandler

    # w = WindowHandler()
    # navigator = Navigator()
    # while True:
    #     navigator.search_img = w.grab()
    #     navigator.state = State.START
    #     navigator.manage_nodes()

    #     cv.imshow("Debug Screen", navigator.cluster.data)
    #     key = cv.waitKey(1)
    #     if key == ord("q"):
    #         cv.destroyAllWindows()
    #         break


if __name__ == "__main__":
    if settings.DEBUG:
        logging.basicConfig(
            level=logging.INFO, format="%(name)s - %(levelname)s - %(message)s"
        )
        logging.info("DEBUG")

    main()
