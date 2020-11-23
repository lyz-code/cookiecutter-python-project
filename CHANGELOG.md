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
