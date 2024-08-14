# Local imports:
from .utils import WindowUtils, PathDescription

# Standard libraries:
from tkinter import Toplevel, Misc, Tk
from typing import Optional, Any
from os.path import exists


class Window(WindowUtils):
    def configure_window(self, *, title: str, width: int, height: int, icon_path: PathDescription = None) -> None:
        self.wm_title(string=title)
        if icon_path and exists(path=icon_path):
            self.wm_iconbitmap(default=icon_path)
        self.center_window(width=width, height=height)

    def configure(self, **standard_options: Any) -> Any:
        result: Any = super().configure(**standard_options)
        for child_widget in self.winfo_children():
            child_widget.event_generate(sequence="<<ParentConfigure>>")
        return result
    config = configure


class EnhTk(Window, Tk):
    def __init__(
            self,
            *,
            title: Optional[str] = "Enhanced Tk",
            width: Optional[int] = 800,
            height: Optional[int] = 600,
            icon_path: PathDescription = None,
            **standard_options: Any) -> None:
        standard_options["className"] = standard_options.pop("className", "enhanced_tk")
        super().__init__(**standard_options)
        self.configure_window(title=title, width=width, height=height, icon_path=icon_path)


class EnhToplevel(Window, Toplevel):
    def __init__(
            self,
            master: Optional[Misc] = None,
            *,
            title: Optional[str] = "Enhanced Toplevel",
            width: Optional[int] = 800,
            height: Optional[int] = 600,
            icon_path: PathDescription = None,
            **standard_options: Any) -> None:
        super().__init__(master, **standard_options)
        self.configure_window(title=title, width=width, height=height, icon_path=icon_path)
