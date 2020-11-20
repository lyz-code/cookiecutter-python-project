[![Actions Status](https://github.com/lyz-code/cookiecutter-python-project/workflows/Tests/badge.svg)](https://github.com/lyz-code/cookiecutter-python-project/actions)
[![Actions Status](https://github.com/lyz-code/cookiecutter-python-project/workflows/Build/badge.svg)](https://github.com/lyz-code/cookiecutter-python-project/actions)

Cookiecutter template to generate python projects following the [best practices
gathered over the time](https://lyz-code.github.io/blue-book/coding/python/python_project_template/).

[Sadly](https://sanctum.geek.nz/why-not-github.html) it's heavily focused on
Github. If you want to use another git web application or CI providers, please open an
[issue](https://github.com/lyz-code/cookiecutter-python-project/issues/new).

The template will:

* [Initialize the git
    repository](https://lyz-code.github.io/blue-book/coding/python/python_project_template/#basic-python-project)
    with the correct github remote and a useful gitignore.

* Configure [the project
    layout](https://lyz-code.github.io/blue-book/coding/python/python_project_template/#project-structure)
    following the `src` and domain driven design structures.

* Configure the program dependencies to be handled by
    [pip-tools](https://lyz-code.github.io/blue-book/devops/pip_tools/).

* Configure the program documentation using
    [MkDocs](https://lyz-code.github.io/blue-book/linux/mkdocs), with some
    niceties like generating a reference page [directly from the
    docstrings](https://lyz-code.github.io/blue-book/coding/python/mkdocstrings/).

* Generate a Makefile to gather the common developer operations, go to the
    [contributing](contributing.md#development-facilities) page to look at the
    most important.

* Configure the versioning to follow [semantic versioning](https://semver.org/):
    Assuming you use commit messages following the [conventional
    commits](https://www.conventionalcommits.org) guidelines, you'll be able to
    automatically bump the version and generate the changelog without human
    interaction with [commitizen](https://commitizen-tools.github.io/commitizen/).

* Create a helper function to output the version of the program, Python and the
    operative system, useful for debugging user issues.

* Configure the static analysis tools:
    * Configure [Pytest](https://lyz-code.github.io/blue-book/coding/python/pytest/)
        as test framework. Set up the format, directories to ignore and the
        `slow` and `secondary` marks.
    * Configure [Black](https://lyz-code.github.io/blue-book/devops/black/) for
        automatic format and check the code styling.
    * Configure [isort](https://isort.readthedocs.io/) to automatically sort the
        import statements.
    * Configure
        [flakehell](https://lyz-code.github.io/blue-book/devops/flakehell/) to
        check errors in your code.
    * Configure [Mypy](https://lyz-code.github.io/blue-book/devops/mypy/) to
        check the typing of your code.
    * Configure [Safety](https://lyz-code.github.io/blue-book/devops/safety/) to
        check dependencies that have vulnerabilities.
    * Configure [Bandit](https://lyz-code.github.io/blue-book/devops/bandit/) to
        check for vulnerabilities in your code.
    * Configure
        [Markdownlint](https://lyz-code.github.io/blue-book/devops/markdownlint/) to
        flag errors, bugs or stylistic errors in markdown files.

* Configure Github's project:
    * Create the repository.
    * Create the issue and pull request templates.
    * Configure Dependabot to notify on outdated dependencies.
    * Create the secrets to publish to PyPI.
    * Configure the Security advisories.

* Configure the [continuous
    integration](https://lyz-code.github.io/blue-book/devops/ci) pipelines:
    * Run the [tests](https://lyz-code.github.io/blue-book/coding/python/pytest).
    * Run the [linters](https://lyz-code.github.io/blue-book/devops/ci/#linters).
    * Run the [type checkers](https://lyz-code.github.io/blue-book/devops/ci/#type-checkers).
    * Run the [security checks](https://lyz-code.github.io/blue-book/devops/ci/#security-vulnerability-checkers).
    * Generate [coverage
        reports](https://lyz-code.github.io/blue-book/devops/ci/#coverage-reports)
        and upload them to [Coveralls](https://coveralls.io/).
    * Build the python package.

* Configure the continuous deployment pipelines:
    * Automatically deploy the documentation static website on each push to
        master.
    * Automatically build the python packages and publish them to PyPI.

* Configure the
    [pre-commits](https://lyz-code.github.io/blue-book/devops/ci/#configuring-pre-commit).
* Configure the base [typing](https://lyz-code.github.io/blue-book/coding/python/type_hints)
* Set the license to GPLv3.

# Usage

We assume you are comfortable with some tools:

* [cruft](https://lyz-code.github.io/blue-book/linux/cruft) or
    [cookiecutter](https://lyz-code.github.io/blue-book/linux/cookiecutter/) to generate
    the l
* [pass](https://www.passwordstore.org/): Used to load the sensitive data such as
    the github credentials.
* [commitizen](https://commitizen-tools.github.io/commitizen/): Used to bump the version
    and make the releases.

To create a new project use:

```bash
cruft https://github.com/lyz-code/cookiecutter-python-project
```

Or

```bash
cookiecutter https://github.com/lyz-code/cookiecutter-python-project
```

# Contributing

For guidance on setting up a development environment, and how to make
a contribution to *cookiecutter-python-project*, see [Contributing to
cookiecutter-python-project](https://github.io/lyz-code/cookiecutter-python-project/contributing).
