from datetime import timedelta

import click
from django.core.management import call_command
from django.utils import timezone

from pagesaver import __version__


@click.command("init")
@click.help_option("-h", "--help")
def init_command(*args, **kwargs):
    """Initialize PageSaver"""
    click.secho(f"[+] Initializing PageSaver v{__version__}...", fg="green")
    click.secho("{}\n".format("-" * 30), fg="green")

    click.secho("[+] Creating database and running initial migrations...", fg="green")
    call_command("migrate")

    click.secho("\n{}".format("-" * 30), fg="green")
    click.secho("[√] Init successfully.", fg="green")

    from pagesaver.authorization.models import APIToken

    expired = timezone.now().astimezone() + timedelta(days=365 * 100)
    token = APIToken.objects.create(expired=expired)
    click.echo(
        "Your API token: {token} (expired: {expired})".format(
            token=click.style(token.token, fg="blue"),
            expired=click.style(expired.strftime("%Y-%m-%d %H:%M:%S"), fg="red"),
        )
    )

    click.echo(
        """
{hint} To using PageSaver, Please install dependencies with the following command: 
    playwright install # browsers 
    playwright install-deps # dependencies to run browsers""".format(
            hint=click.style("Hint:", fg="magenta")
        )
    )

    click.echo(
        """
{hint} To start PageSaver, run: 
    pagesaver server # then visit http://127.0.0.1:8000
        """.format(
            hint=click.style("Hint:", fg="magenta")
        )
    )
