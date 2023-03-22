.. graphql2python documentation master file, created by
   sphinx-quickstart on Tue Dec  6 15:53:57 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to graphql2python's documentation!
===================================

.. image:: https://img.shields.io/github/actions/workflow/status/denisart/graphql2python/check.yml
  :alt: Build
.. image:: https://img.shields.io/github/v/tag/denisart/graphql2python
  :alt: tag
.. image:: https://img.shields.io/github/last-commit/denisart/graphql2python/master
  :alt: last-commit
.. image:: https://img.shields.io/github/license/denisart/graphql2python
  :alt: license

**graphql2python** is a tool that generates python code out of your GraphQL schema.
If you are using python as GraphQL client you can to generate
pydantic data-model with **graphql2python**.

GraphQL query generation moved to https://github.com/denisart/graphql-query

Documentation for version:  |version|

Contents
--------

.. toctree::

  guides
  examples

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

  graphql2python generate --config ./graphql2python.yaml

See the documentation for all the possibilities (
while it is `docs/source/`).

Config reference
----

Global keywords

.. list-table::
  :widths: auto
  :align: left

  * - keyword
    - description
  * - `schema`
    - A path to the target GraphQL schema file.
  * - `output`
    - A file name for output `py` file.
  * - `license_file`
    - An optional path to a file with license for output `py` file.
  * - `options`
    - Optional options for generate of output `py` file.

Options keywords

.. list-table::
  :widths: auto
  :align: left

  * - keywords
    - description
  * - `max_line_len`
    - The maximum of line length of output `py` file. Default is `120`.
  * - `name_suffix`
    - A suffix for invalid field name (as python object name). Default is `"_"`.
  * - `each_field_optional`
    - Each fields of interfaces and objects are optional. Default is `false`.
  * - `add_from_dict`
    - Add `from_dict` (dict -> model) method to the general class. Default is `false`.
  * - `add_to_dict`
    - Add `to_dict` (model -> dict) method to the general class. Default is `false`.
  * - `scalar_pytypes`
    - A dict with python types for custom GraphQL scalars. Maps from scalar name to python type name. Default is empty dict.
  * - `fields_setting`
    - Settings for interfaces or objects fields. Maps from object name to a dict with setting. Default is empty dict.

`fields_setting` keywords for some object name

.. list-table::
  :widths: auto
  :align: left

  * - keywords
    - description
  * - `alias`
    - An alias for a field (see Field.alias for pydantic). Default is null.
  * - `new_name`
    - A new name for a field. Default is null.

An example for `graphql2python.yaml` config:

.. code-block:: yaml

  # graphql2python.yaml
  schema: ./schema/schema.graphql
  output: ./model/model.py
  license_file: ./LICENSE
  options:
    scalar_pytypes:
      String: str
      Float: float
      Int: int
      ID: str
      Boolean: bool
      DateTime: datetime
      Date: date
    max_line_len: 79
    each_field_optional: true
    fields_setting:
      MyObjectName:
        from:
          alias: from
          new_name: correct_from
