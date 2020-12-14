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

        for line in open(path, "r"):
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
    assert result.project.basename == context_override.get(
        "project_slug", context.get("project_slug", None)
    )
    assert result.project.isdir()
    paths = build_files_list(str(result.project))
    assert paths
    check_paths(paths)


@pytest.mark.trylast
@pytest.mark.slow
@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_flakehell_passes(
    cookies: Cookies, context: Dict[str, str], context_override: Dict[str, str]
) -> None:
    """Generated project should pass flakehell."""
    result = cookies.bake(extra_context={**context, **context_override})

    try:
        sh.bash(
            "-c",
            "virtualenv -p `which python3.7` env; "
            "source env/bin/activate; "
            "pip install pip-tools; "
            "pip-compile -U --allow-unsafe setup.py; "
            "pip-compile -U --allow-unsafe requirements-dev.in "
            "   --output-file requirements-dev.txt; "
            "pip install -r requirements-dev.txt; ",
            "pip install -e .",
            _cwd=str(result.project),
        )
        # This step is run by the post-generation hooks
        __import__("pdb").set_trace()  # XXX BREAKPOINT
        sh.black(".", _cwd=str(result.project))
        result = sh.flakehell("lint", "src", "tests", _cwd=str(result.project))
    except sh.ErrorReturnCode as error:
        pytest.fail(error.stdout.decode())


@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_black_passes(
    cookies: Cookies, context: Dict[str, str], context_override: Dict[str, str]
) -> None:
    """Generated project should pass black."""
    result = cookies.bake(extra_context={**context, **context_override})

    try:
        sh.black(
            "--check", "--diff", "--exclude", "migrations", _cwd=str(result.project)
        )
    except sh.ErrorReturnCode as error:
        pytest.fail(error.stdout.decode())


@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_yamllint_passes(
    cookies: Cookies, context: Dict[str, str], context_override: Dict[str, str]
) -> None:
    """Generated project should pass black."""
    result = cookies.bake(extra_context={**context, **context_override})

    try:
        sh.yamllint(".", _cwd=str(result.project))
    except sh.ErrorReturnCode as error:
        pytest.fail(error.stdout.decode())


@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_markdownlint_passes(
    cookies: Cookies, context: Dict[str, str], context_override: Dict[str, str]
) -> None:
    """Generated project should pass black."""
    result = cookies.bake(extra_context={**context, **context_override})

    try:
        sh.markdownlint("-c", ".markdownlint.json", ".", _cwd=str(result.project))
    except sh.ErrorReturnCode as error:
        pytest.fail(error.stdout.decode())


def test_pip_compile_is_able_to_build_requirements(
    cookies: Cookies, context: Dict[str, str]
) -> None:
    """Generated project should be able to build the documentation."""
    result = cookies.bake(extra_context={**context})

    try:
        result = sh.bash(
            "-c",
            "virtualenv -p `which python3.7` env; "
            "source env/bin/activate; "
            "pip install pip-tools; "
            "pip-compile --allow-unsafe; "
            "pip-compile --allow-unsafe docs/requirements.in "
            "   --output-file docs/requirements.txt; "
            "pip-compile --allow-unsafe requirements-dev.in "
            "   --output-file requirements-dev.txt",
            _cwd=str(result.project),
        )
    except sh.ErrorReturnCode as error:
        pytest.fail(error.stderr.decode())


def test_generated_package_is_installable(
    cookies: Cookies, context: Dict[str, str]
) -> None:
    """Generated project should be able to build the documentation."""
    result = cookies.bake(extra_context={**context})

    try:
        result = sh.bash(
            "-c",
            "virtualenv -p `which python3.7` env; "
            "source env/bin/activate; "
            "pip install -e .; "
            "python -c 'import my_test_project'",
            _cwd=str(result.project),
        )
    except sh.ErrorReturnCode as error:
        pytest.fail(error.stderr.decode())


def test_mkdocs_build_valid_site(cookies: Cookies, context: Dict[str, str]) -> None:
    """Generated project should be able to build the documentation."""
    result = cookies.bake(extra_context={**context})

    try:
        result = sh.bash(
            "-c",
            "virtualenv -p `which python3.7` env; "
            "source env/bin/activate; "
            "pip install pip-tools; "
            "pip-compile docs/requirements.in --output-file docs/requirements.txt; "
            "pip install -r docs/requirements.txt; "
            "pip install -e .; "
            "mkdocs build",
            _cwd=str(result.project),
        )
    except sh.ErrorReturnCode as error:
        pytest.fail(error.stderr.decode())
