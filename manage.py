from asyncio import CancelledError
from contextlib import suppress

import click

from app.main import FirstParser


@click.group()
def cli() -> None:
    """Управление приложением."""


@click.command(name="run-first-parser", help="Запуск парсера")
def run_first_parser() -> None:
    """Запуск парсера."""
    FirstParser.bootstrap()


def __main_run() -> None:
    """Запуск приложения."""
    commands = (run_first_parser,)

    for cmd in commands:
        cli.add_command(cmd)

    cli()


if __name__ == "__main__":
    with suppress(KeyboardInterrupt, SystemExit, CancelledError):
        __main_run()
