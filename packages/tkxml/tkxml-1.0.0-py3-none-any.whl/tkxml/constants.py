# Licensed under the GNU LGPL v3
# Copyright (C) 2024 numlinka.

KEY_ID = "id"
KEY_MASTER = "master"
KEY_PSEUDO_CLASS = "class"
KEY_LAYOUT = "layout"
KEY_PACK = "pack"
KEY_PLACE = "place"
KEY_GRID = "grid"

KEYS_VERIABLE = ["Variable", "StringVar", "IntVar", "DoubleVar", "BooleanVar"]
KEYS_LAYOUT_PACK = ["after", "anchor", "before", "expand", "fill", "side", "ipadx", "ipady", "padx", "pady", "in_"]
KEYS_LAYOUT_PLACE = ["anchor", "bordermode", "width", "height", "x", "y", "relheight", "relwidth", "relx", "rely", "in_"]
KEYS_LAYOUT_GRID = ["column", "columnspan", "row", "rowspan", "ipadx", "ipady", "padx", "pady", "sticky", "in_"]
KEYS_LAYOUT = list(set(KEYS_LAYOUT_PACK + KEYS_LAYOUT_GRID))


__all__ = [x for x in globals() if not x.startswith("_")]
