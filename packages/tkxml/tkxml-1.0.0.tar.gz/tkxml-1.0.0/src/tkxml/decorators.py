# Licensed under the GNU LGPL v3
# Copyright (C) 2024 numlinka.

# std
import tkinter
import threading
from typing import *


class _Cistern (object):
    event: threading.Event
    args: tuple
    kwargs: dict
    result: Any = None
    exception: Exception = None



def tkrecall(function: Callable):
    function_ = function

    def is_tk_alive() -> bool:
        try:
            if tkinter._get_default_root("mainwindow").winfo_exists():
                return True

        except Exception:
            return False

    def is_mian_thread() -> bool:
        return threading.current_thread() is threading.main_thread()

    def async_call(cistern: _Cistern):
        try:
            cistern.result = function_(*cistern.args, **cistern.kwargs)

        except Exception as e:
            cistern.exception = e

        finally:
            cistern.event.set()

    def call(*args, **kwargs):
        if not is_tk_alive() or is_mian_thread():
            return function_(*args, **kwargs)

        cistern = _Cistern()
        cistern.event = threading.Event()
        cistern.args = args
        cistern.kwargs = kwargs
    
        tkinter._get_default_root("mainwindow").after(0, async_call, cistern)
        cistern.event.wait()
        if cistern.exception is not None:
            raise cistern.exception

        else:
            return cistern.result

    return call


__all__ = ["tkrecall"]
