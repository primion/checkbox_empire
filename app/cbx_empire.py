"""Master class to collect several checkbox sections and process them. Also generates reports."""

from typing import List
from app.cbx_section import CbxSection
import tomlkit


class CbxEmpire():
    """Master class of a checkbox empire."""

    def __init__(self) -> None:
        """Init empty checkbox empire class. Add sections by config or manually later."""
        self.sections: List[CbxSection] = []

    def load_config(self, filename: str) -> None:
        """Load configuration and create the project based on it."""
        # TODO: Proper config loader
        new_section = CbxSection("ASVS for planning", "ASVS_PLAN", "Using ASVS list for planning")
        new_section.load_asvs_json(filename)
        self.sections.append(new_section)

    def pretty_print(self):
        """ Do some pretty printing """

        for s in self.sections:
            s.pretty_print()

    def to_dict(self):
        """ Convert data to dict """
        data = {"sections":[]}
        for section in self.sections:
            data["sections"].append(section.to_dict())
        return data

    def dump_to_toml(self, filename):
        """ Dump all the data to a toml file """
        with open(filename, "wt") as fh:
            fh.write(tomlkit.dumps(self.to_dict()))