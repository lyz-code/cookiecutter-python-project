"""Configuration tasks to be run after the template has been generated."""

import os
import shutil
import sys
from base64 import b64encode
from typing import Any, Dict, Optional, Tuple

import passpy
import requests
import sh
from cryptography.hazmat.backends import default_backend as crypto_default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from nacl import encoding, public
from sh import git


def encrypt_secret(public_key: str, secret_value: str) -> str:
    """Encrypt a Unicode string using the public key."""
    public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))

    return b64encode(encrypted).decode("utf-8")


def get(
    url: str, token: str, method: str = "get", data: Optional[Dict[str, Any]] = None
) -> requests.models.Response:
    """Handle errors and configuration in requests queries."""
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    if method == "post":
        response = requests.post(url, headers=headers, json=data)
    elif method == "put":
        response = requests.put(url, headers=headers, json=data)
    else:
        response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response


def initialize_git_repository() -> None:
    """Prepare the git repository."""
    print("    * Initializing the project git repository")

    try:
        git.init()
        git.remote(
            "add",
            "origin",
            "git@github.com:{{ cookiecutter.github_user }}/"
            "{{ cookiecutter.project_slug }}.git",
        )
        git.add(".")
        git.commit("-m", "feat: create initial project structure")
        git.checkout("-b", "gh-pages")
        git.checkout("-b", "feat/initial_iteration")

        print("    * Pushing initial changes to master")
        git.push("--force", "--set-upstream", "origin", "master")
        git.push("--force", "--set-upstream", "origin", "gh-pages")
        git.push("--force", "--set-upstream", "origin", "feat/initial_iteration")
        git.push("--force")
    except sh.ErrorReturnCode as error:
        print("There was an error creating the Git repository.")
        print(str(error.stderr, "utf8"))
        sys.exit(1)


def format_code() -> None:
    """Correct source code following the Black style."""
    print("    * Make repository Black linter compliant.")
    sh.black("setup.py", "src", "docs/examples", "tests")


def clean_unwanted_directories() -> None:
    """Remove directories that don't apply to the specific case."""
    print("* Cleaning unwanted directories")
    # Prevent Black from formatting these lines
    # fmt: off
    remove_paths = [
        '{% if cookiecutter.configure_command_line != "True" %} tests/e2e/test_cli.py {% endif %}', # noqa
        '{% if cookiecutter.configure_command_line != "True" %} src/{{cookiecutter.project_slug}}/entrypoints/cli.py {% endif %}', # noqa
        '{% if cookiecutter.read_configuration_from_yaml != "True" %} assets {% endif %}', # noqa
        '{% if cookiecutter.read_configuration_from_yaml != "True" %} tests/unit/test_config.py {% endif %}', # noqa
        '{% if cookiecutter.read_configuration_from_yaml != "True" %} tests/assets {% endif %}', # noqa
    ]
    # fmt: on

    for path in remove_paths:
        path = path.strip()
        if path and os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.unlink(path)


def initialize_requirement_files() -> None:
    """Generate the python dependencies requirement files."""
    print("    * Generate requirements.txt")
    sh.pip_compile("--allow-unsafe")
    print("        * Generate requirements-dev.txt")
    sh.pip_compile("--allow-unsafe", "requirements-dev.in")
    print("        * Generate docs/requirements.txt")
    sh.pip_compile(
        "--allow-unsafe",
        "docs/requirements.in",
        "--output-file",
        "docs/requirements.txt",
    )


def get_password(password_store: passpy.Store, password_path: str) -> str:
    """Get password from pass passwordstore."""
    try:
        password = password_store.get_key(password_path).strip()
    except FileNotFoundError:
        print(f"Error retrieving the password from the path {password_path}")

    return password


def generate_ssh_key() -> Tuple[str, str]:
    """Generate public and private ssh keys."""
    key = rsa.generate_private_key(
        backend=crypto_default_backend(),
        public_exponent=65537,
        key_size=4096,
    )

    private_key = str(
        key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ),
        "utf8",
    )

    public_key = str(
        key.public_key().public_bytes(
            encoding=serialization.Encoding.OpenSSH,
            format=serialization.PublicFormat.OpenSSH,
        )
        + b" {{ cookiecutter.author_email }}",
        "utf8",
    )

    return private_key, public_key


