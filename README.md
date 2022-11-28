# GRAPHQL2PYTHON

Tools for GraphQL client in python.

## Installation

Install using

```bash
pip install graphql2python
```

## A Simple Example

For the query

```graphql
query HeroForEpisode($ep: Episode!) {
  hero(episode: $ep) {
    name
    ... on Droid {
      primaryFunction
    }
    ... on Human {
      height
    }
  }
}
```

we have

```python
from graphql2python.query import InlineFragment, Operation, Query, Variable, Argument

var_ep = Variable(name="ep", type="Episode!")
arg_episode = Argument(name="episode", value=var_ep)

hero = Query(
    name="hero",
    arguments=[arg_episode],
    fields=[
        "name",
        InlineFragment(type="Droid", fields=["primaryFunction"]),
        InlineFragment(type="Human", fields=["height"]),
    ]
)

operation = Operation(
    type="query",
    name="HeroForEpisode",
    queries=[hero],
    variables=[var_ep]
)
operation.render()
# query HeroForEpisode(
#   $ep: Episode!
# ) {
#   hero(
#     episode: $ep
#   ) {
#     name
#     ... on Droid {
#       primaryFunction
#     }
#     ... on Human {
#       height
#     }
#   }
# }
```