GraphQL schema
=====

graphql2python has the function for generation of
pydantic data-model by your GraphQL schema. Below are examples of
using these classes for schema from GraphQL documentation https://graphql.org/learn/schema/

Scalar
------

The generated scalar looks like this:

.. code-block:: graphql

  # in schema.graphql
  scalar DateTime

.. code-block:: python

  ...

  # The `Boolean` scalar type represents `true` or `false`.
  Boolean = str


  # A Scalar type
  # See https://graphql.org/learn/schema/#scalar-types
  DateTime = str


  # The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most
  # often used by GraphQL to represent free-form human-readable text.
  String = str

or with comment

.. code-block:: graphql

  "in the format: dd/mm/yyyy"
  scalar DateTime

.. code-block:: python

  ...

  # in the format: dd/mm/yyyy
  DateTime = str

  ...

The default python type for generated scalars is **str**.
For change this you can using special option in **graphql2python** config:

.. code-block:: yaml

  # graphql2python.yaml
  schema: ...
  output: ...
  options:
    scalar_pytypes:
      String: str
      Float: float
      Int: int
      ID: str
      Boolean: bool
      DateTime: datetime

.. code-block:: python

  ...

  # The `Boolean` scalar type represents `true` or `false`.
  Boolean = bool


  # in the format: dd/mm/yyyy
  DateTime = datetime


  # The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most
  # often used by GraphQL to represent free-form human-readable text.
  String = str

  ...

Enum
----

GraphQL Enum objects rendered as Python **enum.Enum** classes

.. code-block:: graphql

  # in schema.graphql
  enum Episode {
    NEWHOPE
    EMPIRE
    JEDI
  }

.. code-block:: python

  ...

  class Episode(enum.Enum):
      """
      An Enum type
      See https://graphql.org/learn/schema/#enumeration-types
      """
      EMPIRE = "EMPIRE"
      JEDI = "JEDI"
      NEWHOPE = "NEWHOPE"

Or with Enum description

.. code-block:: graphql

  """
  This means that wherever we use the type Episode in our schema
  we expect it to be exactly one of NEWHOPE, EMPIRE, or JEDI.
  """
  enum Episode {
    NEWHOPE
    EMPIRE
    JEDI
  }

.. code-block:: python

  ...

  class Episode(enum.Enum):
      """
      This means that wherever we use the type Episode in our schema
      we expect it to be exactly one of NEWHOPE, EMPIRE, or JEDI.
      """
      EMPIRE = "EMPIRE"
      JEDI = "JEDI"
      NEWHOPE = "NEWHOPE"

Union
-----

GraphQL Union objects rendered as Python **typing.Union**

.. code-block:: graphql

  ...

  """
  Wherever we return a SearchResult type in our schema,
  we might get a Human, a Droid, or a Starship.
  """
  union SearchResult = Human | Droid | Starship

we have

.. code-block:: python

  ...

  # Wherever we return a SearchResult type in our schema,
  # we might get a Human, a Droid, or a Starship.
  SearchResult = _t.Union[
      'Droid',
      'Human',
      'Starship',
  ]

  ...

Since **input.Union** cannot contain a single element
for such Unions we have the following

.. code-block:: graphql

  ...

  """
  Wherever we return a SearchResult type in our schema,
  we might get a Human, a Droid, or a Starship.
  """
  union SearchResult = Human

.. code-block:: python

  ...

  # Wherever we return a SearchResult type in our schema,
  # we might get a Human, a Droid, or a Starship.
  SearchResult = _t.TypeVar('SearchResult', bound='Human')

  ...

Object and interfaces
---------------------

Rendered Interfaces and Objects are inherited from the main class

.. code-block:: python

  class GraphQLBaseModel(BaseModel):
      """Base Model for GraphQL object."""

      class Config:
          allow_population_by_field_name = True
          json_encoders = {
              # custom output conversion for datetime
              datetime: lambda dt: dt.isoformat()
          }
          smart_union = True

So for the following diagram

.. code-block:: graphql

  enum Episode {
    NEWHOPE
    EMPIRE
    JEDI
  }

  "an interface Character that represents any character in the Star Wars trilogy"
  interface Character {
    id: ID!
    name: String!
    friends: [Character]
    appearsIn: [Episode]!
  }

  type Human implements Character {
    id: ID!
    name: String!
    friends: [Character]
    appearsIn: [Episode]!
    starships: [Starship]
    totalCredits: Int
  }

  type Droid implements Character {
    id: ID!
    name: String!
    friends: [Character]
    appearsIn: [Episode]!
    primaryFunction: String
  }

  type Starship implements Character {
    id: ID!
    name: String!
    friends: [Character]
    appearsIn: [Episode]!
    length: Float
  }

we have the following python code

.. code-block:: python

  ...

  class Character(GraphQLBaseModel):
      """
      an interface Character that represents any character in the Star Wars trilogy
      """
      appearsIn: _t.List[_t.Optional['Episode']]
      id: 'ID'
      name: 'String'
      friends: _t.Optional[_t.List[_t.Optional['Character']]] = Field(default_factory=list)
      typename__: _t.Literal["Character"] = Field(default="Character", alias="__typename")


  class Droid(
      Character,
  ):
      """
      An Object type
      See https://graphql.org/learn/schema/#object-types-and-fields
      """
      primaryFunction: _t.Optional['String'] = Field(default=None)
      typename__: _t.Literal["Droid"] = Field(default="Droid", alias="__typename")


  class Human(
      Character,
  ):
      """
      An Object type
      See https://graphql.org/learn/schema/#object-types-and-fields
      """
      starships: _t.Optional[_t.List[_t.Optional['Starship']]] = Field(default_factory=list)
      totalCredits: _t.Optional['Int'] = Field(default=None)
      typename__: _t.Literal["Human"] = Field(default="Human", alias="__typename")


  class Starship(
      Character,
  ):
      """
      An Object type
      See https://graphql.org/learn/schema/#object-types-and-fields
      """
      length: _t.Optional['Float'] = Field(default=None)
      typename__: _t.Literal["Starship"] = Field(default="Starship", alias="__typename")


  Character.update_forward_refs()
  Droid.update_forward_refs()
  Human.update_forward_refs()
  Starship.update_forward_refs()

Rename field
------------

For rename field we can using the following config:

.. code-block:: yaml

  # graphql2python.yaml
  schema: ./schema.graphql
  output: ./output.py
  options:
    fields_setting:
      Character:
        name:
          alias: name
          new_name: character_name

.. code-block:: graphql

  enum Episode {
    NEWHOPE
    EMPIRE
    JEDI
  }

  interface Character {
    id: ID!
    name: String!
    friends: [Character]
    appearsIn: [Episode]!
  }

.. code-block:: python

  class Character(GraphQLBaseModel):
      """
      An Interface type
      See https://graphql.org/learn/schema/#interfaces
      """
      appearsIn: _t.List[_t.Optional['Episode']]
      id: 'ID'
      character_name: 'String' = Field(..., alias='name')
      friends: _t.Optional[_t.List[_t.Optional['Character']]] = Field(default_factory=list)
      typename__: _t.Literal["Character"] = Field(default="Character", alias="__typename")