def configure_github_repository(password_store: passpy.Store) -> None:
    """Configure the github repository."""
    github_url = "https://api.github.com"
    print("* Configure the Github repository")
    github_token = get_password(
        password_store, "{{ cookiecutter.github_token_pass_path }}"
    )

    print("    * Check if the repository exists")
    try:
        get(
            url=(
                f"{github_url}/repos/{{ cookiecutter.github_user }}/"
                "{{ cookiecutter.project_slug }}"
            ),
            token=github_token,
        )
        repository_exists = True
    except requests.exceptions.HTTPError:
        repository_exists = False

    if not repository_exists:
        print("    * Creating Github repository")
        try:
            get(
                url=f"{github_url}/user/repos",
                method="post",
                data={
                    "name": "{{ cookiecutter.project_slug }}",
                    "description": "{{ cookiecutter.project_description }}",
                    "homepage": (
                        "https://{{ cookiecutter.github_user }}.github.io/"
                        "{{ cookiecutter.project_slug }}",
                    ),
                },
                token=github_token,
            )
        except requests.exceptions.HTTPError:
            print("Error creating the repository in github")
            sys.exit(1)

    _set_github_secrets(github_url, github_token, password_store)

    print("* Check if the repository is initialized")
    try:
        repo_commits = get(
            url=(
                f"{github_url}/repos/{{ cookiecutter.github_user }}/"
                "{{ cookiecutter.project_slug }}/commits"
            ),
            token=github_token,
        ).json()
        if len(repo_commits) < 1:
            initialize_requirement_files()
            format_code()
            initialize_git_repository()
    except requests.exceptions.HTTPError:
        initialize_requirement_files()
        format_code()
        initialize_git_repository()


def _set_github_secrets(
    github_url: str, github_token: str, password_store: passpy.Store
) -> None:
    """Generate and deploy the Github secrets."""
    print("    * Check if the deploy keys exists")
    try:
        response = get(
            url=(
                f"{github_url}/repos/{{ cookiecutter.github_user }}/"
                "{{ cookiecutter.project_slug }}/keys"
            ),
            token=github_token,
        ).json()
        deploy_keys = [key["title"] for key in response]
        deploy_keys_exists = "gh-pages" in deploy_keys
    except requests.exceptions.HTTPError:
        deploy_keys_exists = False

    ssh_key, ssh_public_key = generate_ssh_key()

    if not deploy_keys_exists:
        print("    * Adding deploy keys to the Github repository")
        try:
            get(
                url=(
                    f"{github_url}/repos/{{ cookiecutter.github_user }}/"
                    "{{ cookiecutter.project_slug }}/keys"
                ),
                method="post",
                data={"key": ssh_public_key, "title": "gh-pages"},
                token=github_token,
            )
        except requests.exceptions.HTTPError:
            print("Error storing the deployment public ssh key")
            sys.exit(1)

    print("    * Adding secrets to the Github repository")
    secrets = [
        ("ACTIONS_DEPLOY_KEY", ssh_key),
        (
            "PYPI_PASSWORD",
            get_password(password_store, "{{ cookiecutter.pypi_token_pass_path }}"),
        ),
        (
            "TEST_PYPI_PASSWORD",
            get_password(
                password_store, "{{ cookiecutter.test_pypi_token_pass_path }}"
            ),
        ),
    ]

    try:
        print("        * Getting repository public key")
        public_key = get(
            url=(
                f"{github_url}/repos/{{ cookiecutter.github_user }}/"
                "{{ cookiecutter.project_slug }}/actions/secrets/public-key"
            ),
            token=github_token,
        ).json()
    except requests.exceptions.HTTPError:
        print("Error retrieving the repository public key")
        sys.exit(1)
    try:
        print("        * Getting repository secrets")
        response = get(
            url=(
                f"{github_url}/repos/{{ cookiecutter.github_user }}/"
                "{{ cookiecutter.project_slug }}/actions/secrets"
            ),
            token=github_token,
        ).json()
        repository_secrets = [secret["name"] for secret in response["secrets"]]
    except requests.exceptions.HTTPError:
        print("Error retrieving the repository secrets")
        sys.exit(1)

    for secret_name, secret in secrets:
        if secret_name in repository_secrets:
            continue
        print(f"        * Adding secret {secret_name}")
        try:
            get(
                url=(
                    f"{github_url}/repos/{{ cookiecutter.github_user }}/"
                    f"{{ cookiecutter.project_slug }}/actions/secrets/{secret_name}"
                ),
                method="put",
                data={
                    "encrypted_value": encrypt_secret(public_key["key"], secret),
                    "key_id": public_key["key_id"],
                },
                token=github_token,
            )
        except requests.exceptions.HTTPError:
            print(f"Error storing the secret {secret_name} in the github repository")
            sys.exit(1)


def main() -> None:
    """Run the post hooks."""
    print(
        """
#########################
# Post generation hooks #
#########################"""
    )

    password_store = passpy.Store()
    configure_github_repository(password_store)
    clean_unwanted_directories()


if __name__ == "__main__" and os.environ.get("COOKIECUTTER_TESTING") != "true":
    main()
