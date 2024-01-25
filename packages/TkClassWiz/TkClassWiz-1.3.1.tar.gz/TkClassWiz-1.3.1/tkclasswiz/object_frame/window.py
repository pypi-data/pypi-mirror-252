from typing import get_origin, Iterable, List
from collections.abc import Iterable as ABCIterable

from .frame_number import *
from .frame_iterable import *
from .frame_string import *
from .frame_struct import *
from .frame_base import *


from ..dpi import dpi_scaled
from ..extensions import extendable
from ..utilities import gui_except
from ..doc import doc_category

import tkinter as tk
import tkinter.ttk as ttk


__all__ = (
    "ObjectEditWindow",
)


@extendable
@doc_category("Object window")
class ObjectEditWindow(tk.Toplevel):
    """
    Top level window for creating and editing new objects.
    """

    # Map used to map types to specific class.
    # If type is not in this map, structured object will be assumed.
    TYPE_INIT_MAP = {
        str: NewObjectFrameString,
        float: NewObjectFrameNumber,
        int: NewObjectFrameNumber,
        list: NewObjectFrameIterable,
        Iterable: NewObjectFrameIterable,
        ABCIterable: NewObjectFrameIterable,
        tuple: NewObjectFrameIterable,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._closed = False

        dpi_5 = dpi_scaled(5)

        # Elements
        self.opened_frames: List[NewObjectFrameBase] = []
        self.frame_main = ttk.Frame(self, padding=(dpi_5, dpi_5))
        self.frame_toolbar = ttk.Frame(self, padding=(dpi_5, dpi_5))
        ttk.Button(self.frame_toolbar, text="Close", command=self.close_object_edit_frame).pack(side="left")
        ttk.Button(self.frame_toolbar, text="Save", command=self.save_object_edit_frame).pack(side="left")

        self.frame_toolbar.pack(expand=False, fill=tk.X)
        self.frame_main.pack(expand=True, fill=tk.BOTH)
        self.frame_main.rowconfigure(0, weight=1)
        self.frame_main.columnconfigure(0, weight=1)

        var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            self.frame_toolbar,
            text="Keep on top",
            variable=var,
            command=lambda: self.attributes("-topmost", var.get()),
        ).pack(side="right")
        self.attributes("-topmost", var.get())

        # Window initialization
        NewObjectFrameBase.set_origin_window(self)
        self.protocol("WM_DELETE_WINDOW", self.close_object_edit_frame)

    @property
    def closed(self) -> bool:
        return self._closed

    def open_object_edit_frame(
        self,
        class_,
        return_widget,
        old_data = None,
        check_parameters: bool = True,
        allow_save: bool = True,
        **kwargs
    ):
        """
        Opens new frame for defining an object.
        Parameters are the same as for NewObjectFrameBase.

        Parameters
        ------------
        class_: Any
            The class we are defining for.
        return_widget: Any
            The widget to insert the ObjectInfo into after saving.
        old_data: Any
            The old_data gui data.
        check_parameters: bool
            Check parameters (by creating the real object) upon saving.
            This is ignored if editing a function instead of a class.
        allow_save: bool
            If False, will open in read-only mode.
        """
        frame = self._create_and_add_frame(class_, return_widget, old_data, check_parameters, allow_save, kwargs)
        if frame is None and not self.opened_frames:
            self.destroy()
            self._closed = True

    @gui_except()
    def _create_and_add_frame(
        self,
        class_: type,
        return_widget,
        old_data,
        check_parameters: bool,
        allow_save: bool,
        kwargs
    ):
        frame: NewObjectFrameBase
        class_origin = get_origin(class_)
        if class_origin is None:
            class_origin = class_

        frame_class = self.TYPE_INIT_MAP.get(class_origin, NewObjectFrameStruct)
        self.opened_frames.append(
            frame := frame_class(
                class_,
                return_widget,
                old_data=old_data,
                check_parameters=check_parameters,
                allow_save=allow_save,
                parent=self.frame_main,
                **kwargs
            )
        )

        if len(self.opened_frames) > 1:
            self.opened_frames[-2].pack_forget()

        frame.pack(fill=tk.BOTH, expand=True)
        frame.update_window_title()
        self.set_default_size_y()

        return frame

    def close_object_edit_frame(self):
        self.opened_frames[-1].close_frame()

    def save_object_edit_frame(self):
        self.opened_frames[-1].save()

    def clean_object_edit_frame(self):
        self.opened_frames.pop().destroy()
        opened_frames_len = len(self.opened_frames)

        if opened_frames_len:
            frame = self.opened_frames[-1]
            frame.pack(fill=tk.BOTH, expand=True)  # (row=0, column=0)
            frame.update_window_title()
            self.set_default_size_y()
        else:
            self._closed = True
            self.destroy()

    def set_default_size_y(self):
        "Sets window Y size to default"
        self.update()
        self.geometry(f"{self.winfo_width()}x{self.winfo_reqheight()}")
