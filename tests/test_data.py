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

    # Load the data, convert to records, and validate.
    dataset = pd.read_csv(dataset_path).to_dict(orient="records")
    jsonschema.validate(dataset, schema)
