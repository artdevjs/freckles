# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import logging
import os
import sys

import click
import nsbl
from frkl import frkl

import yaml

from . import __version__ as VERSION
from .commands import CommandRepo
from .freckles_defaults import *

log = logging.getLogger("freckles")

# TODO: this is ugly, probably have refactor how role repos are used
nsbl.defaults.DEFAULT_ROLES_PATH = os.path.join(os.path.dirname(__file__), "external", "default_role_repo")
EXTRA_FRECKLES_PLUGINS = os.path.abspath(os.path.join(os.path.dirname(__file__), "external", "freckles_extra_plugins"))

FRECKLES_HELP_TEXT = "TO BE DONE"
FRECKLES_EPILOG_TEXT = "For more information please visit: https://freckles.io"

COMMAND_PROCESSOR_CHAIN = [
    frkl.UrlAbbrevProcessor()
]

# we need the current command to dynamically add it to the available ones
current_command = None
for arg in sys.argv[1:]:

    if arg.startswith("-"):
        continue

    if os.path.exists(arg):
        current_command = arg
        current_command_path = os.path.abspath(arg)
        # frkl_obj = frkl.Frkl(current_command, COMMAND_PROCESSOR_CHAIN)
        # current_command = frkl_obj.process()[0]
        break

if not current_command:
    current_command = None
    current_command_path = None

class FrecklesCommand(click.MultiCommand):

    def __init__(self, current_command, command_repos=[], **kwargs):

        click.MultiCommand.__init__(self, "freckles", **kwargs)

        output_option = click.Option(param_decls=["--output", "-o"], required=False, default="default", metavar="FORMAT", type=click.Choice(SUPPORTED_OUTPUT_FORMATS), help="format of the output")
        ask_become_pass_option = click.Option(param_decls=["--ask-become-pass"], help='whether to force ask for a password, force ask not to, or let try freckles decide (which might not always work)', type=click.Choice(["auto", "true", "false"]), default="true")

        self.params = [output_option, ask_become_pass_option]

        self.command_repo = CommandRepo(paths=command_repos, additional_commands=[current_command], no_run=False)
        self.current_command = current_command[0]
        self.command_names = self.command_repo.commands.keys()
        self.command_names.sort()
        if self.current_command:
            self.command_names.insert(0, self.current_command)

    def list_commands(self, ctx):

        return self.command_names

    def get_command(self, ctx, name):

        if name in self.command_repo.commands.keys():
            return self.command_repo.get_command(ctx, name)

        else:
            return None

cli = FrecklesCommand((current_command, current_command_path), help=FRECKLES_HELP_TEXT, epilog=FRECKLES_EPILOG_TEXT)

if __name__ == "__main__":
    cli()
