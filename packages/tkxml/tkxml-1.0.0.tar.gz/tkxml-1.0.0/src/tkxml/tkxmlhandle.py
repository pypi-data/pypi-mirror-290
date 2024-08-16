# Licensed under the GNU LGPL v3
# Copyright (C) 2024 numlinka.

# std
import xml
import xml.etree.ElementTree
import tkinter
import threading
from types import *
from typing import *

# self
from . import settings
from .constants import *
from .namespace import *


class TkXMLHandle (object):
    def __init__(self, xml_file: str = ..., xml_str: str = ..., namespace: object = ...):
        self._lock = threading.RLock()
        self.namespace = self
        self.mainwindow: tkinter.Misc | tkinter.Wm

        self.widget = NamespaceWidget()
        self.variable = NamespaceVariable()
        self._table_widget: Dict[str: tkinter.Misc]  = dict()
        self._table_class: Dict[str: Dict[str: str]] = dict()
        self.source: List[object] = ...

        self.initialization_first()
        self.initialization(xml_file, xml_str, namespace)
        self.initialization_last()

    def initialization_first(self, *_) -> None: ...

    def initialization(self, xml_file: str = ..., xml_str: str = ..., namespace: object = ...) -> None:
        self.create_xml(xml_file, xml_str)
        self.set_namespace(namespace)

    def initialization_last(self, *_) -> None: ...

    def set_namespace(self, namespace: object = ...) -> None:
        with self._lock:
            if namespace is Ellipsis:
                self.namespace = self
                return

            if namespace is self:
                return

            setattr(namespace, "handle", self)
            setattr(namespace, "widget", self.widget)
            setattr(namespace, "variable", self.variable)
            self.namespace = namespace

    def add_widget(self, id_: str, misc: tkinter.Misc, link: str = ""):
        with self._lock:
            setattr(self.widget, id_, misc)

            if link not in self._table_widget:
                self._table_widget[link] = misc
                return

            count = 2
            while True:
                rlink = f"{link}{count}"
                if rlink in self._table_widget:
                    count += 1
                    continue

                self._table_widget[rlink] = misc
                break

    def add_class(self, id_: str, **kwargs) -> None:
        with self._lock:
            self._table_class[id_] = kwargs

    def get_class(self, id_: str) -> dict:
        with self._lock:
            return self._table_class[id_]

    def add_variable(self, id_: str, variable: tkinter.Variable) -> None:
        with self._lock:
            setattr(self.variable, id_, variable)

    def get_source(self, id_: str):
        with self._lock:
            if not isinstance(self.source, list):
                _source = settings.misc_source

            for items in _source:
                try:
                    attribute = getattr(items, id_)

                except AttributeError:
                    continue

                else:
                    return attribute

    def veriable_find(self, variable: str) -> Any:
        """## 变量查找

        找到并返回字符所对应的变量或对象
        """
        if variable[0] == "$":
            variable = variable[1:]

        name_link = variable.split(".")
        attribute_mode = False
        value = None

        for index, name in enumerate(name_link):
            if index == 0:
                value = self.namespace
                attribute_mode = True

            if attribute_mode:
                value = getattr(value, name)
                continue

            value = value(name)
            attribute_mode = True
            continue

        return value

    def variable_replace(self, items: dict) -> None:
        """## 变量替换

        将表中以 "$" 开头的字符串值替换成所对应的变量或对象
        """
        for key, value in items.items():
            if not isinstance(value, str):
                continue

            if not value.startswith("$"):
                continue

            items[key] = self.veriable_find(value)

    def class_addition(self, items: dict) -> None:
        """## class 添加

        将表中的 class 所对应的属性添加到这个表中但不覆盖

        类似于 html 中的 class 属性
        """
        if KEY_PSEUDO_CLASS not in items:
            return items

        class_ = items.pop(KEY_PSEUDO_CLASS)

        for class_name in class_.split(" "):
            class_items = self.get_class(class_name)
            for key, value in class_items.items():
                if key not in items:
                    items[key] = value

    def items_decomposition(self, items: dict, master: tkinter.Misc = ...) -> tuple[str, dict, str, dict]:
        id_ = "_"
        kwargs = dict()
        layout = dict()
        layout_type = KEY_PACK

        self.class_addition(items)
        self.variable_replace(items)

        if master is not Ellipsis:
            items[KEY_MASTER] = master

        for key, value in items.items():
            if key == KEY_ID:
                id_ = value
                continue

            if key in KEYS_LAYOUT:
                layout[key] = value
                continue

            elif key == KEY_LAYOUT:
                layout_type = value
                continue

            else:
                kwargs[key] = value
                continue

        return  id_, kwargs, layout_type, layout

    def create_widget_layout(self, misc: tkinter.Misc, layout_type: str, layout: dict):
        if not isinstance(misc, tkinter.Wm):
            match layout_type:
                case "pack":
                    misc.pack(**layout)

                case "grid":
                    misc.grid(**layout)

                case "place":
                    misc.place(**layout)

    def create_widget(self, element: xml.etree.ElementTree.Element, master: tkinter.Misc = ..., link: str = ""):
        items = dict(element.items())
        id_, kwargs, layout_type, layout = self.items_decomposition(items, master)
        link = f"{link}.{element.tag}" if link else element.tag

        if element.tag == KEY_PSEUDO_CLASS:
            if id_ is None:
                raise ValueError(f"当标签为 {KEY_PSEUDO_CLASS} 时 {KEY_ID} 不能为空")

            _ = kwargs.pop(KEY_MASTER) if KEY_MASTER in kwargs else None
            self.add_class(id_, **kwargs, **layout, layout=layout_type)
            return

        elif element.tag in KEYS_VERIABLE:
            if id_ is None:
                raise ValueError(f"当标签为 {element.tag} 时 {KEY_ID} 不能为空")

            _ = kwargs.pop(KEY_MASTER) if KEY_MASTER in kwargs else None
            class_ = self.get_source(element.tag)
            variable_ = class_(**kwargs)
            self.add_variable(id_, variable_)
            return

        class_ = self.get_source(element.tag)
        handle = class_(**kwargs)
        self.create_widget_layout(handle, layout_type, layout)
        self.add_widget(id_, handle, link)

        for child in element:
            self.create_widget(child, handle, link)

    def create_xml(self, xml_file: str = ..., xml_str: str = ...) -> None:
        if isinstance(xml_file, str):
            with open(xml_file, "r", encoding="utf-8") as fobj:
                content = fobj.read()

        elif isinstance(xml_str, str):
            content = xml_str

        else:
            return

        xml_handle: xml.etree.ElementTree.Element = xml.etree.ElementTree.fromstring(content)
        self.create_widget(xml_handle)

    def __getattribute__(self, name: str) -> Any:
        if name == "mainwindow":
            return tkinter._get_default_root("mainwindow")

        else:
            return super().__getattribute__(name)
