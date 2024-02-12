import typer

from common.logger import logger
from common.decorators import coro

from common.env_var import get_env_var

app = typer.Typer()

logger.info(f'my environ var: {get_env_var("MY_ENVIROMENT_VARIABLE")}')


def foo(foo):
    pass

foo()

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

