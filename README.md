# Python project template

[![Actions Status](https://github.com/lyz-code/cookiecutter-python-project/workflows/Python%20package/badge.svg)](https://github.com/lyz-code/cookiecutter-python-project/actions)

This is a [cookiecutter](https://github.com/cookiecutter/cookiecutter) template to
generate python projects following the best practices gathered over the time.

Features:

* Initialize the git repository with the correct github remote.
* Generate the `requirements.txt` and `requirements-dev.txt` files.
* Configure the virtualenv and install the development requirements.
* Configure the [pre-commit](https://github.com/pre-commit/pre-commit) and
    Github CI checks of [Black](https://black.readthedocs.io/en/stable/),
    [Flake8](https://flake8.pycqa.org/), [Mypy](http://mypy-lang.org/),
    [Bandit](https://bandit.readthedocs.io/en/latest/),
    [Safety](https://github.com/pyupio/safety).
* Configure Pytest.
* Configure the project layout following the `src` and domain
    driven design structures.
* Configure the documentation with [MkDocs](https://www.mkdocs.org/).
* Configure the CI to publish the packages to pypi
* Configure pytest to show the messages in verbose and the `slow` and
    `secondary` marks.
* Configure the versioning of the program.
* Configure common developer operations with Makefile.
* Configure the Security advisories.
* Configure Github's:
    * Create the repository.
    * Issue and pull request templates.
    * Dependabot.
    * Secrets to publish to PyPI and automatically deploy the documentation
        static website.

## Install

* Install cookiecutter

    ```bash
    pip install cookiecutter
    ```

* Create the template

    ```bash
    cookiecutter https://github.com/lyz-code/cookiecutter-python-project -f
    ```

If you've already run the last command sometime in the pass, you can use
`cookiecutter cookiecutter-python-project -f`.

| Parameter     | Default Value | Description |
| ---           | ---           | ---         |
| playbook_name | Playbook Name |             |

## Contributing

If you want to contribute to the project, you first need to setup your
environment:

* Install the development dependencies: `pip install -r requirements-dev.txt`.
* Install the [pre-commit](https://pre-commit.com/) hooks: `pre-commit install`.

## Testing

Run the tests with `pytest`.

## License

GPLv3
