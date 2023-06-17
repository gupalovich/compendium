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

    def mount(self):
        pass

    def dismount(self):
        pass

    def start(self) -> None:
        if self.vision.is_mounting(self.search_img):
            print("Mounting")
        elif self.vision.is_mounted(self.search_img):
            print("On mount")
        else:
            print("Gonna mount")
