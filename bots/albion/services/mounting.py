from threading import Lock

from core.common.entities import Img

from ..actions.vision import MountVision, ServiceVision


class Service:
    search_img = None

    def __init__(self, vision: ServiceVision) -> None:
        self.lock = Lock()
        self.vision = vision()

    def update_search_img(self, img: Img):
        self.lock.acquire()
        self.search_img = img
        self.lock.release()

    def start(self) -> None:
        raise NotImplementedError()


class MountingService(Service):
    def __init__(self) -> None:
        super().__init__(MountVision)

    def is_mounted(self):
        pass

    def mount(self):
        pass

    def dismount(self):
        pass

    def start(self) -> None:
        print("Mounting service started")
        print(self.vision)
