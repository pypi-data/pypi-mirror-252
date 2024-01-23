# -*- coding: utf-8 -*-

# (c) Meta Platforms, Inc. and affiliates.
#
# Fedora-License-Identifier: GPLv2+
# SPDX-2.0-License-Identifier: GPL-2.0+
# SPDX-3.0-License-Identifier: GPL-2.0-or-later
#
# This program is free software.
# For more information on the license, see COPYING.md.
# For more information on free software, see
# <https://www.gnu.org/philosophy/free-sw.en.html>.

import click
from . import (
    __version__,
)


@click.group("Main CLI")
def cli() -> None:
    """
    Tool for tracking packages of interest
    """


@cli.command(help="Display poi-tracker version information")
def version() -> None:
    """
    Display poi-tracker version information
    """
    click.echo(__version__)
