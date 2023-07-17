#!/usr/bin/env python3

"""A tool to generate checkbox documents and collect data to also check some boxes."""

import argparse
from app.cbx_empire import CbxEmpire


def export(largs: argparse.Namespace) -> None:
    """Export data.

    :param largs: Argparse parsed arguments
    """
    cbe = CbxEmpire()
    cbe.load_config(largs.config)
    # cbe.pretty_print()
    if largs.toml:
        cbe.export_to_toml(largs.toml_file)


def show(largs: argparse.Namespace) -> None:
    """Show details for a specific element.

    :param largs: Argparse parsed arguments
    """
    cbe = CbxEmpire()
    cbe.load_config(largs.config)
    # cbe.pretty_print()

    cbx_control = cbe.find_control_by_uid(largs.uid)
    if cbx_control is not None:
        cbx_control.pretty_print()


def list_controls(largs: argparse.Namespace) -> None:
    """List controls.

    :param largs: Argparse parsed arguments
    """
    cbe = CbxEmpire()
    cbe.load_config(largs.config)

    cbe.print_control_list()


def mark_control(largs: argparse.Namespace) -> None:
    """Mark a  control.

    :param largs: Argparse parsed arguments
    """
    cbe = CbxEmpire()
    cbe.load_config(largs.config)
    cbe.mark_control(largs.uid, largs.state, largs.statement)

    cbe.save_toml_database()


def create_parser() -> argparse.ArgumentParser:
    """Create the command line parser.

    Required by sphinx-argparse to be in a separate def

    :returns: A command line parser
    """
    lparser = argparse.ArgumentParser(description='Manage compliance documents')
    lparser.add_argument('--config', type=str, default="config.toml", help='The main configuration file')
    subparsers = lparser.add_subparsers(help='sub-commands')

    # create the parser for the "export" command
    parser_export = subparsers.add_parser('export', help='Export generated data')
    parser_export.set_defaults(func=export)
    parser_export.add_argument('--toml', action="store_true", default=False, help='Export to toml')
    parser_export.add_argument('--toml_file', default="testfile.toml", help='File name of the toml file to write')

    # create the parser for the "show" command
    parser_show = subparsers.add_parser('show', help='Show control details')
    parser_show.set_defaults(func=show)
    parser_show.add_argument('uid', default=None, help='UID of the element to show details for')

    # create the parser for the "list" command
    parser_list = subparsers.add_parser('list', help='List controls')
    parser_list.set_defaults(func=list_controls)

    # create the parser for the "mark" command
    parser_mark = subparsers.add_parser('mark', help='Mark a control with a state and a comment')
    parser_mark.set_defaults(func=mark_control)
    parser_mark.add_argument('uid', default=None, help='UID of the element to mark')
    parser_mark.add_argument('state', default=None, help='State to write')
    parser_mark.add_argument('--statement', default="", help='Comment why this state is set')

    return lparser


if __name__ == "__main__":
    parser = create_parser()
    # TODO Add argcomplete
    args = parser.parse_args()

    args.func(args)

    # Parser commands:
    # export html

    # Add OWASP WSTG https://github.com/OWASP/wstg/blob/master/checklists/checklist.json
