from core.common.entities import Pixel
from core.input.actions import Actions


class AlbionActions(Actions):
    keybinds = {"mount": "a"}

    def mount(self):
        self.press(self.keybinds["mount"], delay=0.3)

    def dismount(self):
        self.press(self.keybinds["mount"], delay=0.3)

    def gather(self, resource_node: Pixel) -> None:
        self.move_click(resource_node)

    def move(self, location: Pixel) -> None:
        self.move_click(location)
