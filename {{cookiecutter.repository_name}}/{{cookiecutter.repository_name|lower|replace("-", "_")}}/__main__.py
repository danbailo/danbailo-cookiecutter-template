import typer

from {{cookiecutter.repository_name|lower|replace("-", "_")}}.utils.decorators import coro
from {{cookiecutter.repository_name|lower|replace("-", "_")}}.utils.logger import Logger, LoggerFactory

logger: Logger = LoggerFactory.new()

app = typer.Typer()


@app.callback()
def callback():
    pass


@app.command()
@coro
def async_execute(option: str = typer.Option()):
    logger.info(f'option: {option}')


@app.command()
def execute(option: str = typer.Option()):
    logger.info(f'option: {option}')


if __name__ == '__main__':
    app()
