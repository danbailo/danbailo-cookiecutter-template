# {{cookiecutter.project_name}}

<p align="center">
    <em>"{{cookiecutter.project_description}}"</em>
</p>
<p align="center">
<a href="https://github.com/{{cookiecutter.gh_username_or_gh_organization}}/{{cookiecutter.repository_name}}/actions/workflows/publish.yaml" target="_blank">
    <img src="https://github.com/{{cookiecutter.gh_username_or_gh_organization}}/{{cookiecutter.repository_name}}/actions/workflows/publish.yaml/badge.svg" alt="Publish">
</a>
<a href="https://github.com/{{cookiecutter.gh_username_or_gh_organization}}/{{cookiecutter.repository_name}}/actions/workflows/tests.yaml?query=branch=main" target="_blank">
    <img src="https://github.com/{{cookiecutter.gh_username_or_gh_organization}}/{{cookiecutter.repository_name}}/actions/workflows/tests.yaml/badge.svg?branch=main" alt="Tests">
</a>
<a href="https://github.com/{{cookiecutter.gh_username_or_gh_organization}}/{{cookiecutter.repository_name}}/actions/workflows/tests.yaml?query=branch=main" target="_blank">
    <img src="https://codecov.io/gh/{{cookiecutter.gh_username_or_gh_organization}}/{{cookiecutter.repository_name}}/branch/main/graph/badge.svg" alt="Coverage">
<a href="https://pypi.org/project/{{cookiecutter.repository_name}}" target="_blank">
    <img src="https://img.shields.io/pypi/v/{{cookiecutter.repository_name}}?color=%252334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/{{cookiecutter.repository_name}}" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/{{cookiecutter.repository_name}}?color=g" alt="Python Versions">
</a>
</p>

Simple structure that I([@danbailo](https://github.com/danbailo)) like use to build projects.

enjoy and... Python 🐍 for everthing 😄

## Preparing project
This project uses [uv](https://github.com/astral-sh/uv) as package and project manager. This tool also implements a `.venv` and is highly recommended execute the script [prepare_enviroment.sh](prepare_enviroment.sh) before start the devoloping.

Just it run to create an alias to `python` uses the current `.venv` instead of need to run commands using `uv run ...`
```bash
sh prepare_enviroment.sh
```

## Make
The project uses a [Makefile](Makefile) to facilitate project installation, lint execution, typing and testing.

### Project commands

| Command | Description |
|-|-|
| `make install` | Install project |
| `make build` | Build a Docker image to run project |
| `make format` | Format the code |
| `make lint` | Lint the code |
| `make check_vulnerabilities` | Check vulnerabilities |
| `make check_format` | Check code format |
| `make check_lint` | Check code lint |
| `make check_types` | Check code types |
| `make check_all` | Run all checkers of project |
| `make tests` | Run tests |
| `make clean` | Clean project cache |

All settings defined in formatting, typing and linting are defined in the Python project configuration file - [pyproject.toml](pyproject.toml).
