import typer

app = typer.Typer()


@app.callback()
def callback():
    pass


@app.command()
def execute(option: str = typer.Option()):
    raise NotImplementedError()


if __name__ == '__main__':
    app()
