import click

from app.main import get_first_parser, run_worker


@click.group()
def cli() -> None:
    """Управление приложением."""


@click.command(name="run-first-parser", help="Запуск парсера")
def run_first_parser() -> None:
    """Запуск парсера."""
    run_worker(get_first_parser())


def __main_run() -> None:
    """Запуск приложения."""
    commands = (run_first_parser,)

    for cmd in commands:
        cli.add_command(cmd)

    cli()


if __name__ == "__main__":
    __main_run()
