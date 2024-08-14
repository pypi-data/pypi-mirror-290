# Standard libraries:
from typing import TypeAlias, Optional, Union, Tuple, List, Any
from tkinter.font import Font
from _tkinter import Tcl_Obj
from pathlib import Path

# Path aliases:
PathDescription: TypeAlias = Optional[Union[Path, str]]

# Font aliases:
FontDescription: TypeAlias = (
    str
    | Font
    | List[Any]
    | Tuple[str]
    | Tuple[str, int]
    | Tuple[str, int, str]
    | Tuple[str, int, List[str] | Tuple[str, ...]]
    | Tcl_Obj)
