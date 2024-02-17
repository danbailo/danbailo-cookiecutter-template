REPOSITORY = {{cookiecutter.repository_name}}
SOURCE = {{cookiecutter.project_name}}
TESTS = tests


build:
	@docker build -t $(REPOSITORY):latest .

install:
	@poetry install --no-root

check_format:
	@poetry run ruff format $(SOURCE) --check
	@poetry run ruff format $(TESTS) --check

format:
	@poetry run ruff format $(SOURCE)
	@poetry run ruff format $(TESTS)

check_lint:
	@poetry run ruff check $(SOURCE)
	@poetry run ruff check $(TESTS)

lint:
	@poetry run ruff check $(SOURCE) --fix
	@poetry run ruff check $(TESTS) --fix

check_types:
	@poetry run mypy $(SOURCE)
	@poetry run mypy $(TESTS)

test:
	@poetry run pytest -s $(TESTS)

check_all: check_format check_lint check_types test
	@echo "all passed!"