import pytest
from reference_models import COLLECTIONS, sample


SPECS = [
    (collection, dataset, model) for collection, experiments in COLLECTIONS.items()
    for dataset, models in experiments.items()
    for model in models["stan_files"]
]


@pytest.mark.parametrize("collection, dataset, model", SPECS)
def test_sample(collection: str, dataset: str, model: str) -> None:
    sample.__main__([collection, dataset, model])
