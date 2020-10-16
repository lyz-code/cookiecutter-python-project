import os
import re

import pytest
import sh
from binaryornot.check import is_binary

PATTERN = r"{{(\s?cookiecutter)[.](.*?)}}"
RE_OBJ = re.compile(PATTERN)


@pytest.fixture
def context():
    return {
        "project_name": "My Test Project",
        "project_slug": "my-test-project",
    }


SUPPORTED_COMBINATIONS = [
    {"author": "another-author"},
    {"requirements": "requests, sh"},
]

UNSUPPORTED_COMBINATIONS = []


def _fixture_id(context):
    """Helper to get a user friendly test name from the parametrized context."""
    return "-".join(f"{key}:{value}" for key, value in context.items())


def build_files_list(root_dir):
    """Build a list containing absolute paths to the generated files."""
    return [
        os.path.join(dirpath, file_path)
        for dirpath, subdirs, files in os.walk(root_dir)
        for file_path in files
    ]


def check_paths(paths):
    """Method to check all paths have correct substitutions."""
    # Assert that no match is found in any of the files
    for path in paths:
        if is_binary(path):
            continue

        for line in open(path, "r"):
            match = RE_OBJ.search(line)
            assert match is None, f"cookiecutter variable not replaced in {path}"


@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_project_generation_without_external_hooks(cookies, context, context_override):
    """Test that project is generated and fully rendered."""
    result = cookies.bake(extra_context={**context, **context_override})
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == context_override.get(
        "project_slug", context.get("project_slug", None)
    )
    assert result.project.isdir()

    paths = build_files_list(str(result.project))
    assert paths
    check_paths(paths)


@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_flake8_passes(cookies, context_override):
    """Generated project should pass flake8."""
    result = cookies.bake(extra_context=context_override)

    try:
        sh.flake8(_cwd=str(result.project))
    except sh.ErrorReturnCode as e:
        pytest.fail(e.stdout.decode())


@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_black_passes(cookies, context_override):
    """Generated project should pass black."""
    result = cookies.bake(extra_context=context_override)

    try:
        sh.black(
            "--check", "--diff", "--exclude", "migrations", _cwd=str(result.project)
        )
    except sh.ErrorReturnCode as e:
        pytest.fail(e.stdout.decode())


@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_yamllint_passes(cookies, context_override):
    """Generated project should pass black."""
    result = cookies.bake(extra_context=context_override)

    try:
        sh.yamllint(".", _cwd=str(result.project))
    except sh.ErrorReturnCode as e:
        pytest.fail(e.stdout.decode())


@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_markdownlint_passes(cookies, context_override):
    """Generated project should pass black."""
    result = cookies.bake(extra_context=context_override)

    try:
        sh.markdownlint("-c", ".markdownlint.json", ".", _cwd=str(result.project))
    except sh.ErrorReturnCode as e:
        pytest.fail(e.stdout.decode())
