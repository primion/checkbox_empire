#!/usr/bin/env python3

"""A single checkbox item called "control"."""
from typing import List

class CbxControl():
    """A checkbox item."""

    def __init__(self, shortcode, ordinal, description, cwe, nist, requirement_matrix) -> None:
        """Create a control object."""

        self.shortcode = shortcode
        self.ordinal = ordinal
        self.description = description
        self.cwe:List(int) = cwe
        self.nist = nist

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
    def pretty_print(self):
        """ Pretty output for the control"""

        cwe =",".join([str(x) for x in self.cwe])
        nist = ",".join(self.nist)

        out = """            - {shortcode} {description} CWE: {cwe} NIST: {nist} """.format(shortcode = self.shortcode,
                   description = self.description,
                   cwe = cwe,
                   nist = nist
                   )

        print(out)