# Local imports:
from ._hover_misc import HoverMisc
from .utils import ColorUtils

# Standard libraries:
from tkinter import Button, Misc
from typing import Optional, Any


class EnhButton(HoverMisc, Button):
    def __init__(
            self,
            master: Optional[Misc] = None,
            *,
            background: Optional[str] = "transparent",
            borderwidth: Optional[int] = 0,
            hoverbackground: Optional[str] = None,
            **standard_options: Any) -> None:
        super().__init__(master, background=background, borderwidth=borderwidth, hoverbackground=hoverbackground, **standard_options)
        if hoverbackground is not None:
            return None
        active_background_color: str = self.cget(key="activebackground")
        hover_background_color: str = ColorUtils.adjust_hex_code(
            hex_code=active_background_color,
            brightness_factor=.6)
        self.configure(hoverbackground=hover_background_color)
