# GRAPHQL2PYTHON

[![Build](https://img.shields.io/github/actions/workflow/status/denisart/graphql2python/check.yml)](https://github.com/denisart/graphql2python/actions)
[![tag](https://img.shields.io/github/v/tag/denisart/graphql2python)](https://github.com/denisart/graphql2python)
[![last-commit](https://img.shields.io/github/last-commit/denisart/graphql2python/master)](https://github.com/denisart/graphql2python)
[![license](https://img.shields.io/github/license/denisart/graphql2python)](https://github.com/denisart/graphql2python/blob/master/LICENSE)

---
**NOTE.** Please use the package [datamodel-code-generator](https://github.com/koxudaxi/datamodel-code-generator) to generate data model from a GraphQL schema.
---

**graphql2python** is a tool that generates python code out of your GraphQL schema.
If you are using python as GraphQL client you can to generate
pydantic data-model with **graphql2python**. The documentation for **graphql2python**
can be found at [https://denisart.github.io/graphql2python](https://denisart.github.io/graphql2python).

GraphQL query generation moved to https://github.com/denisart/graphql-query

The special example for [gql](https://gql.readthedocs.io/en/latest/index.html) users [here](https://denisart.github.io/graphql2python/gql.html).

## Quickstart

Install with pip

```bash
pip install graphql2python
```

Create the following file

```yaml
# graphql2python.yaml
schema: ./schema.graphql
output: ./model.py
```

and run the following command

```bash
graphql2python generate --config ./graphql2python.yaml
```

## Config reference

Global keywords

| keyword        | description                                                   |
|----------------|---------------------------------------------------------------|
| `schema`       | A path to the target GraphQL schema file.                     |
| `output`       | A file name for output `py` file.                             |
| `license_file` | An optional path to a file with license for output `py` file. |
| `options`      | Optional options for generate of output `py` file.            |

Options keywords

| keywords              | description                                                                                                            |
|-----------------------|------------------------------------------------------------------------------------------------------------------------|
| `max_line_len`        | The maximum of line length of output `py` file. Default is `120`.                                                      |
| `name_suffix`         | A suffix for invalid field name (as python object name). Default is `"_"`.                                             |
| `each_field_optional` | Each fields of interfaces and objects are optional. Default is `false`.                                                |
| `add_from_dict`       | Add `from_dict` (dict -> model) method to the general class. Default is `false`.                                       |
| `add_to_dict`         | Add `to_dict` (model -> dict) method to the general class. Default is `false`.                                         |
| `scalar_pytypes`      | A dict with python types for custom GraphQL scalars. Maps from scalar name to python type name. Default is empty dict. |
| `fields_setting`      | Settings for interfaces or objects fields. Maps from object name to a dict with setting. Default is empty dict.        |

`fields_setting` keywords for some object name

| keywords   | desciption                                                            |
|------------|-----------------------------------------------------------------------|
| `alias`    | An alias for a field (see Field.alias for pydantic). Default is null. |
| `new_name` | A new name for a field. Default is null.                              |

An example for `graphql2python.yaml` config:

```yaml
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
```
