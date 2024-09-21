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
	@uv sync

format:
	@uv run ruff format $(SOURCE)
	@uv run ruff format $(TESTS)

lint:
	@uv run ruff check $(SOURCE) --fix
	@uv run ruff check $(TESTS) --fix

tests:
	@printf "Running Tests"
	@uv run pytest -s $(TESTS) --cov=$(SOURCE)
	@uv run coverage xml

check_format:
	@uv run ruff format $(SOURCE) --check
	@uv run ruff format $(TESTS) --check

check_lint:
	@uv run ruff check $(SOURCE)
	@uv run ruff check $(TESTS)

check_types:
	@uv run mypy $(SOURCE)
	@uv run mypy $(TESTS)

check_all: check_format check_lint check_types tests
	@printf "All checks have been passed! 🎉✅\n"

clean:
	@docker compose -f docker-compose.local.yaml --env-file docker-compose.local.env down --remove-orphans
	@uv cache clean
	@rm -rf .ruff_cache
	@rm -rf .mypy_cache
	@rm -rf .pytest_cache
	@find . -name "__pycache__" -type d -exec rm -rf {} +
	@printf "File and directory cache removed! ➡️ 🗑️ ✅\n"