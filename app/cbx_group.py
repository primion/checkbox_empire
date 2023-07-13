#!/usr/bin/env python3

"""A group collects several controls belonging to the same topic. A kind of document-subsection."""


from app.cbx_item import CbxItem
from typing import List, Union, Optional


class CbxGroup():
    """A group to collect control items."""

    def __init__(self, shortcode: str, ordinal: int, shortname: str, name: str) -> None:
        """Create a group object."""
        self.shortcode = shortcode
        self.ordinal: int = ordinal
        self.shortname = shortname
        self.name = name
        self.items:List[CbxItem] = []

    def add_item(self, item: CbxItem) -> None:
        """Add an item to the internal item list."""
        self.items.append(item)

    def to_dict(self) -> dict[str, Union[Optional[str], int, List[dict[str, Union[Optional[str], int, List[dict[str, Union[Optional[str], int, List[str], List[int]]]]]]]]]:
        """Return the item as a dict."""
        res: dict[str, Union[Optional[str], int, List[dict[str, Union[Optional[str], int, List[dict[str, Union[Optional[str], int, List[str], List[int]]]]]]]]] = {"shortcode": self.shortcode,
               "ordinal": self.ordinal,
               "shortname": self.shortname,
               "name": self.name,
               "items":[]}
        for item in self.items:
            if type(res["items"]) is list:
                res["items"].append(item.to_dict())
        return res

    def pretty_print(self) -> None:
        """Pretty print the group."""
        out = """
    Group {shortcode}  {shortname}
    ***************
    Name: {name}

        """.format(shortcode = self.shortcode,
                   shortname = self.shortname,
                   name = self.name,
                   )

        print(out)