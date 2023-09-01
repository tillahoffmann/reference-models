from docutils import nodes
from docutils.parsers.rst import Directive
import inspect
from pathlib import Path
import re
from reference_models import COLLECTIONS
from sphinx.application import Sphinx
import yaml


project = "Reference Models"
html_theme = "furo"
extensions = [
    "myst_parser",
]
exclude_patterns = [
    ".pytest_cache",
    "README.md",
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
        collection: str = self.arguments[0]
        experiments = COLLECTIONS[collection]
        stan_files = {experiment.stan_file: experiment.data_loader for experiment in
                      experiments.values()}

        root = nodes.inline()
        lines = []
        current_section = None
        for stan_file, data_loader in sorted(stan_files.items()):
            *_, section, name = stan_file.with_suffix("").parts
            if section != current_section:
                lines.extend([f"## {section.replace('_', ' ').title()}", ""])
                current_section = section

            text = stan_file.read_text()
            doc = re.match(r"/\*\s*(.*?)\s*\*/", text, re.DOTALL)
            if not doc:
                raise ValueError(f"missing documentation for stan_file `{stan_file}`")
            doc, = doc.groups()
            # {collection}-{section}-{model}
            target = "-".join(stan_file.with_suffix('').parts[-3:])
            dataset_name = data_loader.__module__.split(".")[-1]
            lines.extend([
                f"({target})=", f"### {name}", doc, "\n",
                f"Dataset: [{dataset_name}](#data-{dataset_name})", "\n"
            ])

        self.state.nested_parse(lines, 0, root, match_titles=True)

        return [root]


class DiscoverData(Directive):
    has_content = False
    required_arguments = 1
    optional_arguments = 0

    def run(self):
        loaders = {}
        for experiments in COLLECTIONS.values():
            for experiment in experiments.values():
                loaders.setdefault(experiment.data_loader, []).append(experiment.stan_file)

        root = nodes.inline()
        lines = []
        for loader in sorted(loaders, key=lambda x: x.__module__):
            # Get the data description.
            schema_file = Path(inspect.getfile(loader)).with_suffix(".schema.yaml")
            with open(schema_file) as fp:
                schema: dict = yaml.safe_load(fp)
            name, _ = schema_file.name.split(".", 1)
            description = schema.get("description")
            if not description:
                raise ValueError(f"missing documentation for schema file `{schema_file}`")
            lines.extend([f"(data-{name})=", f"## {name}", description])

            # Add references to the models that use the data.
            lines.append("### Models")
            for stan_file in sorted(set(loaders[loader])):
                target = "-".join(stan_file.with_suffix('').parts[-3:])
                lines.append(f"- [{'/'.join(stan_file.with_suffix('').parts[-3:])}](#{target})")

        self.state.nested_parse(lines, 0, root, match_titles=True)

        return [root]
