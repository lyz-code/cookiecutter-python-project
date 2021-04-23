## 0.6.0 (2021-04-23)

### Fix

- patch the flakehell extended default ignore error
- change black precommit branch to master

### perf

- Change the overview name for the package name, so it's better seen

### Feat

- add ADR skeleton

### feat

- **Makefile**: support uploading to pypi testing

### fix

- **Makefile**: remove more egg-info directories

## 0.5.0 (2021-03-11)

### Feat

- patch the E0611 error when importing pydantic models

### fix

- SIM115 in setup.py

### Fix

- Add the Config type hint to the runner fixture
- correct configuration error test
- bug in requirement parsing.
- reduce the requirements update to daily

### feat

- ignore ANN102 and TYP001

## 0.4.0 (2020-12-29)

### Feat

- create CI pipeline to hourly update requirements

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
