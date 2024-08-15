# local imports:
from .utils import PathDescription, Size
from . import EnhLabel

# standard libraries:
from typing import Optional, Tuple, Any
from tkinter import Event, Misc
from threading import Thread
from logging import warning
from os.path import exists

# third-party libraries:
from PIL.Image import Image, open as open_image
from PIL.ImageTk import PhotoImage


class EnhImage(EnhLabel):
    _image: Optional[Image] = None
    _image_size: Optional[Tuple[int, int]] = None
    _photo_image: Optional[PhotoImage] = None
    _scheduled_resize: Optional[str] = None

    @staticmethod
    def get_image_size(container: Misc, image: Image) -> Tuple[int, int]:
        container_width: int = container.winfo_width()
        container_height: int = container.winfo_height()
        image_width, image_height = image.size
        scaling_factor: int = min(container_width / image_width, container_height / image_height)
        new_image_width: int = int(image_width * scaling_factor)
        new_image_height: int = int(image_height * scaling_factor) - 4
        return 1 if new_image_width <= 0 else new_image_width, 1 if new_image_height <= 0 else new_image_height

    def __init__(self, master: Optional[Misc] = None, *, imagepath: PathDescription = None, imagesize: Size = None, **standard_options: Any) -> None:
        super().__init__(master, **standard_options)
        self.configure(imagepath=imagepath, imagesize=imagesize)
        self.bind(sequence="<Configure>", func=self.schedule_resize, add=True)

    def schedule_resize(self, event: Optional[Event] = None) -> None:
        if self._image is None:
            return None
        if self._scheduled_resize is not None:
            self.after_cancel(id=self._scheduled_resize)
            self._scheduled_resize = None
        thread: Thread = Thread(target=self.auto_resize, daemon=True)
        self._scheduled_resize = self.after(ms=20, func=thread.start)

    def auto_resize(self) -> None:
        if self._image is None:
            return None
        new_image: Image = self._image.copy()
        new_size: Tuple[int, int] = self._image_size or self.get_image_size(self, image=new_image)
        if new_size == new_image.size:
            self._scheduled_resize = None
            return None
        resized_image: Image = new_image.resize(size=new_size)
        photo_image: PhotoImage = PhotoImage(image=resized_image)
        Misc.configure(self, image=photo_image)
        self._photo_image = photo_image
        self._scheduled_resize = None

    def configure(self, **standard_options: Any) -> Any:
        image_path: Optional[str] = standard_options.pop("imagepath", None)
        if image_path is not None and image_path and exists(path=image_path):
            self._image = open_image(fp=image_path)
            self.schedule_resize(event=None)
        elif image_path is not None and not exists(path=image_path):
            warning(msg="Image path not found.")
            self._image = None
            self._photo_image = None
        image_size: Size = standard_options.pop("imagesize", None)
        if self._image_size != image_size:
            self._image_size = image_size
            self.schedule_resize(event=None)
        return super().configure(**standard_options)
    config = configure
