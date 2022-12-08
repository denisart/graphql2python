.. graphql2python documentation master file, created by
   sphinx-quickstart on Tue Dec  6 15:53:57 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to graphql2python's documentation!
===================================

.. image:: https://img.shields.io/github/workflow/status/denisart/graphql2python/Code%20checking
  :alt: Build
.. image:: https://img.shields.io/github/v/tag/denisart/graphql2python
  :alt: tag
.. image:: https://img.shields.io/github/last-commit/denisart/graphql2python/master
  :alt: last-commit
.. image:: https://img.shields.io/github/license/denisart/graphql2python
  :alt: license

**graphql2python** is a tool that generates python code out of your GraphQL schema.
If you are using python as GraphQL client you can to generate GraphQL queries and
pydantic data-model with **graphql2python**.

**graphql2python** has the following tools for your python GraphQL client:

- python classes for generate of GraphQL queries;
- the function for generation of pydantic data-model by your GraphQL schema;
- ... (in future releases);

Documentation for version:  |version|

Contents
--------

.. toctree::

  guides

Quickstart
----------

Install with pip

.. code-block:: bash

  pip install graphql2python

Create the following file

.. code-block:: yaml

  # graphql2python.yaml
  schema: ./schema.graphql
  output: ./model.py

and run the following command

.. code-block:: bash

  graphql2python render --config ./graphql2python.yaml

See the documentation for all the possibilities (
while it is `docs/source/`).
