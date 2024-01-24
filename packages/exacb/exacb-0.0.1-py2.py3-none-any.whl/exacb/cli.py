# --------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2024 Jayesh Badwaik <j.badwaik@fz-juelich.de>
# --------------------------------------------------------------------------------------------------
import click
import exacb

@click.group(context_settings={'help_option_names': ['-h', '--help']},invoke_without_command=True)
@click.version_option(version=exacb.metadata.__version__, prog_name='exacb')
@click.pass_context
def main(ctx: click.Context):
    click.echo("Hello, World!")
