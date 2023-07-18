"""Master class to collect several checkbox sections and process them. Also generates reports."""

from typing import Any, Dict, List, Union, Optional

import tomlkit
from jinja2 import Environment, select_autoescape, FileSystemLoader

from app.cbx_section import CbxSection
from app.cbx_control import CbxControl


class CbxEmpire():
    """Master class of a checkbox empire."""

    def __init__(self) -> None:
        """Init empty checkbox empire class. Add sections by config or manually later."""
        self.sections: List[CbxSection] = []
        self.database_file_toml: Optional[str] = None
        self.config_file: Optional[str] = None
        self.project: Optional[str] = None

    def load_config(self, filename: str) -> None:
        """Load configuration and create the project based on it.

        :param filename: The name of the main config file to load
        """
        with open(filename, "rt", encoding="UTF-8") as fh:
            data = tomlkit.load(fh)

            if "database_file_toml" in data:
                self.database_file_toml = str(data["database_file_toml"])
            self.config_file = filename
            self.project = str(data["project"])

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
                elif item[1]["file_type"] == "OWASP_WSTG_JSON":
                    new_section.load_wstg_json(str(item[1]["data_file"]))

                self.sections.append(new_section)

        # Load project specific states for the controls
        self.load_toml_database()

    def load_toml_database(self) -> None:
        """Load the database assigning states to controls."""
        if self.database_file_toml is not None:
            with open(self.database_file_toml, "rt", encoding="UTF-8") as fh:
                data = tomlkit.load(fh)
                if "controls" in data:
                    for control in data.item("controls"):   # type: ignore
                        self.mark_control(control["uid"], control["state"], control["statement"])

    def save_toml_database(self) -> None:
        """Save the database assigning states to controls."""
        if self.database_file_toml is not None:
            data: dict[str, list[dict[str, str]]] = {"controls": []}
            for section in self.sections:
                for group in section.get_groups():
                    for item in group.get_items():
                        for control in item.get_controls():
                            data["controls"].append({"uid": control.get_uid(),
                                                     "state": control.state.value,
                                                     "statement": control.statement or ""})
            with open(self.database_file_toml, "wt", encoding="UTF-8") as fh:
                tomlkit.dump(data, fh)

    def pretty_print(self) -> None:
        """Do some pretty printing."""
        for section in self.sections:
            section.pretty_print()

    def to_dict(self) -> Dict[Any, Any]:
        """Convert data to dict.

        :returns: A dict containing the core data of this class
        """
        data: dict[str, list[dict[str, Union[Optional[str], List[dict[str, Union[Optional[str], int, List[dict[str, Union[Optional[str], int, List[dict[str, Union[Optional[str], int, List[str], List[int]]]]]]]]]]]]]] = {"sections": []}
        for section in self.sections:
            data["sections"].append(section.to_dict())
        return data

    def export_to_toml(self, filename: str) -> None:
        """Dump all the data to a toml file.

        :param filename: The name of the toml to write
        """
        with open(filename, "wt", encoding="UTF-8") as fh:
            fh.write(tomlkit.dumps(self.to_dict()))

    def find_control_by_uid(self, uid: str) -> Optional[CbxControl]:
        """Find and return a control by uid.

        :param uid: the UID of the element to find
        :returns: A control or None
        """
        for section in self.sections:
            for group in section.get_groups():
                for item in group.get_items():
                    for control in item.get_controls():
                        if control.get_uid() == uid:
                            return control
        return None

    def print_control_list(self) -> None:
        """Find and return a control by uid."""
        for section in self.sections:
            for group in section.get_groups():
                for item in group.get_items():
                    for control in item.get_controls():
                        text = control.statement or control.description
                        print(f"[{control.state.name}] {control.get_uid()}\t  {text}\t ")

    def mark_control(self, uid: str, state: str, statement: str = "") -> None:
        """Set the state of a control defined by uid.

        :param uid: the UID of the element to mark
        :param state: The state to set.
        :param statement: A statement describing why the state has been set that way
        """
        control = self.find_control_by_uid(uid)
        if control is not None:
            control.set_state(state, statement)

    def generate_html_report(self, template_file: str, outfile: str) -> None:
        """Generate a html report."""
        env = Environment(loader=FileSystemLoader("."),
                          autoescape=select_autoescape()
                          )
        template = env.get_template(template_file)
        with open(outfile, "wt", encoding="utf-8") as fh:
            fh.write(template.render(data=self.to_dict()))
