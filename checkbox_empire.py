#!/usr/bin/env python3

"""A tool to generate checkbox documents and collect data to also check some boxes."""

import argparse
from app.cbx_empire import CbxEmpire

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Manage compliance documents')
    # parser.add_argument('integers', metavar='N', type=int, nargs='+',
    #                    help='an integer for the accumulator')
    # parser.add_argument('--sum', dest='accumulate', action='store_const',
    #                    const=sum, default=max,
    #                    help='sum the integers (default: find the max)')

    args = parser.parse_args()

    cbe = CbxEmpire()
    # cbe.load_config("data/OWASP.Application.Security.Verification.Standard.4.0.3-en.json")
    # cbe.load_config("data/OWASP_ISVS-1.0RC.json")
    # cbe.load_config("data/OWASP_MASVS.yaml")
    cbe.load_config("config.toml")
    cbe.pretty_print()
    cbe.dump_to_toml("testfile.toml")
