from setuptools import setup

from graphql2python import __author__, __email__, __license__, __maintainer__, __version__


def do_setup():
    """Perform the package setup."""

    setup_kwargs = {
        "author": __author__,
        "maintainer": __maintainer__,
        "maintainer_email": __email__,
        "license": __license__,
    }

    setup(
        version=__version__,
        **setup_kwargs,  # type: ignore
    )


if __name__ == "__main__":
    do_setup()
