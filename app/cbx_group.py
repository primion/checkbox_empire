#!/usr/bin/env python3

"""A group collects several controls belonging to the same topic. A kind of document-subsection."""


from app.cbx_item import CbxItem
from typing import List, Union, Optional


class CbxGroup():
    """A group to collect control items."""

    def __init__(self, shortcode: str, ordinal: int, shortname: str, name: str) -> None:
        """Create a group object.

        :param shortcode: The code for this group
        :param ordinal: The counter for this group
        :param shortname: A short name for this group
        :param name: A long name for this group
        """
        self.shortcode = shortcode
        self.ordinal: int = ordinal
        self.shortname = shortname
        self.name = name
        self.items:List[CbxItem] = []

    def add_item(self, item: CbxItem) -> None:
        """Add an item to the internal item list.

        :param item: The item to add
        """
        self.items.append(item)

    def to_dict(self) -> dict[str, Union[Optional[str], int, List[dict[str, Union[Optional[str], int, List[dict[str, Union[Optional[str], int, List[str], List[int]]]]]]]]]:
        """Return the item as a dict.

        :returns: A dict containing the core data of this class
        """
        res: dict[str, Union[Optional[str], int, List[dict[str, Union[Optional[str], int, List[dict[str, Union[Optional[str], int, List[str], List[int]]]]]]]]] = {"shortcode": self.shortcode,
               "ordinal": self.ordinal,
               "shortname": self.shortname,
               "name": self.name,
               "item_list":[]}
        for item in self.items:
            if type(res["item_list"]) is list:
                res["item_list"].append(item.to_dict())
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

    def get_items(self) -> list[CbxItem]:
        """Return a list of items in this group.

        :returns: A list of items in this group
        """
        return self.items