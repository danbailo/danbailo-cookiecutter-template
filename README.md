# Template Project

Simple structure that I([@danbailo](https://github.com/danbailo)) like use to build projects.

enjoy and... Python 🐍 for everthing :)

## Suggest things

- [pyenv](https://github.com/pyenv/pyenv) and [pyenv-installer](https://github.com/pyenv/pyenv-installer)

### Running applications with Docker

```bash
docker compose --env-file=compose.env down --remove-orphans
docker compose --env-file=compose.env build
```

- To run specific service

```bash
docker compose --env-file=compose.env run <service-name>
```

or

```bash
docker compose --env-file=compose.env create <service-name>
docker start <container-service-name>
```

- To run all services

```bash
docker compose --env-file=compose.env up
```

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

### Python dotenv

Running project with `dotenv run python ...` to load external enviroment at runtime.

By default, will load `.env` at current path, but you can load more than one enviroments.

```bash
dotenv -f .env-foo run python ...
```

Suggest enviroment variable `PYTHONBREAKPOINT=ipdb.set_trace`

After install `ipdb` package, you can debug files with ipython when call `breakpoint()` in your code.
