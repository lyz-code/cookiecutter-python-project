[![Actions Status](https://github.com/{{ cookiecutter.github_user }}/{{ cookiecutter.project_slug }}/workflows/Tests/badge.svg)](https://github.com/{{ cookiecutter.github_user }}/{{ cookiecutter.project_slug }}/actions)
[![Actions Status](https://github.com/{{ cookiecutter.github_user }}/{{ cookiecutter.project_slug }}/workflows/Build/badge.svg)](https://github.com/{{ cookiecutter.github_user }}/{{ cookiecutter.project_slug }}/actions)
[![Coverage Status](https://coveralls.io/repos/github/{{ cookiecutter.github_user }}/{{ cookiecutter.project_slug }}/badge.svg?branch=master)](https://coveralls.io/github/{{ cookiecutter.github_user }}/{{ cookiecutter.project_slug }}?branch=master)

{{ cookiecutter.project_description }}

# Installing

```bash
pip install {{ cookiecutter.project_slug }}
```

# A Simple Example

```python
{! examples/simple-example.py !} # noqa
```

# References

As most open sourced programs, `{{ cookiecutter.project_slug }}` is standing on the shoulders of
giants, namely:

[Pytest](https://docs.pytest.org/en/latest)
: Testing framework, enhanced by the awesome
    [pytest-cases](https://smarie.github.io/python-pytest-cases/) library that made
    the parametrization of the tests a lovely experience.

[Mypy](https://mypy.readthedocs.io/en/stable/)
: Python static type checker.

[Flakeheaven](https://github.com/flakeheaven/flakeheaven)
: Python linter with [lots of
    checks](https://lyz-code.github.io/blue-book/devops/flakeheaven#plugins).

[Black](https://black.readthedocs.io/en/stable/)
: Python formatter to keep a nice style without effort.

[Autoimport](https://github.com/lyz-code/autoimport)
: Python formatter to automatically fix wrong import statements.

[isort](https://github.com/timothycrosley/isort)
: Python formatter to order the import statements.

[Pip-tools](https://github.com/jazzband/pip-tools)
: Command line tool to manage the dependencies.

[Mkdocs](https://www.mkdocs.org/)
: To build this documentation site, with the
[Material theme](https://squidfunk.github.io/mkdocs-material).

[Safety](https://github.com/pyupio/safety)
: To check the installed dependencies for known security vulnerabilities.

[Bandit](https://bandit.readthedocs.io/en/latest/)
: To finds common security issues in Python code.

[Yamlfix](https://github.com/lyz-code/yamlfix)
: YAML fixer.

# Contributing

For guidance on setting up a development environment, and how to make
a contribution to *{{ cookiecutter.project_slug }}*, see [Contributing to
{{ cookiecutter.project_slug }}](https://{{ cookiecutter.github_user}}.github.io/{{ cookiecutter.project_slug }}/contributing).
