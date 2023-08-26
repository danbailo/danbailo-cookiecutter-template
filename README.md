## Template Project

Simple structure that I(@danbailo) like to build projects.

enjoy and... Python 🐍 for everthing :)

## Suggest things

- [pyenv](https://github.com/pyenv/pyenv) and [pyenv-installer](https://github.com/pyenv/pyenv-installer)

### Running applications with Docker

```bash
docker compose --env-file=compose.env down --remove-orphans
docker compose --env-file=compose.env build
```

then

```bash
docker compose --env-file=compose.env run <service-name>
```

```bash
docker compose --env-file=compose.env up
```