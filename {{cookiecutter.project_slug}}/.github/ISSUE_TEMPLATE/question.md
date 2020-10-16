---
name: Question
about: Ask a question about how to use {{ cookiecutter.project_slug }}
labels: question
---

### Checks

* [ ] I added a descriptive title to this issue.
* [ ] I have searched (google, github) for similar issues and couldn't find
    anything.
* [ ] I have read and followed [the docs](https://{{ cookiecutter.github_user }}.github.io/{{ cookiecutter.project_slug }})
    and couldn't find an answer.

# Question

Output of `python -c "import {{ cookiecutter.project_slug.replace('-', '_') }}.version; print({{ cookiecutter.project_slug.replace('-', '_') }}.version.version_info())"`

```
...
```

<!-- Please read the [docs](https://{{ cookiecutter.github_user }}.github.io/{{ cookiecutter.project_slug }}) and
search through issues to confirm your question hasn't already been answered. -->

<!-- Where possible please include a self-contained code snippet describing your
question: -->

```py
...
```
