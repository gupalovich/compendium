from threading import Lock, Thread
from time import sleep

from pynput import keyboard

from core.common.entities import Img
from core.common.enums import State
from core.display.vision import Vision
from core.display.window import WindowHandler


class Bot:
    # contants
    INIT_SECONDS: float = 0
    PAUSE_DELAY: float = 0.2
    MAIN_LOOP_DELAY: float = 0.04
    # bot properties
    running: bool = False
    state: State = None
    # vision properties
    search_img: Img = None

    def start(self):
        sleep(self.INIT_SECONDS)
        print(f"- Started {self.__class__.__name__}")
        self.running = True
        self._start()

    def stop(self):
        print(f"- Stopped {self.__class__.__name__}")
        self.running = False

    def _start(self):
        """Process loop"""

    def set_state(self, state: State):
        print(f"- Set state {state} for {self.__class__.__name__}")
        self.state = state

    def manage_state(self):
        """State sequence logic"""


class BotParent(Bot):
    children: list["BotChild"] = []


class BotChild(Bot):
    targets: dict = {}

    def __init__(self, vision: Vision) -> None:
        self.lock = Lock()
        self.vision = vision()

    def update_search_img(self, img: Img):
        self.lock.acquire()
        self.search_img = img
        self.lock.release()


class BotFather(BotParent):
    window: WindowHandler = None
    active_child: BotChild = None

    def manage_active_child(self, child: BotChild, next_state: State):
        if child.state == State.IDLE:
            self.active_child = child
            self.active_child.set_state(State.START)
        if child.state == State.DONE:
            self.active_child.set_state(State.IDLE)
            self.active_child = None
            self.set_state(next_state)

    def set_start_active_child(self, child: BotChild):
        self.stop_active_child()
        self.active_child = child
        self.active_child.set_state(State.START)

    def stop_active_child(self):
        if self.active_child and self.active_child.state == State.DONE:
            self.active_child.set_state(State.IDLE)

    def update_search_img(self):
        self.search_img = self.window.grab()

    def update_children_search_img(self):
        for child in self.children:
            child.update_search_img(self.search_img)

    def set_children_state(self, state: State):
        for child in self.children:
            child.set_state(state)


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
