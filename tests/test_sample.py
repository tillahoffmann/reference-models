from pathlib import Path
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
    args = ["--chains=1", "--iter-warmup=10", "--iter-sampling=5", "--summary", collection, dataset,
            model]
    sample.__main__(args)


def test_no_unused_stan_file() -> None:
    stan_files = {stan_file.resolve() for stan_file in Path("reference_models").glob("**/*.stan")
                  if "data" not in stan_file.parts}
    used_stan_files = {stan_file for experiments in COLLECTIONS.values() for stan_files in
                       experiments.values() for stan_file in stan_files}
    unused_stan_files = stan_files - used_stan_files
    assert not unused_stan_files
