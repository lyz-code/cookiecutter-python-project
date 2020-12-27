## 0.3.0 (2020-12-27)

### Feat

- add command line templates and config reading from yaml
- add command line configuration

### feat

- **pyproject**: disable W1201 and C0301 for everything and E501 for the test of the views

### Fix

- disable the W1203 pylint error.

## 0.2.0 (2020-12-10)

### Feat

- add bump makefile command
- add flakehell exceptions and remove the missing docstring exception in tests
- add the __all__ variable to the project __init__.py file
- add yamlfix formatter to development requirements

### fix

- add typing information to the __all__ variable

### Fix

- **services**: correct docstring
- **version**: correct the name of the package

## 0.1.2 (2020-11-23)

### Fix

- remove the ANN101 and R0201 check in the test files

## 0.1.1 (2020-11-23)

### Fix

- make post hooks idempotent

## 0.1.0 (2020-11-13)

### Fix

- **makefile**: rename tests to test
- **pre-commit**: remove pip-tools and bandit, replace flake8 in favor of flakehell

### Feat

- **setup.py**: adapt it to the template
- **ci**: configure Github templates for issues, security policy and pull requests
- **linters**: substitute Flake8 in favor of Flakehell
- create first version of the cookiecutter template

### fix

- **hooks**: improve the detection of an existent .git directory

### feat

- add linters configuration
