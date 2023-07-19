#!/usr/bin/env python3

"""A section in the document. Collecting several checkbox tests."""

import json
from typing import Optional, List, Union
import hashlib

import yaml

from app.cbx_control import CbxControl
from app.cbx_group import CbxGroup
from app.cbx_item import CbxItem


class CbxSection():
    """Load data from a data file. This is a section in the document. A single data file can be loaded several times for different sections (for example use similar checklists for planning and testing)."""

    def __init__(self, name: str, prefix: str, description: str):
        """Create a section object.

        A section represents a checklist like ASVS, MASVS or similar with several groups, items and controls.

        :param name: The name of the section
        :param prefix: The unique prefix of the section
        :param description: the description of the section
        """
        self.manual_name: Optional[str] = name
        self.manual_prefix: Optional[str] = prefix
        self.manual_description: Optional[str] = description

        # From data file
        self.data_name: Optional[str] = None
        self.data_shortname: Optional[str] = None
        self.data_version: Optional[str] = None
        self.data_description: Optional[str] = None

        self.groups: list[CbxGroup] = []

    def load_masvs_yaml(self, filename: str) -> None:
        """Load MASVS style yaml files.

        :param filename: the name of the masvs as a yaml file
        """
        with open(filename, "rt", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
            self.data_name = data["metadata"]["title"]
            self.data_shortname = data["metadata"]["remarks"]
            self.data_version = data["metadata"]["version"]
            self.data_description = ""

            item_count = 0

            for group in data["groups"]:
                new_group = CbxGroup(shortcode=group["id"],
                                     ordinal=int(group["index"]),
                                     shortname=group["title"],
                                     name=group["description"])

                new_item = CbxItem(shortcode="None",
                                   ordinal=item_count,
                                   name="None")

                item_count += 1

                for control in group["controls"]:
                    new_control = CbxControl(shortcode=control["id"],
                                             ordinal=0,
                                             description=control["description"],
                                             cwe=[],
                                             nist=[],
                                             requirement_matrix={},
                                             statement=control["statement"],
                                             section_prefix=self.manual_prefix)
                    new_item.add_control(new_control)
                new_group.add_item(new_item)
                self.groups.append(new_group)

    def load_isvs_json(self, filename: str) -> None:
        """Load ISVS style json.

        :param filename: the name of the isvs as a json document
        """
        self.data_name = "None"
        self.data_shortname = "None"
        self.data_version = "None"
        self.data_description = "None"

        group_count = 0
        item_count = 0
        control_count = 0

        with open(filename, "rt", encoding="utf-8") as fh:
            data = json.load(fh)
            new_group = CbxGroup(shortcode="None",
                                 ordinal=group_count,
                                 shortname="None",
                                 name="None")
            group_count += 1
            new_item = CbxItem(shortcode="None",
                               ordinal=item_count,
                               name="None")
            item_count += 1

            for control in data:
                new_control = CbxControl(shortcode=control["ID"],
                                         ordinal=control_count,
                                         description=control["Description"],
                                         cwe=[],
                                         nist=[],
                                         requirement_matrix={},
                                         section_prefix=self.manual_prefix)
                control_count += 1
                new_item.add_control(new_control)

            new_group.add_item(new_item)
            self.groups.append(new_group)

    def load_asvs_json(self, filename: str) -> None:
        """Load ASVS json.

        :param filename: The filename of the asvs as a json document
        """
        with open(filename, "rt", encoding="utf-8") as fh:
            data = json.load(fh)
            self.data_name = data["Name"]
            self.data_shortname = data["ShortName"]
            self.data_version = data["Version"]
            self.data_description = data["Description"]

            for group_data in data["Requirements"]:
                new_group = CbxGroup(shortcode=group_data["Shortcode"],
                                     ordinal=group_data["Ordinal"],
                                     shortname=group_data["ShortName"],
                                     name=group_data["Name"])
                for item in group_data["Items"]:
                    new_item = CbxItem(shortcode=item["Shortcode"],
                                       ordinal=item["Ordinal"],
                                       name=item["Name"])
                    for control in item["Items"]:
                        new_control = CbxControl(shortcode=control["Shortcode"],
                                                 ordinal=control["Ordinal"],
                                                 description=control["Description"],
                                                 cwe=control["CWE"],
                                                 nist=control["NIST"],
                                                 requirement_matrix={},
                                                 section_prefix=self.manual_prefix)
                        new_item.add_control(new_control)
                    new_group.add_item(new_item)
                self.groups.append(new_group)

    def load_wstg_json(self, filename: str) -> None:
        """Load WSTG json.

        :param filename: The filename of the wstg as a json document
        """
        with open(filename, "rt", encoding="utf-8") as fh:
            data = json.load(fh)
            self.data_name = "WSTG json"
            self.data_shortname = "WSTGj"
            self.data_version = ""
            self.data_description = ""

            group_ordinal = 0
            test_ordinal = 0
            control_ordinal = 0

            for group in data["categories"].keys():
                new_group = CbxGroup(shortcode=data["categories"][group]["id"],
                                     ordinal=group_ordinal,
                                     shortname=group,
                                     name=group)
                group_ordinal += 1
                for item in data["categories"][group]["tests"]:
                    new_item = CbxItem(shortcode=item["id"],
                                       ordinal=test_ordinal,
                                       name=item["name"])
                    test_ordinal += 1
                    for control in item["objectives"]:
                        new_control = CbxControl(shortcode=hashlib.md5(bytes(control, encoding="utf-8")).hexdigest(),
                                                 ordinal=control_ordinal,
                                                 description=control,
                                                 cwe=[],
                                                 nist=[],
                                                 requirement_matrix={},
                                                 section_prefix=self.manual_prefix)
                        control_ordinal += 1
                        new_item.add_control(new_control)
                    new_group.add_item(new_item)
                self.groups.append(new_group)

    def to_dict(self) -> dict[str, Union[Optional[str], List[dict[str, Union[Optional[str], int, List[dict[str, Union[Optional[str], int, List[dict[str, Union[Optional[str], int, List[str], List[int]]]]]]]]]]]]:
        """Return class attributes as dict.

        :returns: A dict containing the core data of this class
        """
        res: dict[str, Union[Optional[str], List[dict[str, Union[Optional[str], int, List[dict[str, Union[Optional[str], int, List[dict[str, Union[Optional[str], int, List[str], List[int]]]]]]]]]]]] = {"manual_name": self.manual_name,
                                                                                                                                                                                                          "manual_prefix": self.manual_prefix,
                                                                                                                                                                                                          "manual_description": self.manual_description,
                                                                                                                                                                                                          "data_name": self.data_name,
                                                                                                                                                                                                          "data_shortname": self.data_shortname,
                                                                                                                                                                                                          "data_version": self.data_version,
                                                                                                                                                                                                          "data_description": self.data_description,
                                                                                                                                                                                                          "groups": []}

        for group in self.groups:
            if isinstance(res["groups"], list):
                res["groups"].append(group.to_dict())

        return res

    def pretty_print(self) -> None:
        """Print pretty to stdout."""
        out = f"""
Section {self.manual_name}
***************
User-prefix: {self.manual_prefix}
User-description: {self.manual_description}

Data file
*********
Name: {self.data_name}
Shortname: {self.data_shortname}
Version: {self.data_version}
Description: {self.data_description}
        """

        print(out)
        for group in self.groups:
            group.pretty_print()
            for item in group.items:
                item.pretty_print()
                for control in item.get_controls():
                    control.pretty_print()

    def get_groups(self) -> list[CbxGroup]:
        """Return a list of groups."""
        return self.groups
