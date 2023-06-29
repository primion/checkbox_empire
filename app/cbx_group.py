#!/usr/bin/env python3

from app.cbx_item import CbxItem
from typing import List

"""A group collects several controls belonging to the same topic. A kind of document-subsection."""


class CbxGroup():
    """A group to collect control items."""

    def __init__(self, shortcode, ordinal, shortname, name) -> None:
        """Create a group object."""
        self.shortcode = shortcode
        self.ordinal = ordinal
        self.shortname = shortname
        self.name = name
        self.items:List[CbxItem] = []

    def add_item(self, item: CbxItem):
        """ Adds an item to the internal item list """
        self.items.append(item)

    def pretty_print(self):
        """ Pretty print the group """
        out = """
    Group {shortcode}  {shortname}
    ***************
    Name: {name}

        """.format(shortcode = self.shortcode,
                   shortname = self.shortname,
                   name = self.name,
                   )

        print(out)