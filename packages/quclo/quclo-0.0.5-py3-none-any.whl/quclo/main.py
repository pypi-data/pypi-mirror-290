"""Main module for the QuClo CLI."""

from importlib.metadata import version as get_version
from pathlib import Path
import click
from quclo.user import User
from quclo.execution import Execution
from quclo.circuit import Circuit
from quclo.backend import Backend
from quclo.config import Config
from quclo.models import Priority
from quclo.utils import run_file_with_proxy


@click.group()
def cli():
    """QuClo CLI."""
    pass


@cli.group()
def create():
    """Create resources."""
    pass


@cli.group()
def get():
    """Get resources."""
    pass


@cli.group()
def edit():
    """Edit resources."""
    pass


@cli.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option("--id", help="ID of the circuit")
@click.option(
    "--token",
    default=Config.load_token(),
    help="Token for the user",
    required=True,
)
def run(filename: str | None, id: str | None, token: str):
    """Run a file or circuit."""
    if filename and id:
        raise click.ClickException("Cannot specify both filename and ID")
    if not filename and not id:
        raise click.ClickException("Either filename or ID is required")
    if filename:
        click.echo(f"Running file: {filename}")
        run_file_with_proxy(file=filename, token=token)
    else:
        click.echo(f"Running circuit with ID: {id}")


@cli.command(hidden=True)
def version():
    """Show the version of QuClo."""
    click.echo(f'QuClo Version: {get_version("quclo")}')


@cli.command(hidden=True)
def help():
    """Show the help message."""
    click.echo(cli.get_help(click.get_current_context()))


@create.command()
@click.option("--email", prompt=True, required=True, help="Email for the user")
@click.password_option(required=True, help="Password for the user")
def user(email: str, password: str):
    """Create a user."""
    new_user = User(email=email, password=password)
    new_user.create()
    Config.save_default_user(email)
    click.echo(f"User created with email: {new_user.email}")


@create.command()
@click.option(
    "--email",
    prompt=True,
    default=Config.load_default_user(),
    required=True,
    help="Email of the user",
)
@click.password_option(
    confirmation_prompt=False, required=True, help="Password of the user"
)
@click.option(
    "--duration", type=int, default=None, help="Duration of the token in days"
)
def token(email: str, password: str, duration: int | None):
    """Create a token."""
    user = User(email=email, password=password)
    token = user.get_token(duration)
    if token is None:
        raise click.ClickException("Failed to create token")
    Config.save_default_user(email)
    Config.save_token(token)
    click.echo(f"Token created for user with email: {email}")


@create.command()
@click.option("--data", help="QIR or QASM code for the circuit")
@click.option("--file", type=click.Path(exists=True), help="Path to circuit file")
@click.option(
    "--priority",
    type=click.Choice([p.value for p in Priority]),
    help="Select a backend based on priority",
)
@click.option("--backend", help="Select a specific backend")
def circuit(
    data: str | None,
    file: str | None,
    priority: str | None,
    backend: str | None,
):
    """Create a circuit."""
    data = data or Path(file).read_text() if file else data
    if not data:
        raise click.ClickException("No data provided for the circuit")
    circuit = Circuit(data=data)
    execution = None
    if priority:
        execution = Execution(circuit=circuit, priority=Priority(priority))
    elif backend:
        execution = Execution(circuit=circuit, backend=Backend(name=backend))
    else:
        execution = Execution(circuit=circuit)
    click.echo(execution.run())


@get.command()
@click.argument("email", default=Config.load_default_user())
@click.argument("token", default=Config.load_token())
def user(token: str):
    """Get a user."""
    click.echo("Getting current user")
    user = User(token=token)
    click.echo(user)


@get.command()
def backends():
    """Get all backends."""
    click.echo("Getting backends")


@get.command()
@click.argument("name")
def backend(name: str):
    """Get a backend."""
    click.echo(f"Getting backend with name: {name}")


@get.command()
def circuits():
    """Get all circuits."""
    click.echo("Getting circuits")


@get.command()
@click.argument("id")
def circuit(id: str):
    """Get a circuit."""
    click.echo(f"Getting circuit with ID: {id}")


@get.command()
def config():
    """Get the configuration."""
    click.echo(Config())


@edit.command()
@click.option(
    "--email",
    required=True,
    prompt=True,
    default=Config.load_default_user(),
    help="Email for the user",
)
@click.password_option(confirmation_prompt=False, help="Password for the user")
def user(email: str, password: str):
    """Edit a user."""
    new_email = click.prompt("New Email", default=email)
    new_password = click.prompt(
        "New Password",
        default=password,
        hide_input=True,
        confirmation_prompt=True,
        show_default=False,
    )


@edit.command()
@click.argument("id")
def circuit(id: str):
    """Edit a circuit."""
    click.echo(f"Editing circuit with ID: {id}")


@edit.command()
@click.option("--token", help="Token for the user")
@click.option("--email", help="Email for the user")
@click.option("--priority", help="Priority for the user")
@click.option("--backend", help="Backend for the user")
def config(
    token: str | None, email: str | None, backend: str | None, priority: str | None
):
    """Edit the configuration."""
    if token is not None:
        Config.save_token(token)
        click.echo("Token updated")
    if email is not None:
        Config.save_default_user(email)
        click.echo("Email updated")
    if backend is not None:
        Config.save_default_backend(backend)
        click.echo("Backend updated")
    if priority is not None:
        Config.save_default_priority(priority)
        click.echo("Priority updated")


if __name__ == "__main__":
    cli()
