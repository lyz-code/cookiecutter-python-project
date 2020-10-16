import os
import sys
from base64 import b64encode
from typing import Dict, Optional

import passpy
import requests
import sh
from nacl import encoding, public
from sh import git


def encrypt_secret(public_key: str, secret_value: str) -> str:
    """Encrypt a Unicode string using the public key."""
    public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))

    return b64encode(encrypted).decode("utf-8")


def get(
    url: str, token: str, method: str = "get", data: Optional[Dict] = None
) -> requests.models.Response:
    """
    Requests wrapper to handle errors and configuration.
    """

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
    print("* Initializing the project git repository")

    if ".git " not in sh.ls("-a"):
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
        except sh.ErrorReturnCode as e:
            print("There was an error creating the Git repository.")
            print(str(e.stderr, "utf8"))
            sys.exit(1)


def format_code() -> None:
    print("* Make repository Black linter compliant.")
    sh.black("setup.py", "src", "docs/examples", "tests")


def initialize_requirement_files() -> None:
    print("* Generate requirements.txt")
    sh.pip_compile("--allow-unsafe")
    print("    * Generate requirements-dev.txt")
    sh.pip_compile("--allow-unsafe", "requirements-dev.in")
    print("    * Generate docs/requirements.txt")
    sh.pip_compile(
        "--allow-unsafe",
        "docs/requirements.in",
        "--output-file",
        "docs/requirements.txt",
    )


def generate_virtualenv() -> None:
    pass

    # It seems it is not generating the virtualenv

    # sh.bash.bake(
    #     "mkvirtualenv",
    #     "--python=python3",
    #     "-a",
    #     directory_path,
    #     "{{ cookiecutter.project_slug }}",
    # )


def get_password(password_store: passpy.Store, password_path: str) -> str:
    try:
        password = password_store.get_key(password_path).strip()
    except Exception:
        print(f"Error retrieving the password from the path {password_path}")

    return password


def configure_github_repository() -> None:
    github_url = "https://api.github.com"
    print("* Configure the Github repository")
    password_store = passpy.Store()
    github_token = get_password(
        password_store, "{{ cookiecutter.github_token_pass_path }}"
    )

    print("    * Check if the repository exists")
    try:
        get(
            url=f"{github_url}/repos/{{ cookiecutter.github_user }}/{{ cookiecutter.project_slug }}",
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
                    "homepage": "https://{{ cookiecutter.github_user }}.github.io/{{ cookiecutter.project_slug }}",
                },
                token=github_token,
            )
        except Exception:
            print("Error creating the repository in github")
            sys.exit(1)

        print("    * Adding deploy keys to the Github repository")
        try:
            get(
                url=f"{github_url}/repos/{{ cookiecutter.github_user }}/{{ cookiecutter.project_slug }}/keys",
                method="post",
                data={
                    "key": get_password(
                        password_store,
                        "{{ cookiecutter.github_ssh_public_key_pass_path }}",
                    ),
                },
                token=github_token,
            )
        except Exception:
            print(f"Error storing the deployment public ssh key")
            sys.exit(1)

        print("    * Adding secrets to the Github repository")
        secrets = [
            (
                "ACTIONS_DEPLOY_KEY",
                get_password(
                    password_store, "{{ cookiecutter.github_ssh_key_pass_path }}"
                ),
            ),
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
                url=f"{github_url}/repos/{{ cookiecutter.github_user }}/{{ cookiecutter.project_slug }}/actions/secrets/public-key",
                token=github_token,
            ).json()
        except Exception:
            print("Error retrieving the repository public key")
            sys.exit(1)

        for secret_name, secret in secrets:
            print(f"        * Adding secret {secret_name}")
            try:
                get(
                    url=f"{github_url}/repos/{{ cookiecutter.github_user }}/{{ cookiecutter.project_slug }}/actions/secrets/{secret_name}",
                    method="put",
                    data={
                        "encrypted_value": encrypt_secret(public_key["key"], secret),
                        "key_id": public_key["key_id"],
                    },
                    token=github_token,
                )
            except Exception:
                print(
                    f"Error storing the secret {secret_name} in the github repository"
                )
                sys.exit(1)


def main() -> None:

    print(
        """
#########################
# Post generation hooks #
#########################"""
    )

    configure_github_repository()
    generate_virtualenv()
    initialize_requirement_files()
    format_code()
    initialize_git_repository()


if __name__ == "__main__":
    if os.environ.get("COOKIECUTTER_TESTING") != "true":
        main()
