## 0.9.0 (2022-03-10)

### Feat

- use flakeheaven instead of the unmaintained flakehell
- use flakeheaven instead of the unmaintained flakehell
- change package management to pdm
- change package management to pdm
- use GoodConf to manage yaml configuration
- mark deprecation warnings as errors
- create the load_config entrypoint function
- **ci**: add the workflow_dispatch event handler
- Configure black to drop python 3.6 and use python 3.9 and 3.10 instead
- Configure black to drop python 3.6 and use python 3.9 and 3.10 instead
- disable github integration on cookiecutter creation
- disable github integration on cookiecutter creation
- add support for python 3.10, drop support for 3.6
- add support for python 3.10, drop support for 3.6
- ignore pragma cover for TYPE_CHECKING statements

### Perf

- fix flakeheaven issues
- upgrade the versions of the pre-commits

### Fix

- ignore freezegun deprecation warning
- select pdm path editable backed
- select pdm path editable backed
- remove the python_paths that is no longer needed
- define the log_level attribute of the config object
- **ci**: deprecate dependabot as pdm is not supported yet
- **template**: remove the __all__ at init level
- **template**: remove models directory and create model.py
- **template**: correct the path to remove the cli.py entrypoint if it's not configured
- hardcode flake8<4.0.0 until flakehell supports it

## 0.8.2 (2021-10-21)

### Fix

- correct makefile tab to spaces
- use pip-sync to sync the virtualenv with the requirements

### fix

- **pre_commit**: correct black revision branch

## 0.8.1 (2021-06-03)

### Fix

- remove git hooks from the update ci workflow

## 0.8.0 (2021-05-02)

### Feat

- run pytest in parallel

## 0.7.0 (2021-04-23)

### Fix

- install wheel in the build pipeline

### feat

- add a ci job to test that the program is installable

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
