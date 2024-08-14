# Local imports:
from ._transparent_misc import TransparentMisc

# Standard libraries:
from tkinter import Listbox, Canvas, Frame, Entry, Text


class EnhListbox(TransparentMisc, Listbox):
    pass


class EnhCanvas(TransparentMisc, Canvas):
    pass


class EnhFrame(TransparentMisc, Frame):
    pass


class EnhEntry(TransparentMisc, Entry):
    pass


class EnhText(TransparentMisc, Text):
    pass
