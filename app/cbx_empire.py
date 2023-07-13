"""Master class to collect several checkbox sections and process them. Also generates reports."""

from typing import Any, Dict, List, Union, Optional

import tomlkit

from app.cbx_section import CbxSection


class CbxEmpire():
    """Master class of a checkbox empire."""

    def __init__(self) -> None:
        """Init empty checkbox empire class. Add sections by config or manually later."""
        self.sections: List[CbxSection] = []

    def load_config(self, filename: str) -> None:
        """Load configuration and create the project based on it."""
        with open(filename, "rt", encoding="UTF-8") as fh:
            data = tomlkit.load(fh)

            sections = data["sections"]

            for item in sections.items():  # type: ignore
                new_section = CbxSection(name=item[1]["name"],
                                         prefix=item[1]["prefix"],
                                         description=item[1]["description"])
                if item[1]["file_type"] == "OWASP_ASVS_JSON":
                    new_section.load_asvs_json(item[1]["data_file"])
                elif item[1]["file_type"] == "OWASP_ISVS_JSON":
                    new_section.load_isvs_json(item[1]["data_file"])
                elif item[1]["file_type"] == "OWASP_MASVS_YAML":
                    new_section.load_masvs_yaml(str(item[1]["data_file"]))

                self.sections.append(new_section)

    def pretty_print(self) -> None:
        """Do some pretty printing."""
        for section in self.sections:
            section.pretty_print()

    def to_dict(self) -> Dict[Any, Any]:
        """Convert data to dict."""
        data: dict[str, list[dict[str, Union[Optional[str], List[dict[str, Union[Optional[str], int, List[dict[str, Union[Optional[str], int, List[dict[str, Union[Optional[str], int, List[str], List[int]]]]]]]]]]]]]] = {"sections": []}
        for section in self.sections:
            data["sections"].append(section.to_dict())
        return data

    def dump_to_toml(self, filename: str) -> None:
        """Dump all the data to a toml file."""
        with open(filename, "wt", encoding="UTF-8") as fh:
            fh.write(tomlkit.dumps(self.to_dict()))
