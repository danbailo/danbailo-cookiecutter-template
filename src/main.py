import os

import typer

from common.logger import logger

app = typer.Typer()

logger.info(f'my environ var: {os.environ.get("MY_ENVIROMENT_VARIABLE")}')


@app.callback()
def callback():
    pass


@app.command()
def execute(option: str = typer.Option()):
    logger.info(f'option: {option}')


if __name__ == '__main__':
    app()
