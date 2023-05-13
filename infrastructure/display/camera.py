class CameraHandler:
    """Class for 3d camera handling"""

    # constants
    INITIALIZING_SECONDS = 2
    # threading properties
    stopped = True
    lock = None
    # properties
    state = None
    screen = None
    screen_size = (1920, 1080)
    targets = []
    character_position = []
    main_loop_delay = 0.04

    def __init__(self):
        # create a thread lock
        self.lock = Lock()
        # properties
        self.vision = Vision()

    def choose_target(self, targets: list[tuple]) -> tuple:
        """Choose middle target from targets"""
        index = math.floor(len(targets) / 2)
        index = index - 1 if len(targets) % 2 == 0 else index
        return targets[index]

    def follow_target(self, rect: tuple) -> None:
        """1786 1907
        - Using skill: Доблестный Удар
        20 0
        1900 1828"""
        """Camera follow given target coords
           move_y = int(y - (screen_h / 3))  #  and abs(move_y) < 50"""
        screen_w, screen_h = self.screen_size
        x, y, w, h = calc_rect_middle(rect)
        move_x = int(x - (screen_w / 2))
        if abs(move_x) < 50:
            return None
        wind_mouse_move_camera(move_x, 0, step=35)

    def move_camera_around(self) -> None:
        """Move camera around"""
        move_range = random.randint(200, 1000)
        wind_mouse_move_camera(move_range, 0, step=35)

    def adjust_angle(self, rect: tuple) -> None:
        """Adjust camera angle by character position on screen"""
        x, y, w, h = calc_rect_middle(rect)
        target_y = 680
        pos_x, pos_y = win32api.GetCursorPos()
        move_y = -int(y - target_y)
        if abs(move_y) <= 4:
            return
        overhead = 70
        move_y = move_y + overhead if move_y > 0 else move_y - overhead
        wind_mouse_move_camera(pos_x, move_y)

    def adjust_camera_angle(self):
        """camera adjustment by character"""
        self.character_position = self.vision.find_ui(
            self.screen, "character", threshold=0.8
        )
        if self.character_position:
            self.adjust_angle(self.character_position[0])

    def update_targets(self, targets: list[tuple]) -> None:
        """Threading method: update targets property"""
        self.lock.acquire()
        self.targets = targets
        self.lock.release()

    def update_screen(self, screen: object) -> None:
        """Threading method: update screen property"""
        self.lock.acquire()
        self.screen = screen
        self.lock.release()

    def update_state(self, state: object) -> None:
        """Threading method: update screen property"""
        self.lock.acquire()
        self.state = state
        self.lock.release()

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()
        print(f"- {__class__.__name__} started")

    def stop(self):
        self.stopped = True
        print(f"- {__class__.__name__} stopped")

    def run(self):
        sleep(self.INITIALIZING_SECONDS)
        while not self.stopped:
            if self.targets:
                self.follow_target(self.targets[0])

            if self.state == BotState.INIT:
                pass
            elif self.state == BotState.SEARCHING:
                if not self.targets:
                    self.move_camera_around()
            elif self.state == BotState.KILLING:
                pass
            sleep(self.main_loop_delay)
