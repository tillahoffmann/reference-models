import cmdstanpy
from pathlib import Path
from typing import Callable, Dict, Tuple


class Experiment:
    """
    Experimental configuration.

    Args:
        stan_file: Path to the Stan file.
        data_loader: Callable that returns data as a dictionary for cmstanpy.
        data_loader_kwargs: Keyword arguments supplied to :code:`data_loader`.
        name: Unique name of the experiment (inferred from :code:`stan_file` if not given).
    """
    def __init__(self, stan_file: Path | str, data_loader: Callable[..., Dict],
                 data_loader_kwargs: Dict | None = None, name: str | None = None) -> None:
        self.stan_file = Path(stan_file)
        self.data_loader = data_loader
        self.data_loader_kwargs = data_loader_kwargs or {}
        self.name = name or self.stan_file.with_suffix("").name

    def run(self, **kwargs) -> Tuple[cmdstanpy.CmdStanModel, cmdstanpy.CmdStanMCMC]:
        """
        Run the experiment.

        Args:
            **kwargs: Keyword arguments passed to :meth:`cmdstanpy.CmdStanModel.sample`.

        Returns:
            Model and posterior samples.
        """
        model = cmdstanpy.CmdStanModel(stan_file=self.stan_file, stanc_options=get_stanc_options())
        data = self.data_loader(**self.data_loader_kwargs)
        fit = model.sample(data, **kwargs)
        return model, fit


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
