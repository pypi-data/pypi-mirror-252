#!/usr/bin/env python3
"""
action_trees CLI
"""

import click
from action_trees import __version__


@click.group()
def cli():
    pass  # pragma: no cover


@cli.command()
def info():
    """ Print package info """
    print(__version__)


cli.add_command(info)

if __name__ == "__main__":
    cli()  # pragma: no cover
