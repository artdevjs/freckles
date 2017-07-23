# -*- coding: utf-8 -*-

import logging
import os
import sys

import click

import yaml
from nsbl.nsbl import Nsbl

from . import __version__ as VERSION
from .commands import CommandRepo
from .freckles import freckles

log = logging.getLogger("freckles")

# @click.command()
# @click.option('--version', help='the version of freckles you are running', is_flag=True)
# @click.option('--ask-become-pass', help='whether to ask the user for a sudo password if necessary', is_flag=True, default=True)
# @click.option('--profile', help='only use one or multiple profiles, not all (if applicable)', multiple=True)
# @click.argument("repo_url", required=True, nargs=1)
# def cli(version, repo_url, profile, ask_become_pass):
#     """Freckles manages your dotfiles (and other aspects of your local machine).

#     For information about how to use and configure Freckles, please visit: XXX
#     """

#     if version:
#         click.echo(VERSION)
#         sys.exit(0)

#     runner = freckles(repo_url, profiles=profile)
#     runner.run(os.path.expanduser("~/.freckles/runs/"), force=True, ansible_verbose="", ask_become_pass=ask_become_pass, callback="nsbl_internal", display_sub_tasks=True, display_skipped_tasks=False)

# we need the current command to dynamically add it to the available ones
current_command = None
for arg in sys.argv[1:]:

    if arg.startswith("-"):
        continue

    current_command = arg
    break

class FrecklesCommand(click.MultiCommand):

    def __init__(self, current_command, command_repos=[], **kwargs):

        super(FrecklesCommand, self).__init__(kwargs)
        self.command_repo = CommandRepo(command_repos)
        self.current_command = current_command
        self.command_names = self.command_repo.commands.keys()
        if self.current_command:
            self.command_names.insert(0, self.current_command)

    def list_commands(self, ctx):

        return self.command_names

    def get_command(self, ctx, name):

        if name in self.command_repo.commands.keys():
            return self.command_repo.get_command(ctx, name)

        else:
            return None


cli = FrecklesCommand(current_command, help="Test")

if __name__ == "__main__":
    cli()
