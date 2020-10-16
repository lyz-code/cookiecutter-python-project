---
name: Feature Request
about: Suggest a new feature or change to {{ cookiecutter.project_slug }}
labels: feature request
---

### Checks

* [ ] I added a descriptive title to this issue.
* [ ] I have searched (google, github) for similar issues and couldn't find
    anything.
* [ ] I have read and followed [the docs](https://{{ cookiecutter.github_user }}.github.io/{{ cookiecutter.project_slug }})
    and still think this feature/change is needed.

# Feature Request

Output of `python -c "import {{ cookiecutter.project_slug.replace('-', '_') }}.version; print({{ cookiecutter.project_slug.replace('-', '_') }}.version.version_info())"`

```
...
```

<!-- Please read the [docs](https://{{ cookiecutter.github_user }}.github.io/{{ cookiecutter.project_slug }}) and
search through issues to confirm your feature hasn't already been reported. -->

<!-- Where possible please include a self-contained code snippet describing your
feature: -->

```py
...
```
