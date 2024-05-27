import click

from app.main import WorkerRunner, get_first_parser


@click.group()
def cli() -> None:
    """Управление приложением."""


@click.command(name="run-first-parser", help="Запуск парсера")
def run_first_parser() -> None:
    """Запуск парсера."""
    WorkerRunner(get_first_parser())


def __main_run() -> None:
    """Запуск приложения."""
    commands = (run_first_parser,)

    for cmd in commands:
        cli.add_command(cmd)

    cli()


if __name__ == "__main__":
    __main_run()
