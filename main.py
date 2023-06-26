import logging

from config import settings


def main():
    from bots.albion.bots.gatherer import GathererStateManager

    gatherer = GathererStateManager()
    gatherer.start()


if __name__ == "__main__":
    if settings.DEBUG:
        logging.basicConfig(
            level=logging.INFO, format="%(name)s - %(levelname)s - %(message)s"
        )
        logging.info("DEBUG")

    main()
