import asyncio

from functools import wraps

import os

import typer

from common.logger import logger

app = typer.Typer()

logger.info(f'my environ var: {os.environ.get("MY_ENVIROMENT_VARIABLE")}')


@app.callback()
def callback():
    pass


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapper


@coro
@app.command()
def async_execute(option: str = typer.Option()):
    logger.info(f'option: {option}')
    

@app.command()
def execute(option: str = typer.Option()):
    logger.info(f'option: {option}')


if __name__ == '__main__':
    app()
