graphql2python.model usage examples
=====

Usage examples for schema from https://graphql.org/learn/schema/

Scalar
------

The generated scalar looks like this:

.. code-block:: graphql

  scalar DateTime

.. code-block:: python

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

The default type is **str**. For change this you can using options

.. code-block:: yaml

  # graphql2pythonConfig.yaml
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

For an enum definition:

.. code-block:: graphql

  enum Episode {
    NEWHOPE
    EMPIRE
    JEDI
  }

we have

.. code-block:: python

  class Episode(enum.Enum):
      """
      An Enum type
      See https://graphql.org/learn/schema/#enumeration-types
      """
      EMPIRE = "EMPIRE"
      JEDI = "JEDI"
      NEWHOPE = "NEWHOPE"

or with description

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

  class Episode(enum.Enum):
      """
      This means that wherever we use the type Episode in our schema
      we expect it to be exactly one of NEWHOPE, EMPIRE, or JEDI.
      """
      EMPIRE = "EMPIRE"
      JEDI = "JEDI"
      NEWHOPE = "NEWHOPE"