.PHONY: build \
	install \
	check_format \
	format \
	lint \
	tests \
	check_lint \
	check_types \
	check_all \
	clean \

REPOSITORY = {{cookiecutter.repository_name}}
SOURCE = {{cookiecutter.repository_name|lower|replace("-", "_")}}
TESTS = tests

build:
	@docker build -t $(REPOSITORY):latest .

install:
	@printf "\nInstalling project..."
	@poetry install --no-root
	@printf "\nProject installed!"

format:
	@poetry run ruff format $(SOURCE)
	@poetry run ruff format $(TESTS)

lint:
	@poetry run ruff check $(SOURCE) --fix
	@poetry run ruff check $(TESTS) --fix

tests:
	@printf "Running Tests"
	@poetry run pytest -s $(TESTS) --cov=$(SOURCE)
	@poetry run coverage xml

check_format:
	@poetry run ruff format $(SOURCE) --check
	@poetry run ruff format $(TESTS) --check

check_lint:
	@poetry run ruff check $(SOURCE)
	@poetry run ruff check $(TESTS)

check_types:
	@poetry run mypy $(SOURCE)
	@poetry run mypy $(TESTS)

check_all: check_format check_lint check_types tests
	@printf "All checks have been passed! 🎉✅\n"

prepare_env_pyenv:
	@printf "Preparing virtualenv using pyenv..."\n
	@pyenv update
	@pyenv install 3.11 -s
	@pyenv virtualenv -f 3.11 {{cookiecutter.repository_name|lower|replace("-", "_")}}-env
	@pyenv local {{cookiecutter.repository_name|lower|replace("-", "_")}}-env
	@printf "Installing poetry...\n"
	@pip install poetry
	@poetry config virtualenvs.create false --local
	@poetry config virtualenvs.prefer-active-python true --local
	@printf "Project prepared to install!\n"

clean:
	#@docker compose -f docker-compose.local.yaml --env-file docker-compose.local.env down --remove-orphans
	@rm -rf .ruff_cache
	@rm -rf .mypy_cache
	@rm -rf .pytest_cache
	@find . -name "__pycache__" -type d -exec rm -rf {} +
	@printf "File and directory cache removed! ➡️ 🗑️ ✅\n"