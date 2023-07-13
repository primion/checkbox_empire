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
        with open(filename, "rt") as fh:
            data = tomlkit.load(fh)
            print(data)
            for cs_name in data["sections"].keys():
                # data["sections"][cs_name]["data_file"]
                new_section = CbxSection(name=data["sections"][cs_name]["name"],
                                         prefix=data["sections"][cs_name]["prefix"],
                                         description=data["sections"][cs_name]["description"])
                if data["sections"][cs_name]["file_type"] == "OWASP_ASVS_JSON":
                    new_section.load_asvs_json(data["sections"][cs_name]["data_file"])
                elif data["sections"][cs_name]["file_type"] == "OWASP_ISVS_JSON":
                    new_section.load_isvs_json(data["sections"][cs_name]["data_file"])
                elif data["sections"][cs_name]["file_type"] == "OWASP_MASVS_YAML":
                    new_section.load_masvs_yaml(data["sections"][cs_name]["data_file"])
                # new_section.load_masvs_yaml(data["sections"][cs_name]["data_file"])

                self.sections.append(new_section)

    def pretty_print(self):
        """ Do some pretty printing """

        for s in self.sections:
            s.pretty_print()

    def to_dict(self):
        """ Convert data to dict """
        data = {"sections": []}
        for section in self.sections:
            data["sections"].append(section.to_dict())
        return data

    def dump_to_toml(self, filename):
        """ Dump all the data to a toml file """
        with open(filename, "wt") as fh:
            fh.write(tomlkit.dumps(self.to_dict()))
