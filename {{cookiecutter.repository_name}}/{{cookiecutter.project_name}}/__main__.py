import typer
from commons.decorators import coro
from commons.env_var import get_env_var
from commons.logger import Logger

logger = Logger().get_logger()

app = typer.Typer()

logger.info(f'my environ var: {get_env_var("MY_ENVIROMENT_VARIABLE")}')


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
