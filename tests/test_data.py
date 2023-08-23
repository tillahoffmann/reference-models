import jsonschema
from pathlib import Path
import pandas as pd
import pytest
import yaml


DATASETS = Path("reference_models/data").glob("*.csv")


@pytest.mark.parametrize("dataset_path", DATASETS, ids=lambda path: path.name)
def test_dataset(dataset_path: Path) -> None:
    # Load the corresponding schema.
    schema_path = dataset_path.with_suffix(".schema.yaml")
    with schema_path.open("rb") as fp:
        schema = yaml.safe_load(fp)

    # Load and validate the data. We replace `nan` with `None` for json schema validation.
    dataset = pd.read_csv(dataset_path).replace(float("nan"), None)
    jsonschema.validate(dataset.to_dict(orient="records"), schema)
