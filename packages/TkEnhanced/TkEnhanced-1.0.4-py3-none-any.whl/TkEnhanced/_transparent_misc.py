# standard libraries:
from tkinter import Widget, Event, Misc
from typing import Optional, Any


class TransparentMisc(Misc):
    _is_transparent_background: bool = False

    def __init__(self, master: Optional[Misc] = None, *, background: Optional[str] = "transparent", **standard_options: Any) -> None:
        assert isinstance(self, Widget), "This instance must be a Widget."
        background_color: Optional[str] = standard_options.pop("bg", background)
        super().__init__(master, **standard_options)
        self.configure(background=background_color)
        self.bind(sequence="<<ParentConfigure>>", func=self.on_parent_configure, add=True)

    def on_parent_configure(self, event: Optional[Event] = None) -> None:
        if not self._is_transparent_background:
            return None
        parent_background_color: Optional[str] = Misc.cget(self.master, key="background") or None
        if parent_background_color is None:
            return None
        Misc.configure(self.master, background=parent_background_color)
        for child_widget in self.winfo_children():
            child_widget.event_generate(sequence="<<ParentConfigure>>")

    def configure(self, **standard_options: Any) -> Any:
        background_color: Optional[str] = standard_options.pop("background", None)
        background_color = standard_options.pop("bg", background_color)
        if background_color is not None:
            self._is_transparent_background = isinstance(background_color, str) and background_color == "transparent"
            if not self._is_transparent_background:
                standard_options["background"] = background_color
            self.on_parent_configure(event=None)
        return super().configure(**standard_options)
    config = configure

    def cget(self, key: str) -> Any:
        return "transparent" if key in ("background", "bg") and self._is_transparent_background else super().cget(key)
