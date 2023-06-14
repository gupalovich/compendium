from threading import Thread

from pynput import keyboard

from core.common.enums import State


class Bot:
    # contants
    INIT_SECONDS = 0
    MAIN_LOOP_DELAY = 0.04
    # bot properties
    running = False
    state = None

    def start(self):
        print(f"- Started {self.__class__.__name__}")
        self.running = True
        self._start()

    def stop(self):
        print(f"- Stopped {self.__class__.__name__}")
        self.running = False

    def set_state(self, state: State):
        print(f"\n- Set state {state} for {self.__class__.__name__}\n")
        self.state = state

    def _start(self):
        """Process loop"""


class BotFather(Bot):
    children = []

    def update_children_state(self):
        for child in self.children:
            child.set_state(self.state)


class BotMother(Bot):
    children = []

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
    INIT_SECONDS = 1


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
