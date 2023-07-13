#!/usr/bin/env python3

"""An item collecting several "controls" which are checkboxes."""
from typing import List, Union, Optional
from app.cbx_control import CbxControl


class CbxItem():
    """A checkbox item, a collection of controls."""

    def __init__(self, shortcode: str, ordinal: int, name: str) -> None:
        """Create an item object."""
        self.shortcode = shortcode
        self.ordinal = ordinal
        self.name = name
        self.controls: List[CbxControl] = []

    def add_control(self, control: CbxControl) -> None:
        """Add a control to the item."""
        self.controls.append(control)

    def get_controls(self) -> List[CbxControl]:
        """Return a list of controls in this item."""
        return self.controls

    def to_dict(self) -> dict[str, Union[Optional[str], int, List[dict[str, Union[Optional[str], int, List[str], List[int]]]]]]:
        """Return this control as dict."""
        res: dict[str, Union[Optional[str], int, List[dict[str, Union[Optional[str], int, List[str], List[int]]]]]] = {"shortcode": self.shortcode,
                                                                                                                       "ordinal": self.ordinal,
                                                                                                                       "name": self.name,
                                                                                                                       "controls": []}
        for control in self.controls:
            if isinstance(res["controls"], list):
                res["controls"].append(control.to_dict())
        return res

    def pretty_print(self) -> None:
        """Pretty output for the control container."""
        out = f"""
        Item {self.shortcode}
        ***************
        Name: {self.name}

        """

        print(out)
