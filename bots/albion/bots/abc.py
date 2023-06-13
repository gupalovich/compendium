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
    key_binds = []
    children = []

    def start_children(self):
        for child in self.children:
            child.start()

    def stop_children(self):
        for child in self.children:
            child.stop()

    def feed_children(self):
        pass

    def prepare_task(self):
        pass


class BotMother(Bot):
    pass


class BotChild(Bot):
    # contants
    INIT_SECONDS = 1
