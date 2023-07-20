"""Master class to collect several checkbox sections and process them. Also generates reports."""

import re
from typing import Any, Dict, List, Optional, Union

import tomlkit
from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.cbx_control import CbxControl
from app.cbx_section import CbxSection

# Project offers logins
required_tags: dict[str, list[Any]] = {"login": ["OWASP_ASVS-V2.1.1", "OWASP_ASVS-V2.1.2", "OWASP_ASVS-V2.1.3", "OWASP_ASVS-V2.1.4", "OWASP_ASVS-V2.1.5", "OWASP_ASVS-V2.1.6", "OWASP_ASVS-V2.1.7", "OWASP_ASVS-V2.1.8", "OWASP_ASVS-V2.1.9", "OWASP_ASVS-V2.1.10", "OWASP_ASVS-V2.1.11", "OWASP_ASVS-V2.1.12", "OWASP_ASVS-V2.2.1", "OWASP_ASVS-V2.2.2", "OWASP_ASVS-V2.2.3", "OWASP_ASVS-V2.2.4", "OWASP_ASVS-V2.2.5", "OWASP_ASVS-V2.2.6", "OWASP_ASVS-V2.2.7", "OWASP_ASVS-V2.3.1", "OWASP_ASVS-V2.3.2", "OWASP_ASVS-V2.3.3", "OWASP_ASVS-V2.4.1", "OWASP_ASVS-V2.4.2", "OWASP_ASVS-V2.4.3", "OWASP_ASVS-V2.4.4", "OWASP_ASVS-V2.4.5", "OWASP_ASVS-V2.5.1", "OWASP_ASVS-V2.5.2", "OWASP_ASVS-V2.5.3", "OWASP_ASVS-V2.5.4", "OWASP_ASVS-V2.5.5", "OWASP_ASVS-V2.5.6", "OWASP_ASVS-V2.5.7", "OWASP_ASVS-V2.6.1", "OWASP_ASVS-V2.6.2", "OWASP_ASVS-V2.6.3", "OWASP_ASVS-V2.7.1", "OWASP_ASVS-V2.7.2", "OWASP_ASVS-V2.7.3", "OWASP_ASVS-V2.7.4", "OWASP_ASVS-V2.7.5", "OWASP_ASVS-V2.7.6", "OWASP_ASVS-V2.8.1", "OWASP_ASVS-V2.8.2", "OWASP_ASVS-V2.8.3", "OWASP_ASVS-V2.8.4", "OWASP_ASVS-V2.8.5", "OWASP_ASVS-V2.8.6", "OWASP_ASVS-V2.8.7", "OWASP_ASVS-V2.9.1", "OWASP_ASVS-V2.9.2", "OWASP_ASVS-V2.9.3", "OWASP_ASVS-V2.10.1", "OWASP_ASVS-V2.10.2", "OWASP_ASVS-V2.10.3", "OWASP_ASVS-V2.10.4",],
                                       # Project offers file uploads
                                       "file_upload": ["OWASP_ASVS-V12.1.1", "OWASP_ASVS-V12.1.2", "OWASP_ASVS-V12.1.3",],
                                       # Project offers file downloads
                                       "file_download": ["OWASP_ASVS-V12.5.1", "OWASP_ASVS-V12.5.2"],
                                       # Project uses GraphQL
                                       "graphql": ["OWASP_ASVS-V13.4.1", "OWASP_ASVS-V13.4.2", "OWASP_WSTG-195", "OWASP_WSTG-196", "OWASP_WSTG-197"],
                                       # Project uses http or https as web or API interface
                                       "http_or_https": ["OWASP_ASVS-V14.3.3", "OWASP_ASVS-V5.1.1", "OWASP_ASVS-V5.2.1", "OWASP_ASVS-V8.3.1", "OWASP_ASVS-V9.1.1", "OWASP_ASVS-V9.1.2", "OWASP_ASVS-V9.1.3", "OWASP_ASVS-V9.2.1", "OWASP_ASVS-V9.2.2", "OWASP_ASVS-V9.2.3", "OWASP_ASVS-V9.2.4", "OWASP_ASVS-V9.2.5", "OWASP_ASVS-V13.1.3", "OWASP_ASVS-V13.1.4", " OWASP_ASVS-V13.1.5", "OWASP_ASVS-V13.2.1", "OWASP_ASVS-V13.2.2", "OWASP_ASVS-V13.2.3", "OWASP_ASVS-V13.2.4", "OWASP_ASVS-V13.2.5", "OWASP_ASVS-V13.2.6", "OWASP_ASVS-V14.4.1", "OWASP_ASVS-V14.4.2", "OWASP_ASVS-V14.4.3", "OWASP_ASVS-V14.4.4", "OWASP_ASVS-V14.4.5", "OWASP_ASVS-V14.4.6", "OWASP_ASVS-V14.4.7", "OWASP_ASVS-V14.5.1", "OWASP_ASVS-V14.5.2", "OWASP_ASVS-V14.5.3", "OWASP_ASVS-V14.5.4"],
                                       # Uses a database (SQL, graphql, json, xml...)
                                       "database": ["OWASP_ASVS-V13.4.1", "OWASP_ASVS-V13.4.2", "OWASP_WSTG-195", "OWASP_WSTG-196", "OWASP_WSTG-197", "OWASP_ASVS-V5.3.4", "OWASP_ASVS-V5.3.5", "OWASP_ASVS-V5.3.6", "OWASP_ASVS-V5.3.10", "OWASP_ASVS-V5.5.2", "OWASP_ASVS-V5.5.4", "OWASP_ASVS-V6.1.1", "OWASP_ASVS-V6.1.2", "OWASP_ASVS-V6.1.3"],
                                       # keep deleted and duplicate entries
                                       "keep_deleted": ["OWASP_ASVS-V1.4.2", "OWASP_ASVS-V1.4.3", "OWASP_ASVS-V1.12.1", "OWASP_ASVS-V4.1.4", "OWASP_ASVS-V7.3.2", "OWASP_ASVS-V13.1.2", "OWASP_ASVS-V13.2.4", "OWASP_ASVS-V14.3.1"],
                                       # IoT: project contains IoT or is at least connected to one
                                       "iot": [re.compile("^OWASP_ISVS.*")],
                                       # mobile application: runs on a mobile phone or similar
                                       "mobile": [re.compile("^OWASP_MASVS.*")],
                                       # web technology (using a web page)
                                       "web": [re.compile("^OWASP_WSTG.*"), "OWASP_ASVS-V14.3.2"],
                                       # SOAP API technology being used or provided
                                       "soap": ["OWASP_ASVS-V13.3.1", "OWASP_ASVS-V13.3.2"],
                                       # REST API being used or provided ?
                                       "rest": [re.compile(r"OWASP_ASVS-V13.2.\d{1,2}.*")],
                                       # SQL being used as database ?
                                       "sql": ["OWASP_ASVS-V5.3.4", "OWASP_ASVS-V5.3.5", "OWASP_MASVS-MASVS-CODE-4", "OWASP_WSTG-1ae57a55d2ec89263111e2c90548239f", "OWASP_WSTG-e1a2c57dab62c521836cce08625f5607"],
                                       # XML being used for data storage or transfer ?
                                       "xml": ["OWASP_ASVS-V5.3.10", "OWASP_ASVS-V5.5.2", "OWASP_ASVS-V5.5.3", "OWASP_ASVS-V13.3.1", "OWASP_WSTG-04fd8451791bc8adaae066bcfe127c51", "OWASP_WSTG-ce3b74688e3058a250ee977d07ddddfe"]
                                       }


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

            #  For the Mypy ignore: It is a list. Better checks are possible when using pydantic. This is planned
            tags: List[Any] = data["project_tags"]   # type: ignore
            for tag in tags:
                if tags[tag] is False:
                    for uid in required_tags[tag]:
                        if isinstance(uid, str):
                            self.mark_control(uid, "not_relevant", "Project does not require that. See project tags")
                            print(f"Setting as irrelevant because {tag} is false: {uid}")
                        elif isinstance(uid, re.Pattern):
                            for control_uid in self.list_all_control_uids():
                                if uid.search(control_uid) is not None:
                                    self.mark_control(control_uid, "not_relevant", "Project does not require that. See project tags")

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

    def list_all_control_uids(self) -> List[str]:
        """Return a list of all uids used for controls."""
        res = []
        for section in self.sections:
            for group in section.get_groups():
                for item in group.get_items():
                    for control in item.get_controls():
                        res.append(control.get_uid())
        return res

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
