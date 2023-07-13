#!/usr/bin/env python3

"""An item collecting several "controls" which are checkboxes."""
from typing import List
from app.cbx_control import CbxControl


class CbxItem():
    """A checkbox item, a collection of controls."""

    def __init__(self, shortcode, ordinal, name) -> None:
        """Create an item object."""
        self.shortcode = shortcode
        self.ordinal = ordinal
        self.name = name
        self.controls: List[CbxControl] = []

    def add_control(self, control: CbxControl):
        self.controls.append(control)

    def get_controls(self):
        return self.controls

    def to_dict(self):
        res = {"shortcode": self.shortcode,
               "ordinal": self.ordinal,
               "name": self.name,
               "controls": []}
        for control in self.controls:
            res["controls"].append(control.to_dict())
        return res

    def pretty_print(self):
        """ Pretty output for the control container """
        out = """
        Item {shortcode}
        ***************
        Name: {name}

        """.format(shortcode=self.shortcode,
                   name=self.name,
                   )

        print(out)
