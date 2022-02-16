"""Module to hold the cookiecutter generation tests."""

import os
import re
from typing import Dict, List

import pytest
import sh
from binaryornot.check import is_binary
from pytest_cookies.plugin import Cookies

PATTERN = r"{{(\s?cookiecutter)[.](.*?)}}"
RE_OBJ = re.compile(PATTERN)
SUPPORTED_COMBINATIONS = [
    {"author": "another-author"},
    {"read_configuration_from_yaml": "false"},
    {"configure_command_line": "false"},
    {"requirements": "requests, sh"},
]
UNSUPPORTED_COMBINATIONS: List[Dict[str, str]] = []


@pytest.fixture(name="context")
def context_() -> Dict[str, str]:
    """Define the common default cookiecutter configuration."""
    return {
        "project_name": "My Test Project",
        "project_slug": "my-test-project",
    }


def _fixture_id(context: Dict[str, str]) -> str:
    """Generate a user friendly test name from the parametrized context."""
    return "-".join(f"{key}:{value}" for key, value in context.items())


def build_files_list(root_dir: str) -> List[str]:
    """Build a list containing absolute paths to the generated files."""
    return [
        os.path.join(dirpath, file_path)
        for dirpath, subdirs, files in os.walk(root_dir)
        for file_path in files
    ]


def check_paths(paths: List[str]) -> None:
    """Check all paths have substituted the cookiecutter variables."""
    # Assert that no match is found in any of the files
    for path in paths:
        if is_binary(path):
            continue

        with open(path, "r", encoding="utf-8") as path_file:
            path_content = path_file.read()

        for line in path_content.splitlines():
            match = RE_OBJ.search(line)
            assert match is None, f"cookiecutter variable not replaced in {path}"


@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_project_generation_without_external_hooks(
    cookies: Cookies, context: Dict[str, str], context_override: Dict[str, str]
) -> None:
    """Test that project is generated and fully rendered."""
    result = cookies.bake(extra_context={**context, **context_override})

    assert result.exit_code == 0
    assert result.exception is None
    assert os.path.basename(result.project_path) == context_override.get(
        "project_slug", context.get("project_slug", None)
    )
    paths = build_files_list(str(result.project_path))
    assert paths
    check_paths(paths)


@pytest.mark.trylast()
@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_flakeheaven_passes(
    cookies: Cookies, context: Dict[str, str], context_override: Dict[str, str]
) -> None:
    """Generated project should pass flakeheaven."""
    result = cookies.bake(extra_context={**context, **context_override})

    try:
        # The black step is executed by the post hooks
        # we need to run everything in the same step so that flakeheaven uses the
        # virtualenv.
        sh.bash(
            "-c",
            "virtualenv -p `which python3.9` env; "
            "source env/bin/activate; "
            "pdm install; "
            "pdm run black --exclude env .; "
            "pdm run flakeheaven lint src tests",
            _cwd=str(result.project_path),
        )
    except sh.ErrorReturnCode as error:
        pytest.fail(error.stdout.decode())


@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_black_is_able_to_correct_files(
    cookies: Cookies, context: Dict[str, str], context_override: Dict[str, str]
) -> None:
    """Black is run on the post hooks, make sure it runs without problem."""
    result = cookies.bake(extra_context={**context, **context_override})

    try:
        sh.black("--exclude", "migrations", ".", _cwd=str(result.project_path))
    except sh.ErrorReturnCode as error:
        pytest.fail(error.stdout.decode())


@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_yamllint_passes(
    cookies: Cookies, context: Dict[str, str], context_override: Dict[str, str]
) -> None:
    """Generated project pass yamllint."""
    result = cookies.bake(extra_context={**context, **context_override})

    try:
        sh.yamllint(".", _cwd=str(result.project_path))
    except sh.ErrorReturnCode as error:
        pytest.fail(error.stdout.decode())


@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_markdownlint_passes(
    cookies: Cookies, context: Dict[str, str], context_override: Dict[str, str]
) -> None:
    """Generated project should pass markdownlint."""
    result = cookies.bake(extra_context={**context, **context_override})

    try:
        sh.markdownlint("-c", ".markdownlint.json", ".", _cwd=str(result.project_path))
    except sh.ErrorReturnCode as error:
        pytest.fail(error.stdout.decode())


@pytest.mark.trylast()
def test_project_is_able_to_update_requirements(
    cookies: Cookies, context: Dict[str, str]
) -> None:
    """Generated project should be able to update the requirements."""
    result = cookies.bake(extra_context={**context})

    try:
        result = sh.bash(
            "-c",
            "virtualenv -p `which python3.9` env; "
            "source env/bin/activate; "
            "pdm install; "
            "pdm update",
            _cwd=str(result.project_path),
        )
    except sh.ErrorReturnCode as error:
        pytest.fail(error.stderr.decode())


@pytest.mark.trylast()
def test_mkdocs_build_valid_site(cookies: Cookies, context: Dict[str, str]) -> None:
    """Generated project should be able to build the documentation."""
    result = cookies.bake(extra_context={**context})

    try:
        result = sh.bash(
            "-c",
            "virtualenv -p `which python3.9` env; "
            "source env/bin/activate; "
            "pdm install; "
            "mkdocs build",
            _cwd=str(result.project_path),
        )
    except sh.ErrorReturnCode as error:
        pytest.fail(error.stderr.decode())
