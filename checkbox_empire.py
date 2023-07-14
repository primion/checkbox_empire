#!/usr/bin/env python3

"""A tool to generate checkbox documents and collect data to also check some boxes."""

import argparse
from app.cbx_empire import CbxEmpire


def export(largs: argparse.Namespace) -> None:
    """Export data."""
    cbe = CbxEmpire()
    cbe.load_config(largs.config)
    # cbe.pretty_print()
    if largs.toml:
        cbe.export_to_toml(largs.toml_file)


def show(largs: argparse.Namespace) -> None:
    """Show details for a specific element."""
    cbe = CbxEmpire()
    cbe.load_config(largs.config)
    # cbe.pretty_print()

    cbx_control = cbe.find_control_by_uid(largs.uid)
    if cbx_control is not None:
        cbx_control.pretty_print()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Manage compliance documents')
    parser.add_argument('--config', type=str, default="config.toml", help='an integer for the accumulator')
    subparsers = parser.add_subparsers(help='sub-commands')

    # create the parser for the "export" command
    parser_export = subparsers.add_parser('export', help='Export generated data')
    parser_export.set_defaults(func=export)
    parser_export.add_argument('--toml', action="store_true", default=False, help='export to toml')
    parser_export.add_argument('--toml_file', default="testfile.toml", help='file name of the toml file to write')

    # create the parser for the "show" command
    parser_show = subparsers.add_parser('show', help='show control details')
    parser_show.set_defaults(func=show)
    parser_show.add_argument('uid', default=None, help='uid of the element to show details for')

    args = parser.parse_args()

    args.func(args)
    # TODO: Sphinx documentation for arguments

    # Parser commands:
    # export html
    # mark item
    # list
