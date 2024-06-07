# {{cookiecutter.project_name}}

[![Pull Request Checks](https://github.com/danbailo/{{cookiecutter.repository_name}}/actions/workflows/pull-request-checks.yaml/badge.svg)](https://github.com/danbailo/{{cookiecutter.repository_name}}/actions/workflows/pull-request-checks.yaml)

[![Tests](https://github.com/jusbrasil/legalops-commons/actions/workflows/tests.yaml/badge.svg?branch=main)](https://github.com/jusbrasil/legalops-commons/actions/workflows/tests.yaml) ![Coverage Status](./assets/coverage-badge.svg)

Simple structure that I([@danbailo](https://github.com/danbailo)) like use to build projects.

enjoy and... Python 🐍 for everthing :)

### Utilizando pyenv

- Pré-requisitos: https://github.com/pyenv/pyenv/wiki/Common-build-problems#prerequisites

Instale o pyenv - https://github.com/pyenv/pyenv-installer.

*Opcional*: após instalar o pyenv, prepare o ambiente utilizando o `make`.

```bash
make -f Makefile-project prepare_env_pyenv
```

## Ambientes virtuais
É altamente recomendado a utilização de ambientes virtuais durante o desenvolvimento de projetos em Python.

O projeto faz a utilização do [Poetry](https://github.com/python-poetry/poetry), que por padrão já configura um ambiente virtual, porém, caso o desenvolvedor opte utilizar outro gerenciador de ambiente virtual, fica aqui a sugestão do [pyenv](https://github.com/pyenv/pyenv).

### Utilizando pyenv
Instale os [Pré-requisitos](https://github.com/pyenv/pyenv/wiki/Common-build-problems#prerequisites) e após isso, instale o [pyenv](https://github.com/pyenv/pyenv-installer).

*Opcional*: após instalar o pyenv, prepare o ambiente utilizando o `make`.

```shell
make -f Makefile prepare_env_pyenv
```

*Dessa forma será configurado automaticamente um ambiente de desenvolvimento do projeto, já definindo a versão do Python e assim que a pasta do projeto for acessada o ambiente virtual será carregado.*

## Make
O projeto faz a utilização de um arquivo [Makefile](Makefile) para facilitar a instalação do projeto, execução de lint, tipagens e testes do mesmo.

### Instalação do projeto

Após realizar a configuração do ambiente de desenvolvimento, basta executar
`make install` para instalar o projeto e começar a desenvolver!

### Linter, Formatação, Typehinting e Testes

Durante o desenvolvimento, basta executar:

`make check_format` - Verifica a formatação do código.

`make format` - Formata o código automaticamente.

`make check_lint` - Verifica o lint do código.

`make lint` - Formata o código corrigindo o lint automaticamente.

`make check_types` - Verifica a tipagem do código.

`make test` - Executa os testes do projeto.

`make check_all` - Executa todos os "checkers" e testes do projeto sinalizando quando está tudo certo. Dessa forma é certo que o pipeline do pull-request irá estar pronto para ir para main.

Todas as configurações definidas na formatação, tipagem, lint, etc. Estão definidas no arquivo de configuração do projeto Python - [pyproject.toml](pyproject.toml).
