import click
from .is_even_folder import is_even_module


@click.command()
@click.argument("number", type=int)
def cli(number: int):
    click.echo(
        "{} is even? {}!".format(
            click.style(number, bold=True),
            click.style(is_even_module(number), bold=True, fg="green"),
        )
    )