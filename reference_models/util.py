import cmdstanpy
import os
from pathlib import Path
from time import time
from typing import Callable, Dict, Tuple


class Experiment:
    """
    Experimental configuration.

    Args:
        stan_file: Path to the Stan file.
        data_loader: Callable that returns data as a dictionary for cmstanpy.
        data_loader_kwargs: Keyword arguments supplied to :code:`data_loader`.
        name: Unique name of the experiment (inferred from :code:`stan_file` if not given).
        sample_kwargs: Keyword arguments passed to :meth:`cmdstanpy.CmdStanModel.sample`.
    """
    def __init__(self, stan_file: Path | str, data_loader: Callable[..., Dict],
                 data_loader_kwargs: Dict | None = None, name: str | None = None,
                 sample_kwargs: Dict | None = None) -> None:
        self.stan_file = Path(stan_file)
        self.data_loader = data_loader
        self.data_loader_kwargs = data_loader_kwargs or {}
        self.name = name or self.stan_file.with_suffix("").name
        self.sample_kwargs = sample_kwargs or {}

    def run(self, **kwargs) -> Tuple[cmdstanpy.CmdStanModel, cmdstanpy.CmdStanMCMC]:
        """
        Run the experiment.

        Args:
            **kwargs: Keyword arguments passed to :meth:`cmdstanpy.CmdStanModel.sample`.

        Returns:
            Model and posterior samples.
        """
        start = time()
        model = cmdstanpy.CmdStanModel(stan_file=self.stan_file, stanc_options=get_stanc_options(),
                                       compile=os.environ.get("CMDSTAN_COMPILE", True))
        compile_time = time() - start
        data = self.data_loader(**self.data_loader_kwargs)
        if isinstance(data, tuple):
            data, *_ = data
        start = time()
        fit = model.sample(data, **(self.sample_kwargs | kwargs))
        sample_time = time() - start
        return model, fit, {
            "compile_time": compile_time,
            "sample_time": sample_time,
        }


def experiment_to_dict(*experiments: Experiment, root: Path | None = None) -> Dict[str, Experiment]:
    """
    Convert a sequence of experiments to a dictionary with unique keys for easy lookup by name.
    """
    result = {}
    for experiment in experiments:
        if experiment.name in result:  # pragma: no cover
            raise ValueError(f"experiment with key `{experiment.name}` already exists")
        if root:
            experiment.stan_file = root / experiment.stan_file
        result[experiment.name] = experiment
    return result


def get_stanc_options() -> Dict:
    return {
        "include-paths": [Path(__file__).parent],
    }
