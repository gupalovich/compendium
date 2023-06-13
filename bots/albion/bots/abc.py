from threading import Thread

from core.common.enums import State


class Bot:
    # contants
    MAIN_LOOP_DELAY = 0.04
    # threading properties
    running = False
    # bot properties
    state = None

    def start(self):
        print(f"- Started {self.__class__.__name__}")
        self.running = True

    def stop(self):
        print(f"- Stopped {self.__class__.__name__}")
        self.running = False

    def set_state(self, state: State):
        self.state = state

    def _start(self):
        """Process loop"""


class BotFather(Bot):
    # contants
    INIT_SECONDS = 0
    # properties
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

    def update_children_state(self):
        for child in self.children:
            child.set_state(self.state)

    def prepare_task(self):
        pass

    def propagate_info(self):
        pass


class BotMother(Bot):
    pass


class BotChild(Bot):
    # contants
    INIT_SECONDS = 1

    def start(self):
        super().start()
        self._start()
