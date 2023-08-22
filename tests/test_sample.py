import pytest
from reference_models import sample


@pytest.mark.parametrize("collection, dataset, model", sample.discover_experiments().values[:, :3])
def test_sample(collection: str, dataset: str, model: str) -> None:
    sample.__main__([collection, dataset, model])
