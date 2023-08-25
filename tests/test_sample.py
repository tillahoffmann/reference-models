import cmdstanpy
from pathlib import Path
import pytest
from reference_models import COLLECTIONS, sample


SPECS = [
    (collection, experiment) for collection, experiments in COLLECTIONS.items() for experiment in
    experiments
]


@pytest.mark.parametrize("collection, experiment", SPECS)
def test_sample(collection: str, experiment: str, tmp_path: Path) -> None:
    args = ["--chains=1", "--iter-warmup=10", "--iter-sampling=5", "--summary", "--output",
            str(tmp_path), collection, experiment]
    sample.__main__(args)

    assert isinstance(cmdstanpy.from_csv(tmp_path), cmdstanpy.CmdStanMCMC)
    assert (tmp_path / "metadata.yaml").is_file()


def test_no_unused_stan_file() -> None:
    stan_files = {stan_file.resolve() for stan_file in Path("reference_models").glob("*/**/*.stan")
                  if "data" not in stan_file.parts}
    used_stan_files = {experiment.stan_file for experiments in COLLECTIONS.values() for experiment
                       in experiments.values()}
    unused_stan_files = stan_files - used_stan_files
    assert not unused_stan_files
