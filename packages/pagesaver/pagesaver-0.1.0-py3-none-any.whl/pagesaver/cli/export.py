from pathlib import Path

import click

from pagesaver.cli.types import MultipleChoice
from pagesaver.constants import SUPPORT_FORMATS
from pagesaver.enums import ExportFormat
from pagesaver.utils import export_utils

SUCCESS_ANSI = click.style("successfully", fg="green")


@click.command("export")
@click.argument("url", type=click.STRING)
@click.option(
    "-f",
    "--format",
    "format",
    required=True,
    type=MultipleChoice(SUPPORT_FORMATS, case_sensitive=False),
    help="Format which you want to export",
)
@click.option(
    "-o",
    "--output",
    "output",
    required=True,
    type=click.Path(writable=True, dir_okay=True, file_okay=False),
    help="Output directory of the file",
)
@click.option(
    "-n",
    "--name",
    "name",
    required=False,
    default="exported",
    show_default=True,
    type=click.STRING,
    help="Name of the exported file",
)
@click.help_option("-h", "--help")
@click.pass_context
def export_command(ctx, url, format, output, name):
    """Export page to the output file"""
    path_lst, _ = export_utils.export(
        url, Path(output).absolute() / name, [ExportFormat(i) for i in format]
    )
    click.echo(f"Exported {SUCCESS_ANSI}:")
    for path in path_lst:
        click.echo(f"  - {path['format']}: {path['path']}")
