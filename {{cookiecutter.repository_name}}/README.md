# {{cookiecutter.project_name}}

[![Tests and Linting](https://github.com/{{cookiecutter.gh_username_or_gh_organization}}/{{cookiecutter.repository_name}}/actions/workflows/tests.yaml/badge.svg?branch=main)](https://github.com/{{cookiecutter.gh_username_or_gh_organization}}/{{cookiecutter.repository_name}}/actions/workflows/tests.yaml) ![Coverage Status](./assets/coverage-badge.svg)

Simple structure that I([@danbailo](https://github.com/danbailo)) like use to build projects.

enjoy and... Python 🐍 for everthing 😄

## Make
The project uses a [Makefile](Makefile) to facilitate project installation, lint execution, typing and testing.

### Preparing virtual enviroment

It is highly recommended to use virtual environments when developing Python projects.

### Using poetry

Install [poetry](https://github.com/python-poetry/poetry) then install the project using Make.

```
make install
```

### Using pyenv

Install the [prerequisites](https://github.com/pyenv/pyenv/wiki/Common-build-problems#prerequisites) and then install [pyenv](https://github.com/pyenv/pyenv-installer). After install and configure pyenv, just install the project using Make.

```
make prepare_env_pyenv
```

then

```
make install
```

### Project commands

| Command | Description |
|-|-|
| `make install` | Install project as dev |
| `make build` | Build a Docker image to run project |
| `make format` | Format the code |
| `make lint` | Lint the code |
| `make check_format` | Check code format |
| `make check_lint` | Check code lint |
| `make check_types` | Check code types |
| `make check_all` | Run all checkers of project |
| `make tests` | Run tests |
| `make clean` | Clean project cache |

All settings defined in formatting, typing and linting are defined in the Python project configuration file - [pyproject.toml](pyproject.toml).
