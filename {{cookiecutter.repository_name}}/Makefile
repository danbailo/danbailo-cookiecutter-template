REPOSITORY = {{cookiecutter.repository_name}}
SOURCE = {{cookiecutter.repository_name|lower|replace("-", "_")}}
TESTS = tests


build:
	@docker build -t $(REPOSITORY):latest .

install:
	@echo "\nInstalling project..."
	@poetry install --no-root
	@echo "\nProject installed!"

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
	@echo "\nRunning Tests"
	@poetry run pytest -s $(TESTS) --cov=$(SOURCE)
	@poetry run coverage-badge -o assets/coverage-badge.svg -f -q

check_all: check_format check_lint check_types test
	@echo "\nAll checks have been passed!"

prepare_env_pyenv:
	@echo "\nPreparing virtualenv using pyenv..."
	@pyenv update
	@pyenv install 3.11.3 -s
	@pyenv virtualenv -f 3.11.3 {{cookiecutter.repository_name|lower|replace("-", "_")}}-env
	@pyenv local {{cookiecutter.repository_name|lower|replace("-", "_")}}-env

	@echo "\nInstalling poetry..."
	@pip install poetry

	@echo "\nProject prepared to install!"

install_with_pyenv: prepare_env_pyenv install
	@echo "\nProject installed with pyenv!"