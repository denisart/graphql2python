graphql2python.query usage examples
=====

Usage examples for queries from https://graphql.org/learn/queries/

Simple query
------------

Code for simple query from (see https://graphql.org/learn/queries/#fields)
with **graphql2python.query**

.. code-block:: python

  from graphql2python.query import Operation, Query

  hero = Query(name="hero", fields=["name"])
  operation = Operation(type="query", queries=[hero])

  print(operation.render())
  # query {
  #  hero {
  #    name
  #  }
  # }

Sub-fields
----------

Simple example with sub-field

.. code-block:: python

  from graphql2python.query import Field, Operation, Query

  hero = Query(
      name="hero",
      fields=[
          "name",
          Field(name="friends", fields=["name"])
      ]
  )
  operation = Operation(type="query", queries=[hero])

  print(operation.render())
  # query {
  #   hero {
  #     name
  #     friends {
  #       name
  #     }
  #   }
  # }

Arguments
---------

Code for query from https://graphql.org/learn/queries/#arguments

.. code-block:: python

  from graphql2python.query import Argument, Operation, Query, Field

  human = Query(
      name="human",
      arguments=[Argument(name="id", value='"1000"')],
      fields=[
          "name",
          Field(
              name="height",
              arguments=[Argument(name="unit", value="FOOT")]
          )
      ]
  )
  operation = Operation(type="query", queries=[human])
  # query {
  #   human(
  #     id: "1000"
  #   ) {
  #     name
  #     height(
  #       unit: FOOT
  #     )
  #   }
  # }

Aliases
-------

Example with aliases for queries

.. code-block:: python

  from graphql2python.query import Argument, Operation, Query

  empireHero = Query(
      name="hero",
      alias="empireHero",
      arguments=[Argument(name="episode", value="EMPIRE")],
      fields=["name"]
  )

  jediHero = Query(
      name="hero",
      alias="jediHero",
      arguments=[Argument(name="episode", value="JEDI")],
      fields=["name"]
  )

  operation = Operation(type="query", queries=[empireHero, jediHero])
  # query {
  #   empireHero: hero(
  #     episode: EMPIRE
  #   ) {
  #     name
  #   }
  #
  #   jediHero: hero(
  #     episode: JEDI
  #   ) {
  #     name
  #   }
  # }

Fragments
---------

Fragment in query is easy

.. code-block:: python

  from graphql2python.query import Argument, Operation, Query, Fragment, Field

  comparisonFields = Fragment(
      name="comparisonFields",
      type="Character",
      fields=["name", "appearsIn", Field(name="friends", fields=["name"])]
  )

  leftComparison = Query(
      name="hero",
      alias="leftComparison",
      arguments=[Argument(name="episode", value="EMPIRE")],
      fields=[comparisonFields]
  )

  rightComparison = Query(
      name="hero",
      alias="rightComparison",
      arguments=[Argument(name="episode", value="JEDI")],
      fields=[comparisonFields]
  )

  operation = Operation(
      type="query",
      queries=[leftComparison, rightComparison],
      fragments=[comparisonFields]
  )
  # query {
  #   leftComparison: hero(
  #     episode: EMPIRE
  #   ) {
  #     ...comparisonFields
  #   }
  #
  #   rightComparison: hero(
  #     episode: JEDI
  #   ) {
  #     ...comparisonFields
  #   }
  # }
  #
  # fragment comparisonFields on Character {
  #   name
  #   appearsIn
  #   friends {
  #     name
  #   }
  # }

Using variables inside fragments
--------------------------------

.. code-block:: python

  from graphql2python.query import Argument, Operation, Query, Fragment, Field, Variable

  var_first = Variable(name="first", type="Int", default="3")

  comparisonFields = Fragment(
      name="comparisonFields",
      type="Character",
      fields=[
          "name",
          Field(
              name="friendsConnection",
              arguments=[Argument(name="first", value=var_first)],
              fields=[
                  "totalCount",
                  Field(
                      name="edges",
                      fields=[
                          Field(name="node", fields=["name"])
                      ]
                  )
              ]
          )
      ]
  )

  leftComparison = Query(
      name="hero",
      alias="leftComparison",
      arguments=[Argument(name="episode", value="EMPIRE")],
      fields=[comparisonFields]
  )

  rightComparison = Query(
      name="hero",
      alias="rightComparison",
      arguments=[Argument(name="episode", value="JEDI")],
      fields=[comparisonFields]
  )

  operation = Operation(
      type="query",
      name="HeroComparison",
      queries=[leftComparison, rightComparison],
      fragments=[comparisonFields],
      variables=[var_first]
  )
  # query HeroComparison(
  #   $first: Int = 3
  # ) {
  #   leftComparison: hero(
  #     episode: EMPIRE
  #   ) {
  #     ...comparisonFields
  #   }
  #
  #   rightComparison: hero(
  #     episode: JEDI
  #   ) {
  #     ...comparisonFields
  #   }
  # }
  #
  # fragment comparisonFields on Character {
  #   name
  #   friendsConnection(
  #     first: $first
  #   ) {
  #     totalCount
  #     edges {
  #       node {
  #         name
  #       }
  #     }
  #   }
  # }

Operation name
--------------

Here’s an example that includes the keyword query as operation type and
HeroNameAndFriends as operation name:

.. code-block:: python

  from graphql2python.query import Operation, Query, Field

  hero = Query(
      name="hero",
      fields=["name", Field(name="friends", fields=["name"])]
  )

  operation = Operation(
      type="query",
      name="HeroNameAndFriends",
      queries=[hero],
  )
  # query HeroNameAndFriends {
  #   hero {
  #     name
  #     friends {
  #       name
  #     }
  #   }
  # }

Mutations
-------

Creating mutation is the same as creating query

.. code-block:: python

  from graphql2python.query import Argument, Operation, Query, Variable

  ep = Variable(name="ep", type="Episode!")
  review = Variable(name="review", type="ReviewInput!")

  createReview = Query(
      name="createReview",
      arguments=[
          Argument(name="episode", value=ep),
          Argument(name="review", value=review),
      ],
      fields=["stars", "commentary"]
  )

  operation = Operation(
      type="mutation",
      name="CreateReviewForEpisode",
      variables=[ep, review],
      queries=[createReview],
  )
  # mutation CreateReviewForEpisode(
  #   $ep: Episode!
  #   $review: ReviewInput!
  # ) {
  #   createReview(
  #     episode: $ep
  #     review: $review
  #   ) {
  #     stars
  #     commentary
  #   }
  # }

Inline Fragments
----------------

Example from https://graphql.org/learn/queries/#inline-fragments

.. code-block:: python

  from graphql2python.query import Argument, Operation, Query, Variable, InlineFragment

  ep = Variable(name="ep", type="Episode!")

  hero = Query(
      name="hero",
      arguments=[
          Argument(name="episode", value=ep),
      ],
      fields=[
          "stars",
          InlineFragment(type="Droid", fields=["primaryFunction"]),
          InlineFragment(type="Human", fields=["height"]),
      ]
  )

  operation = Operation(
      type="query",
      name="HeroForEpisode",
      variables=[ep],
      queries=[hero],
  )
  # query HeroForEpisode(
  #   $ep: Episode!
  # ) {
  #   hero(
  #     episode: $ep
  #   ) {
  #     stars
  #     ... on Droid {
  #       primaryFunction
  #     }
  #     ... on Human {
  #       height
  #     }
  #   }
  # }