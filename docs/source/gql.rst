gql
====

The special example for `gql`_ users.

.. _gql: https://gql.readthedocs.io/en/latest/intro.html#less-dependencies

Step 1
------

Download GraphQL schema from https://countries.trevorblades.com/
and run **graphql2python** with her:

.. code-block:: yaml

  # graphql2python.yaml
  schema: ./schema.graphql
  output: ./model.py
  options:
    each_field_optional: true
    scalar_pytypes:
      Boolean: bool

You will receive the following file `model.py`:

.. code-block:: python

  """Auto-generated by graphql2python."""

  # pylint: disable-all
  # mypy: ignore-errors

  import enum
  import typing as _t
  from datetime import date, datetime

  from pydantic import BaseModel, Field

  __all__ = [
      "GraphQLBaseModel",
      # scalars
      "Boolean",
      "ID",
      "String",
      "_Any",
      # enums
      # unions
      "_Entity",
      # interfaces
      # objects
      "Continent",
      "Country",
      "Language",
      "State",
      "_Service",
  ]


  class GraphQLBaseModel(BaseModel):
      """Base Model for GraphQL object."""

      class Config:
          allow_population_by_field_name = True
          json_encoders = {
              # custom output conversion for datetime
              datetime: lambda dt: dt.isoformat()
          }
          smart_union = True


  # The `Boolean` scalar type represents `true` or `false`.
  Boolean = bool


  # The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID
  # type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an
  # input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
  ID = str


  # The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most
  # often used by GraphQL to represent free-form human-readable text.
  String = str


  # A Scalar type
  # See https://graphql.org/learn/schema/#scalar-types
  _Any = str


  # A Union type
  # See https://graphql.org/learn/schema/#union-types
  _Entity = _t.Union[
      'Continent',
      'Country',
      'Language',
  ]


  class Continent(GraphQLBaseModel):
      """
      An Object type
      See https://graphql.org/learn/schema/#object-types-and-fields
      """
      code: _t.Optional['ID'] = Field(default=None)
      countries: _t.Optional[_t.List['Country']] = Field(default_factory=list)
      name: _t.Optional['String'] = Field(default=None)
      typename__: _t.Literal["Continent"] = Field(default="Continent", alias="__typename")


  class Country(GraphQLBaseModel):
      """
      An Object type
      See https://graphql.org/learn/schema/#object-types-and-fields
      """
      capital: _t.Optional['String'] = Field(default=None)
      code: _t.Optional['ID'] = Field(default=None)
      continent: _t.Optional['Continent'] = Field(default=None)
      currency: _t.Optional['String'] = Field(default=None)
      emoji: _t.Optional['String'] = Field(default=None)
      emojiU: _t.Optional['String'] = Field(default=None)
      languages: _t.Optional[_t.List['Language']] = Field(default_factory=list)
      name: _t.Optional['String'] = Field(default=None)
      native: _t.Optional['String'] = Field(default=None)
      phone: _t.Optional['String'] = Field(default=None)
      states: _t.Optional[_t.List['State']] = Field(default_factory=list)
      typename__: _t.Literal["Country"] = Field(default="Country", alias="__typename")


  class Language(GraphQLBaseModel):
      """
      An Object type
      See https://graphql.org/learn/schema/#object-types-and-fields
      """
      code: _t.Optional['ID'] = Field(default=None)
      name: _t.Optional['String'] = Field(default=None)
      native: _t.Optional['String'] = Field(default=None)
      rtl: _t.Optional['Boolean'] = Field(default=None)
      typename__: _t.Literal["Language"] = Field(default="Language", alias="__typename")


  class State(GraphQLBaseModel):
      """
      An Object type
      See https://graphql.org/learn/schema/#object-types-and-fields
      """
      code: _t.Optional['String'] = Field(default=None)
      country: _t.Optional['Country'] = Field(default=None)
      name: _t.Optional['String'] = Field(default=None)
      typename__: _t.Literal["State"] = Field(default="State", alias="__typename")


  class _Service(GraphQLBaseModel):
      """
      An Object type
      See https://graphql.org/learn/schema/#object-types-and-fields
      """
      sdl: _t.Optional['String'] = Field(default=None)
      typename__: _t.Literal["_Service"] = Field(default="_Service", alias="__typename")


  Continent.update_forward_refs()
  Country.update_forward_refs()
  Language.update_forward_refs()
  State.update_forward_refs()
  _Service.update_forward_refs()

Step 2
------

Create the queries with graphql-query (https://github.com/denisart/graphql-query):

.. code-block:: python

  # queries.py
  from graphql_query import Operation, Query

  continents = Query(name="continents", fields=["code", "name"])
  getContinents = Operation(
      type="query",
      name="getContinents",
      queries=[continents]
  )

Step 3
------

Install **gql** and do magic

.. code-block:: python

  from gql import gql, Client
  from gql.transport.aiohttp import AIOHTTPTransport

  from queries import getContinents
  from model import Continent

  # Select your transport with a defined url endpoint
  transport = AIOHTTPTransport(url="https://countries.trevorblades.com/")

  # Create a GraphQL client using the defined transport
  client = Client(transport=transport, fetch_schema_from_transport=True)

  # Provide a GraphQL query
  query = gql(getContinents.render())

  # Execute the query on the transport
  result = client.execute(query)
  continents = [
      Continent.parse_obj(continent)
      for continent in result[getContinents.queries[0].name]
  ]

  print(continents)
  # [Continent(code='AF', countries=[], name='Africa', typename__='Continent'), Continent(code='AN', countries=[], name='Antarctica', typename__='Continent'), Continent(code='AS', countries=[], name='Asia', typename__='Continent'), Continent(code='EU', countries=[], name='Europe', typename__='Continent'), Continent(code='NA', countries=[], name='North America', typename__='Continent'), Continent(code='OC', countries=[], name='Oceania', typename__='Continent'), Continent(code='SA', countries=[], name='South America', typename__='Continent')]
