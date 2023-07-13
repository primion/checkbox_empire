#!/usr/bin/env python3

"""A single checkbox item called "control"."""
from typing import List, Dict, Any, Union, Sequence
from enum import Enum

class State(Enum):
    """ State of the checkbox """

    UNCHECKED = "unchecked"
    CHECKED = "checked"
    NOT_RELEVANT = "not_relevant"


class CbxControl():
    """A checkbox item."""

    def __init__(self, shortcode: str, ordinal: int, description: str, cwe: List[int], nist: List[str], requirement_matrix: Dict[Any, Any], statement: str="", section_prefix: str = "") -> None:
        """Create a control object."""

        self.shortcode = shortcode
        self.ordinal: int = ordinal
        self.description = description
        self.cwe:List[int] = cwe
        self.nist: List[str] = nist
        self.state:State = State.UNCHECKED
        self.statement = statement
        self.section_prefix = section_prefix

        # TODO manage requirement matrix

        """
              "L1": {
                "Required": false,
                "Requirement": ""
              },
              "L2": {
                "Required": true,
                "Requirement": ""
              },
              "L3": {
                "Required": true,
                "Requirement": ""
              },
        """

    def get_uid(self) -> str:
        """ Get unique ID """
        return self.section_prefix + "-" + self.shortcode


    def to_dict(self) -> dict[str, Sequence[object]]:
        res = {"shortcode": self.shortcode,
               "ordinal": self.ordinal,
               "description": self.description,
               "CWE": self.cwe,
               "NIST": self.nist,
               "state": self.state.name,
               "statement": self.statement,
               "uid": self.get_uid()}
        return res

    def pretty_print(self) -> None:
        """ Pretty output for the control"""

        cwe =",".join([str(x) for x in self.cwe])
        nist = ",".join(self.nist)

        out = """            - :{uid}: {shortcode} {description} {statement} CWE: {cwe} NIST: {nist} """.format(shortcode = self.shortcode,
                   description = self.description,
                   cwe = cwe,
                   nist = nist,
                   statement = self.statement,
                   uid = self.get_uid()
                   )

        print(out)