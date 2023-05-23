from pynput import keyboard, mouse


class KeyListener:
    def on_press(self, key):
        pass

    def on_release(self, key):
        if key == keyboard.Key.end:
            return False

    def on_move(self, x, y):
        pass

    def on_click(self, x, y, button, pressed):
        pass

    def on_scroll(self, x, y, dx, dy):
        pass

    def start(self, on_release=None):
        print(f"- {__class__.__name__} started")
        with mouse.Listener(
            on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll
        ) as listener:
            with keyboard.Listener(
                on_press=self.on_press, on_release=self.on_release
            ) as listener:
                listener.join()


key_listener = KeyListener()
