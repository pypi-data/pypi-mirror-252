#!/usr/bin/env python3

import os

from snakebids.app import SnakeBidsApp
from snakebids.cli import add_dynamic_args


def get_parser():
    """Exposes parser for sphinx doc generation, cwd is the docs dir"""
    app = SnakeBidsApp("../labelmerge", skip_parse_args=True)
    add_dynamic_args(
        app.parser, app.config["parse_args"], app.config["pybids_inputs"]
    )
    return app.parser


def main():
    app = SnakeBidsApp(os.path.abspath(os.path.dirname(__file__)))
    app.run_snakemake()


if __name__ == "__main__":
    main()
