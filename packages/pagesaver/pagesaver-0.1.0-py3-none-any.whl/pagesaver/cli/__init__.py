import click

from pagesaver import __version__

VERSION = rf"""
        ____                  _       _   _       _
        |  _ \ __ _  __ _  ___| |__   | | | |_   _| |__
        | |_) / _` |/ _` |/ _ \ '_ \  | |_| | | | | '_ \
        |  __/ (_| | (_| |  __/ | | | |  _  | |_| | |_) |
        |_|   \__,_|\__, |\___|_| |_| |_| |_|\__,_|_.__/
                    |___/

                    VERSION {__version__}
"""


@click.group()
@click.version_option(__version__, "-V", "--version", message=VERSION)
@click.help_option("-h", "--help")
def main():
    pass


from .export import export_command
from .init import init_command
from .server import server_command

main.add_command(export_command)
main.add_command(server_command)
main.add_command(init_command)