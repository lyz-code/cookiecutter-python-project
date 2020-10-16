import os


def main():

    print(
        """
########################
# Pre generation hooks #
########################"""
    )


if __name__ == "__main__":
    if os.environ.get("COOKIECUTTER_TESTING") != "true":
        main()
