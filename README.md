# Repositório de template de projetos pessoais

Esse repositório faz a utilização da ferramenta [cookiecutter](https://www.cookiecutter.io/) para
gerenciar o template para criação de novos projetos.

## cookiecutter

Essa ferramenta utiliza o [Jinja](https://jinja.palletsprojects.com/en/3.1.x/) para escrever as
configurações do template e facilmente conseguimos definir quais valores queremos "substituir" na
criação de um novo projeto. Basta escrevermos o arquivo `cookiecutter.json` e declarar quais
propriedades devem ser substituidas no novo template.

Exemplo:
```json
{
    "alguma-variavel": "foo",
    "arquivo-python": "main",
    "arquivo-comum": "file"
}
```

Com isso, no diretório de template, todos os lugares que estiverem declarado com ``{{alguma-variavel}}``, ``{{arquivo-python}}`` ou ``{{arquivo-comum}}`` serão gerados com o novo nome definido no ato da execução.

Ainda é possível aplicar [filtros Jinja](https://jinja.palletsprojects.com/en/3.1.x/templates/#list-of-builtin-filters) para customizar nomes específicos de dentro do template.

Ex: 
- ``{{alguma-variavel|lower}}`` - no template esse valor será gerado em lowercase
- ``{{alguma-variavel|upper}}`` - no template esse valor será gerado em uppercase

## Requisitos

Somente instale o `cookiecutter` através do pip.

- Recomendado: utilize o [pipx](https://github.com/pypa/pipx) para realizar a instalação desse pacote para isolar a instalação dessa ferramenta do sistema.

```bash
pipx install cookiecutter
```

## Utilização

Realize a chamada do `cookiecutter` passando o diretório onde contém um template cookiecutter que configura o arquivo `cookiecutter.json`
