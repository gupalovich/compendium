import logging

from config import settings


def main():
    # crop_areas = {
    #     "skill_panel": Rect(Pixel(480, 975), Pixel(1475, 1065)),
    # }
    # ui_elements = {
    #     "mount": ImgLoader("albion/ui/mount_hp_1.png", 0.9),
    #     "mount_r": ImgLoader("albion/ui/mount_circle_radian.png", 0.87),
    # }

    from bots.albion.bots.gatherer import GathererStateManager

    gatherer = GathererStateManager()
    gatherer.start()

    # find_character_on_map()

    # from bots.albion.services.navigation import ImgExtractor
    # extractor = ImgExtractor()
    # img = extractor.extract("map", "test")
    # img.show()

    # from bots.albion.services.navigation import NodeMapper

    # node_mapper = NodeMapper(
    #     "albion/maps/mase_knoll.png",
    # )
    # node_mapper.start()

    # from bots.albion.services.navigation import NodeWalker

    # node_walker = NodeWalker()
    # node_walker.start()

    # from core.display.vision import YoloVision

    # classes = [
    #     "Heretic",
    #     "Elemental",
    #     "Sandstone",
    #     "Rough Stone",
    #     "Limestone",
    #     "Birch",
    #     "Chestnut",
    #     "Logs",
    #     "Copper Ore",
    #     "Tin Ore",
    # ]
    # model_file_path = "ai/albion/models/best_albion1.0.engine"
    # yolo_vision = YoloVision(model_file_path, classes)
    # yolo_vision.start()


if __name__ == "__main__":
    if settings.DEBUG:
        logging.basicConfig(
            level=logging.INFO, format="%(name)s - %(levelname)s - %(message)s"
        )
        logging.info("DEBUG")

    main()
