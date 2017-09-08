# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

from .utils import FRECKLES_REPO, FRECKLES_URL
import click

__author__ = """Markus Binsteiner"""
__email__ = 'makkus@posteo.net'
__version__ = '0.1.115'

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(__version__)
    ctx.exit()
