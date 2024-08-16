# Licensed under the GNU LGPL v3
# Copyright (C) 2024 numlinka.

# std
import tkinter


class Namespace (object):
    ...



class NamespaceWidget (object):
    def __getattribute__(self, name: str) -> tkinter.Misc:
        return super().__getattribute__(name)



class NamespaceVariable (object):
    def __getattribute__(self, name: str) -> tkinter.Variable:
        return super().__getattribute__(name)



__all__ = [
    "Namespace",
    "NamespaceWidget",
    "NamespaceVariable"
]
