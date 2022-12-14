# GRAPHQL2PYTHON

[![Build](https://img.shields.io/github/workflow/status/denisart/graphql2python/Code%20checking)](https://github.com/denisart/graphql2python/actions)
[![tag](https://img.shields.io/github/v/tag/denisart/graphql2python)](https://github.com/denisart/graphql2python)
[![last-commit](https://img.shields.io/github/last-commit/denisart/graphql2python/master)](https://github.com/denisart/graphql2python)
[![license](https://img.shields.io/github/license/denisart/graphql2python)](https://github.com/denisart/graphql2python/blob/master/LICENSE)

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
graphql2python render --config ./graphql2python.yaml
```
