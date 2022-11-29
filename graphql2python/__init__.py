"""GRAPHQL2PYTHON

Tools for GraphQL client in python:

    - A simple GraphQL client;
    - Auto generated pydantic classes from a GraphQL schema;
    - Auto generated GraphQL queries;
    - e.t.c

The sub-packages:

    - `graphql2python.client`:
    - `graphql2python.model`: The package with the pydantic datamodel generator from some GraphQL schema;
    - `graphql2python.query`: Tools for generate GraphQL queries from python classes;

"""

from .__info__ import __author__, __email__, __license__, __maintainer__
from .__version__ import __version__

__all__ = [
    "__version__",
    "__email__",
    "__author__",
    "__license__",
    "__maintainer__",
]
