import pytest
from reference_models import COLLECTIONS, sample


SPECS = [
    (collection, dataset, stan_file.with_suffix("").name)
    for collection, experiments in COLLECTIONS.items()
    for dataset, stan_files in experiments.items()
    for stan_file in stan_files
]


@pytest.mark.parametrize("collection, dataset, model", SPECS)
def test_sample(collection: str, dataset: str, model: str) -> None:
    sample.__main__([collection, dataset, model])
