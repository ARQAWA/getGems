from asyncio import CancelledError
from contextlib import suppress

import click

from app.main import StatsFetcherMain


@click.group()
def cli() -> None:
    """Управление приложением."""


@click.command(name="run-stats-fetcher", help="Запуск сборщика статистики")
def run_stats_fetcher() -> None:
    """Запуск сборщика статистики."""
    StatsFetcherMain.bootstrap()


def __main_run() -> None:
    """Запуск приложения."""
    for cmd in (run_stats_fetcher,):
        cli.add_command(cmd)

    cli()


if __name__ == "__main__":
    with suppress(KeyboardInterrupt, SystemExit, CancelledError):
        __main_run()
