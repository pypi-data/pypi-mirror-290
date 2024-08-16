from .popupmenu import FluPopupMenu
from tkdeft.object import DObject


class FluMenu(FluPopupMenu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)