import click

from app.main import FirstParser, WorkerRunner


@click.group()
def cli() -> None:
    """Управление приложением."""


@click.command(name="run-parser", help="Запуск парсера")
def run_parser() -> None:
    """Запуск парсера."""
    click.echo("Выполнение команды run-parser")
    WorkerRunner(FirstParser)


def __main_run() -> None:
    """Запуск приложения."""
    commands = (run_parser,)

    for cmd in commands:
        cli.add_command(cmd)

    cli()


if __name__ == "__main__":
    __main_run()
