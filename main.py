import logging

import cv2 as cv

from config import settings


def main():
    from bots.albion.bots.gatherer import GathererStateManager

    gatherer = GathererStateManager()
    gatherer.start()

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
