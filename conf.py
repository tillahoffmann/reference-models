from docutils import nodes
from docutils.parsers.rst import Directive
from pathlib import Path
import re
from sphinx.application import Sphinx
import yaml


project = "Reference Models"
html_theme = "furo"
extensions = [
    "myst_parser",
]
exclude_patterns = [
    ".pytest_cache",
    "venv",
]


def setup(app: Sphinx) -> None:
    app.add_directive("discover_data", DiscoverData)
    app.add_directive("discover_models", DiscoverModels)


class DiscoverModels(Directive):
    has_content = False
    required_arguments = 1
    optional_arguments = 0

    def run(self):
        path: str = self.arguments[0]
        source = Path(self.state.document.attributes["source"])
        directory = (source.parent / path).resolve()

        root = nodes.inline()
        lines = []
        current_section = None
        for stan_file in sorted(directory.glob("*/*.stan")):
            *_, section, name = stan_file.with_suffix("").parts
            if section != current_section:
                lines.extend([f"## {section.replace('_', ' ').title()}", ""])
                current_section = section

            text = stan_file.read_text()
            doc = re.match(r"/\*\s*(.*?)\s*\*/", text, re.DOTALL)
            if not doc:
                raise ValueError(f"missing documentation for stan_file `{stan_file}`")
            doc, = doc.groups()
            lines.extend([f"### {name}", doc, "\n"])

        self.state.nested_parse(lines, 0, root, match_titles=True)

        return [root]


class DiscoverData(Directive):
    has_content = False
    required_arguments = 1
    optional_arguments = 0

    def run(self):
        path: str = self.arguments[0]
        source = Path(self.state.document.attributes["source"])
        directory = (source.parent / path).resolve()

        root = nodes.inline()
        lines = []
        for schema_file in sorted(directory.glob("*.schema.yaml")):
            with open(schema_file) as fp:
                schema: dict = yaml.safe_load(fp)
            name, _ = schema_file.name.split(".", 1)
            description = schema.get("description")
            if not description:
                raise ValueError(f"missing documentation for schema file `{schema_file}`")
            lines.extend([f"## {name}", description])

        self.state.nested_parse(lines, 0, root, match_titles=True)

        return [root]
