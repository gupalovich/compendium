from threading import Lock, Thread
from time import sleep

from pynput import keyboard

from core.common.entities import Img
from core.common.enums import State
from core.display.window import WindowHandler


class Bot:
    # contants
    INIT_SECONDS: float = 0
    PAUSE_DELAY: float = 0.2
    MAIN_LOOP_DELAY: float = 0.03
    # properties
    running: bool = False
    state: State = None
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
        while self.running:
            self.manage_state()
            sleep(self.MAIN_LOOP_DELAY)

    def set_state(self, state: State, state_type: str = "state"):
        if state_type == "state":
            print("")
        print(f"- Set {state_type} [{state.name}] for {self.__class__.__name__}")
        self.state = state

    def manage_state(self):
        """State sequence logic"""


class BotParent(Bot):
    children: list["BotChild"] = []


class BotChild(Bot):
    def __init__(self) -> None:
        self.lock = Lock()

    def set_state(self, state: State, state_type: str = "status"):
        super().set_state(state, state_type)

    def update_search_img(self, img: Img):
        self.lock.acquire()
        self.search_img = img
        self.lock.release()


class BotFather(BotParent):
    window: WindowHandler = None
    active_child: BotChild = None

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
