from threading import Lock, Thread
from time import sleep

from core.common.enums import State


class Bot:
    # contants
    INIT_SECONDS = 0
    # threading properties
    thread_service = None
    running = False
    lock = None
    # bot properties
    state = None
    loop_delay = 0.04

    def __init__(self):
        self.lock = Lock()

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def set_state(self, state: State):
        self.state = state

    def run(self):
        raise NotImplementedError


class Gatherer(Bot):
    def __init__(self):
        super().__init__()
        print(self.lock)

    def run(self):
        """
        1. INIT
        - Логирование операции
        -

        """
        sleep(self.INIT_SECONDS)
        while self.running:
            sleep(self.loop_delay)
