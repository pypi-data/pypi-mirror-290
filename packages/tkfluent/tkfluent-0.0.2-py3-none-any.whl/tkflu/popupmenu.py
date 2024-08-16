from tkinter import Toplevel
from .frame import FluFrame


class FluPopupMenuWindow(Toplevel):
    def __init__(self, *args, transparent_color="#ffefa2", mode="light", width=200, height=400, **kwargs):
        super().__init__(*args, background=transparent_color, width=width, height=height, **kwargs)

        self.theme(mode=mode)

        self.transient_color = transparent_color
        self.overrideredirect(True)
        self.attributes("-transparentcolor", transparent_color)

        self.withdraw()

    def popup(self, x, y):
        self.geometry(f"+{x}+{y}")

    def theme(self, mode=None):
        if mode:
            self.mode = mode
        for widget in self.winfo_children():
            if hasattr(widget, "theme"):
                widget.theme(mode=self.mode.lower())


class FluPopupMenu(FluFrame):
    def __init__(self, *args, transparent_color="#ffefa2", style="popupmenu", **kwargs):
        self.window = FluPopupMenuWindow(transparent_color=transparent_color)

        super().__init__(self.window, *args, style=style, **kwargs)

        self.pack(fill="both", expand="yes", padx=5, pady=5)

    def popup(self, x, y):
        self.window.popup(x=x, y=y)
