# Template Project

![pylint]()

Simple structure that I([@danbailo](https://github.com/danbailo)) like use to build projects.

enjoy and... Python 🐍 for everthing :)

## Preparing local enviroment

### Installing virtual enviroment

Install a virtualenv - recommended [pyenv](https://github.com/pyenv/pyenv) | [pyenv-installer](https://github.com/pyenv/pyenv-installer)

```
pyenv update
pyenv install 3.11.5
pyenv virtualenv 3.11.5 template-project-env
pyenv local template-project-env
```

### Installing project requirements

```bash
pip install poetry==1.6.1
poetry install
```

### Python dotenv

Running project with `dotenv run python ...` to load external enviroment at runtime.

By default, will load `.env` at current path, but you can load more than one enviroments.

```bash
dotenv -f .env-foo run python ...
```

Suggest enviroment variable `PYTHONBREAKPOINT=ipdb.set_trace`

After install `ipdb` package, you can debug files with ipython when call `breakpoint()` in your code.


## Using Docker

#### Creating containers

If you need to build the project(if you modify the code, for example), just add the flag `--build` at the end of the command
```bash
docker compose --env-file=compose.env create
```

#### Starting/running containers

If you need to see the container logs, just add the flag `-a` to run it in attached mode(example: when you'll run pylint)

```bash
docker start <container-service-name>
```

#### To stop/remove containers

```bash
docker compose --env-file=compose.env down --remove-orphans
```

## Suggest things

### `__main__.py` module

A nice thing implemented in Python to run modules it's the [`__main__.py`](https://docs.python.org/3/library/__main__.html#main-py-in-python-packages) file.

You can implement a module with `__main.py__` inside it and call it directly.

Example

```
src
  commands
    ├── __init__.py
    └── __main__.py
```


```bash
cd src
python -m commands
```