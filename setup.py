from graphql2python import __version__

from setuptools import setup


def do_setup():
    """Perform the package setup."""

    setup_kwargs = {}

    setup(
        version=__version__,
        **setup_kwargs,  # type: ignore
    )


if __name__ == "__main__":
    do_setup()
