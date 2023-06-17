from threading import Lock, Thread
from time import sleep

from pynput import keyboard

from core.common.entities import Img
from core.common.enums import State
from core.display.vision import Vision


class Bot:
    # contants
    INIT_SECONDS = 0
    MAIN_LOOP_DELAY = 0.04
    PAUSE_DELAY = 0.2
    # bot properties
    running = False
    state = None
    # vision properties
    search_img = None

    def start(self):
        sleep(self.INIT_SECONDS)
        print(f"- Started {self.__class__.__name__}")
        self.running = True
        self._start()

    def stop(self):
        print(f"- Stopped {self.__class__.__name__}")
        self.running = False

    def set_state(self, state: State):
        print(f"- Set state {state} for {self.__class__.__name__}")
        self.state = state

    def _start(self):
        """Process loop"""


class BotParent(Bot):
    window = None
    children = []


class BotFather(BotParent):
    def set_state(self, state: State):
        super().set_state(state)
        self.update_children_state()

    def update_search_img(self):
        self.search_img = self.window.grab()
        self.update_children_search_img()

    def update_children_state(self):
        for child in self.children:
            child.set_state(self.state)

    def update_children_search_img(self):
        for child in self.children:
            child.update_search_img(self.search_img)


class BotMother(BotParent):
    def start(self):
        super().start()
        self.start_children()

    def stop(self):
        super().stop()
        self.stop_children()

    def start_children(self):
        for child in self.children:
            child = Thread(target=child.start, args=())
            child.start()

    def stop_children(self):
        for child in self.children:
            child.stop()


class BotChild(Bot):
    def __init__(self, vision: Vision) -> None:
        self.lock = Lock()
        self.vision = vision()

    def update_search_img(self, img: Img):
        self.lock.acquire()
        self.search_img = img
        self.lock.release()


class Watcher(BotMother):
    def __init__(self, children: list, on_release_type: str = ""):
        self.children = children
        self._set_on_release(on_release_type)

    def _set_on_release(self, on_release_type: str):
        if not isinstance(on_release_type, str):
            raise ValueError("Incorrect on_release_type: ", on_release_type)

        match on_release_type:
            case "gatherer":
                self.on_release = self.gatherer_on_release
            case _:
                self.on_release = self._on_release

    def gatherer_on_release(self, key: keyboard.Key):
        if key == keyboard.Key.esc:
            self.stop()
            return False
        return True

    def _on_release(self, key: keyboard.Key):
        if key == keyboard.Key.end:
            self.stop()
            return False
        return True

    def _start(self):
        listener = keyboard.Listener(on_release=self.on_release)
        listener.start()
