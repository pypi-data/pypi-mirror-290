# Licensed under the GNU LGPL v3
# Copyright (C) 2024 numlinka.

__name__ = "tkxml"
__author__ = "numlinka"
__license__ = "LGPL 3.0"
__copyright__ = "Copyright (C) 2024 numlinka"

__version_info__ = (1, 0, 0)
__version__ = ".".join(map(str, __version_info__))

from . import namespace
from . import constants
from . import settings
from . import decorators
from .tkxmlhandle import TkXMLHandle


__all__ = [
    "TkXMLHandle",
    "namespace",
    "constants",
    "settings",
    "decorators"
]
