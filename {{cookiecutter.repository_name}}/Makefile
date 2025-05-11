REPOSITORY = {{cookiecutter.repository_name}}
SOURCE = {{cookiecutter.repository_name|lower|replace("-", "_")}}
TESTS = tests

build:
	@docker build -t $(REPOSITORY):latest .

install:
	@uv sync

docs:
	@uv run mkdocs build

format:
	@uv run ruff format $(SOURCE)
	@uv run ruff format $(TESTS)

lint:
	@uv run ruff check $(SOURCE) --fix
	@uv run ruff check $(TESTS) --fix

.PHONY: tests
tests:
	@echo "Running Tests"
	@uv run pytest -s $(TESTS) --cov=$(SOURCE)
	@uv run coverage xml
#	@uv run coverage-badge -o coverage.svg -f -q

check_vulnerabilities:
	@uv run bandit -c pyproject.toml -r $(SOURCE)	

check_format:
	@uv run ruff format $(SOURCE) --check
	@uv run ruff format $(TESTS) --check

check_lint:
	@uv run ruff check $(SOURCE)
	@uv run ruff check $(TESTS)

check_types:
	@uv run mypy $(SOURCE)
	@uv run mypy $(TESTS)

check_all: check_vulnerabilities check_format check_lint check_types tests
	@echo "🎉✅ All checks have been passed!"

helm_audit:
	@polaris audit --helm-chart $(HELM) -c $(POLARIS_CFG) --set-exit-code-on-danger --set-exit-code-below-score "75" --quiet

helm_prepare:
	@helm dependency build $(HELM)

helm_lint: helm_prepare
	@helm lint $(HELM)

helm_render: helm_prepare helm_lint
	@helm template $(IMAGE) $(HELM) -n $(K8S_NAMESPACE)

kubernetes_apply_test: helm_prepare
	@helm template $(IMAGE) $(HELM) --dry-run=server > $(HELM_OUTPUT_MANIFESTS)
	@kubectl apply -f $(HELM_OUTPUT_MANIFESTS) --dry-run=server

.PHONY: clean
clean:
	@docker compose down --remove-orphans
	@uv cache clean
	@rm -rf $(HELM_OUTPUT_MANIFESTS)
	@rm -rf .ruff_cache
	@rm -rf .mypy_cache
	@rm -rf .pytest_cache
	@find . -name "__pycache__" -type d -exec rm -rf {} +
	@find . -iname '*.pyc' -delete
	@find . -iname '*.pyo' -delete
	@find . -iname '*~' -delete
	@find . -iname '*.swp' -delete
	@find . -iname '.pytest_cache' -exec rm -rf {} \+	
	@rm -rf .coverage
	@rm -rf coverage.xml
	@echo "➡️ 🗑️ ✅ Cache cleaned!"
