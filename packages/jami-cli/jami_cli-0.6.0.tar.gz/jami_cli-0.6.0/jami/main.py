from importlib import metadata

import typer
from typing_extensions import Annotated

from jami.encryption import password_decrypt, password_encrypt

cli = typer.Typer()


@cli.command()
def version():
    typer.secho(metadata.version("jami-cli"), fg=typer.colors.GREEN)


@cli.command()
def encrypt(
    text: Annotated[str, typer.Option(prompt="Type in your text")],
    password: Annotated[
        str,
        typer.Option(prompt=True, confirmation_prompt=True, hide_input=True),
    ],
):
    cypher = password_encrypt(text.encode("utf-8"), password).decode("utf-8")
    typer.secho(cypher, fg=typer.colors.GREEN)


@cli.command()
def decrypt(
    cypher: Annotated[str, typer.Option(prompt="Type in your encrypted text")],
    password: Annotated[
        str,
        typer.Option(prompt=True, hide_input=True),
    ],
):
    text = password_decrypt(cypher.encode("utf-8"), password).decode("utf-8")
    typer.secho(text, fg=typer.colors.GREEN)
