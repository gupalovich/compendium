from core.input.actions import Actions


class AlbionActions(Actions):
    """Common actions for albion bot"""


class MounterActions(AlbionActions):
    def mount(self):
        self.press("a", delay=0.3)


class NavigatorActions(AlbionActions):
    pass


class GathererActions(AlbionActions):
    pass
