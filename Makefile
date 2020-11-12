SHELL=/bin/bash
.DEFAULT_GOAL := all
isort = isort hooks tests setup.py
black = black --target-version py37 hooks tests setup.py

.PHONY: install
install:
	python -m pip install -U setuptools pip
	pip install -r requirements-dev.txt
	pre-commit install

.PHONY: update
update:
	@echo "-------------------------"
	@echo "- Updating dependencies -"
	@echo "-------------------------"

	pip-compile -U --allow-unsafe
	pip-compile -U --allow-unsafe docs/requirements.in --output-file docs/requirements.txt
	pip-compile -U --allow-unsafe requirements-dev.in --output-file requirements-dev.txt
	pip install -r requirements-dev.txt

	@echo ""

.PHONY: format
format:
	@echo "----------------------"
	@echo "- Formating the code -"
	@echo "----------------------"

	$(isort)
	$(black)

	@echo ""

.PHONY: lint
lint:
	@echo "--------------------"
	@echo "- Testing the lint -"
	@echo "--------------------"

	flakehell lint hooks/ tests/
	$(isort) --check-only --df
	$(black) --check --diff

	@echo ""

.PHONY: mypy
mypy:
	@echo "----------------"
	@echo "- Testing mypy -"
	@echo "----------------"

	mypy hooks tests

	@echo ""

.PHONY: test
test: test-code

.PHONY: test-code
test-code:
	@echo "----------------"
	@echo "- Testing code -"
	@echo "----------------"

	pytest tests ${ARGS}

	@echo ""

.PHONY: all
all: lint mypy test security

.PHONY: clean
clean:
	@echo "---------------------------"
	@echo "- Cleaning unwanted files -"
	@echo "---------------------------"

	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -rf .cache
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -rf *.egg-info
	rm -f .coverage
	rm -f .coverage.*
	rm -rf build
	rm -rf dist
	rm -f src/*.c pydantic/*.so
	python setup.py clean
	rm -rf site
	rm -rf docs/_build
	rm -rf docs/.changelog.md docs/.version.md docs/.tmp_schema_mappings.html
	rm -rf codecov.sh
	rm -rf coverage.xml

	@echo ""

.PHONY: docs
docs:
	@echo "-------------------------"
	@echo "- Serving documentation -"
	@echo "-------------------------"

	mkdocs serve

	@echo ""

.PHONY: build-docs
build-docs:
	@echo "--------------------------"
	@echo "- Building documentation -"
	@echo "--------------------------"

	mkdocs build
	@echo ""

.PHONY: version
version:
	@python -c "import repository_pattern.version; print(repository_pattern.version.version_info())"

.PHONY: security
security:
	@echo "--------------------"
	@echo "- Testing security -"
	@echo "--------------------"

	safety check
	@echo ""
	bandit -r hooks

	@echo ""
