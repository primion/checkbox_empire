#!/usr/bin/env python3

"""A section in the document. Collecting several checkbox tests."""

import json
from app.cbx_group import CbxGroup
from app.cbx_item import CbxItem
from app.cbx_control import CbxControl


class CbxSection():
    """Load data from a data file. This is a section in the document. A single data file can be loaded several times for different sections (for example use similar checklists for planning and testing)"""

    def __init__(self, name: str, prefix: str, description: str):
        """Create a section object."""
        self.manual_name = name
        self.manual_prefix = prefix
        self.manual_description = description

        # From data file
        self.data_name = None
        self.data_shortname = None
        self.data_version = None
        self.data_description = None

        self.groups = []

    def load_asvs_json(self, filename: str) -> None:
        """Load ASVS json."""
        with open(filename, "rt", encoding="utf-8") as fh:
            data = json.load(fh)
            self.data_name = data["Name"]
            self.data_shortname = data["ShortName"]
            self.data_version = data["Version"]
            self.data_description = data["Description"]

            for group_data in data["Requirements"]:
                new_group = CbxGroup(shortcode = group_data["Shortcode"],
                                     ordinal = group_data["Ordinal"],
                                     shortname = group_data["ShortName"],
                                     name = group_data["Name"])
                for item in group_data["Items"]:
                    new_item = CbxItem(shortcode = item["Shortcode"],
                                       ordinal = item["Ordinal"],
                                       name = item["Name"])
                    for control in item["Items"]:
                        new_control = CbxControl(shortcode = control["Shortcode"],
                                                 ordinal = control["Ordinal"],
                                                 description = control["Description"],
                                                 cwe = control["CWE"],
                                                 nist = control["NIST"],
                                                 requirement_matrix = {})
                        new_item.add_control(new_control)
                    new_group.add_item(new_item)
                self.groups.append(new_group)

    def to_dict(self):
        res = {"manual_name": self.manual_name,
                "manual_prefix": self.manual_prefix,
                "manual_description": self.manual_description,
                "data_name": self.data_name,
                "data_shortname": self.data_shortname,
                "data_version": self.data_version,
                "data_description": self.data_description,
                "groups": []}

        for group in self.groups:
            res["groups"].append(group.to_dict())

        return res

    def pretty_print(self):
        """ Print pretty to stdout """

        out = """
Section {mname}
***************
User-prefix: {mprefix}
User-description: {mdescription}

Data file
*********
Name: {name}
Shortname: {shortname}
Version: {version}
Description: {description}
        """.format(mname = self.manual_name,
                   mprefix = self.manual_prefix,
                   mdescription = self.manual_description,
                   name = self.data_name,
                   shortname = self.data_shortname,
                   version = self.data_version,
                   description = self.data_description)

        print(out)
        for g in self.groups:
            g.pretty_print()
            for i in g.items:
                i.pretty_print()
                for c in i.get_controls():
                    c.pretty_print()


