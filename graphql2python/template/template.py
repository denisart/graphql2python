from pathlib import Path
from typing import Any, Dict, List, Optional

from graphql import GraphQLScalarType
from jinja2 import Environment, FileSystemLoader, Template, TemplateNotFound

__all_ = [
    "TemplatesManager",
]


TEMPLATES_PYDANTIC = Path(__file__).parent / Path("templates/pydantic")


class TemplatesManager:
    """Jinja2 templates manager for GraphQL2Python.

    Args:
        custom_template_dir: A dir to custom templates.
            Will first search for a template in this directory.

    """

    supported_templates = [
        "comment.jinja2",
        "scalar.jinja2",
    ]

    def __init__(
        self,
        custom_template_dir: Optional[Path] = None,
    ):
        self._default_templates_folder = TEMPLATES_PYDANTIC
        self._custom_templates_folder = custom_template_dir or self._default_templates_folder

        self._default_templates_env = Environment(loader=FileSystemLoader(searchpath=self._default_templates_folder))
        self._custom_templates_env = Environment(loader=FileSystemLoader(searchpath=self._custom_templates_folder))

    def get_template(self, template_name: str) -> Template:
        """Get a template by name.

        Will first search for a template in custom_template_dir. If not found here
        then will search in default templates directory.

        Args:
             template_name: the name of target template.

        """

        if template_name not in self.supported_templates:
            raise ValueError(f"Invalid template name. Must be one of: {self.supported_templates}")

        try:
            return self._custom_templates_env.get_template(template_name)
        except TemplateNotFound:
            return self._default_templates_env.get_template(template_name)

    def render_comment(
        self,
        lines: List[str],
        indent: int = 0,
        extra_template_data: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Render a comment with `comment.jinja2` template.

        Args:
            lines: comment lines.
            indent: optional indent length for each line.
            extra_template_data: extra template data for custom template.

        """

        if len(lines) == 0:
            lines = ["..."]

        return self.get_template("comment.jinja2").render(
            lines=lines,
            indent=" " * indent,
            extra_template_data=extra_template_data,
        )

    def render_scalar(
        self,
        scalar_object: GraphQLScalarType,
        pytype: str,
        alias: Optional[str] = None,
        extra_template_data: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Render a Scalar object.

        Args:
            scalar_object: a target Scalar object.
            pytype: python type for the scalar.
            alias: optional alias for the scalar name.
            extra_template_data: some data for custom template.

        """

        return self.get_template("scalar.jinja2").render(
            obj=scalar_object,
            pytype=pytype,
            alias=alias,
            comment_template=self.get_template("comment.jinja2"),
            extra_template_data=extra_template_data,
        )
