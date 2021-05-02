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

	pip install -U pip

	rm requirements.txt
	touch requirements.txt
	pip-compile -Ur --allow-unsafe

	rm docs/requirements.txt
	touch docs/requirements.txt
	pip-compile -Ur --allow-unsafe docs/requirements.in --output-file docs/requirements.txt

	rm requirements-dev.txt
	touch requirements-dev.txt
	pip-compile -Ur --allow-unsafe requirements-dev.in --output-file requirements-dev.txt

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
	rm -f `find . -type f -name '*.rej' `
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

.PHONY: bump
bump: pull-master bump-version clean

.PHONY: pull-master
pull-master:
	@echo "------------------------"
	@echo "- Updating repository  -"
	@echo "------------------------"

	git checkout master
	git pull

	@echo ""

.PHONY: build-docs
build-docs:
	@echo "--------------------------"
	@echo "- Building documentation -"
	@echo "--------------------------"

	mkdocs build

	@echo ""

.PHONY: bump-version
bump-version:
	@echo "---------------------------"
	@echo "- Bumping program version -"
	@echo "---------------------------"

	cz bump --changelog --no-verify
	git push
	git push --tags

	@echo ""

.PHONY: security
security:
	@echo "--------------------"
	@echo "- Testing security -"
	@echo "--------------------"

	# There is currently no fix [#2981](https://github.com/tornadoweb/tornado/issues/2981)
	safety check -i 39462
	@echo ""
	bandit -r hooks

	@echo ""

.PHONY: version
version:
	@python -c "import cookiecutter_python_project.version; print(cookiecutter_python_project.version.version_info())"
