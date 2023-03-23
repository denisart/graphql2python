from graphql import (
    GraphQLScalarType,
    GraphQLEnumValue,
    GraphQLEnumType,
    GraphQLUnionType,
    GraphQLObjectType,
)

from graphql2python.type.definitions import (
    GraphQL2PythonScalarType,
    GraphQL2PythonEnumValue,
    GraphQL2PythonEnumType,
    GraphQL2PythonUnionType,
)


def test_scalar():
    """scalar Date"""

    scalar_graphql_core = GraphQLScalarType(name="Date", description="Custom scalar type.")

    scalar_graphql2python = GraphQL2PythonScalarType(
        graphql_core=scalar_graphql_core,
        name=scalar_graphql_core.name,
        description=scalar_graphql_core.description,
        pytype="datetime.date",
        alias="DateAlias",
    )

    assert scalar_graphql2python.graphql_core == scalar_graphql_core
    assert scalar_graphql2python.name == "Date"
    assert scalar_graphql2python.description == "Custom scalar type."
    assert scalar_graphql2python.pytype == "datetime.date"
    assert scalar_graphql2python.alias == "DateAlias"


def test_enum_value():
    enum_value_graphql_core = GraphQLEnumValue(
        value="JEDI", description="Value description.",
        deprecation_reason="Will be remove."
    )

    enum_value_graphql2python = GraphQL2PythonEnumValue(
        graphql_core=enum_value_graphql_core,
        name="JEDI",
        description=enum_value_graphql_core.description,
        deprecation_reason=enum_value_graphql_core.deprecation_reason
    )

    assert enum_value_graphql2python.graphql_core == enum_value_graphql_core
    assert enum_value_graphql2python.name == "JEDI"
    assert enum_value_graphql2python.description == "Value description."
    assert enum_value_graphql2python.deprecation_reason == "Will be remove."


def test_enum():
    """
    enum Episode {
      NEWHOPE
      EMPIRE
      JEDI
    }

    """

    enum_value_newhope = GraphQLEnumValue(value="NEWHOPE", description="New Hope episode.")
    enum_value_empire = GraphQLEnumValue(value="EMPIRE", description="Empire episode.")
    enum_value_jedi = GraphQLEnumValue(value="JEDI", description="Jedi episode.", deprecation_reason="Will be remove.")

    enum_graphql_core = GraphQLEnumType(
        name="Episode",
        values={
            "NEWHOPE": enum_value_newhope,
            "EMPIRE": enum_value_empire,
            "JEDI": enum_value_jedi,
        },
        description="StarWars episodes."
    )

    enum_graphql2python = GraphQL2PythonEnumType(
        graphql_core=enum_graphql_core,
        name=enum_graphql_core.name,
        description=enum_graphql_core.description,
        values=[
            GraphQL2PythonEnumValue(
                graphql_core=v,
                name=v_name,
                description=v.description,
                deprecation_reason=v.deprecation_reason
            )
            for v_name, v in enum_graphql_core.values.items()
        ]
    )

    assert enum_graphql2python.graphql_core == enum_graphql_core
    assert enum_graphql2python.name == "Episode"
    assert enum_graphql2python.description == "StarWars episodes."

    assert len(enum_graphql2python.values) == 3


def test_union():
    """union SearchResult = Human | Droid | Starship"""

    union_description = (
        "Wherever we return a SearchResult type in our schema, we might get a Human, a Droid, or a Starship."
    )

    human = GraphQLObjectType("Human", {})
    droid = GraphQLObjectType("Droid", {})
    starship = GraphQLObjectType("Starship", {})

    union_graphql_core = GraphQLUnionType(
        name="SearchResult",
        types=[human, droid, starship],
        description=union_description
    )

    union_graphq2python = GraphQL2PythonUnionType(
        graphql_core=union_graphql_core,
        name=union_graphql_core.name,
        description=union_graphql_core.description,
        types=[type_.name for type_ in union_graphql_core.types]
    )

    assert union_graphq2python.graphql_core == union_graphql_core
    assert union_graphq2python.name == "SearchResult"
    assert union_graphq2python.description == union_description
    assert union_graphq2python.types == ["Human", "Droid", "Starship"]
