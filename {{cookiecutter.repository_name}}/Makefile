REPOSITORY = {{cookiecutter.repository_name}}
SOURCE = {{cookiecutter.project_name}}


build:
	@docker build -t $(REPOSITORY):latest .

install:
	@poetry install --no-root

lint:
	@poetry run ruff check $(SOURCE)

format:
	@poetry run ruff format $(SOURCE)

check_format:
	@poetry run ruff format $(SOURCE) --check

check_types:
	@poetry run mypy $(SOURCE)

test:
	@poetry run pytest -s tests
