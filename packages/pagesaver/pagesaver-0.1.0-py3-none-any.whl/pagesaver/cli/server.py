import asyncio

import click
from hypercorn.asyncio import serve
from hypercorn.config import Config

from pagesaver.core.asgi import application
from pagesaver.settings import pagesaver_settings


@click.command("server")
@click.help_option("-h", "--help")
@click.option(
    "-b",
    "--bind",
    "bind",
    show_default=True,
    default=pagesaver_settings.SERVER_BIND,
    help="The TCP host/address to bind to.",
)
def server_command(*args, **kwargs):
    """Run PageSaver HTTP server"""
    config = Config.from_mapping({"bind": pagesaver_settings.SERVER_BIND}, **kwargs)
    asyncio.run(serve(application, config))
