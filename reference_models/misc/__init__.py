from pathlib import Path

from ..data import detergents
from ..util import Experiment, experiment_to_dict


EXPERIMENTS = experiment_to_dict(
    Experiment("detergents.stan", detergents.load_data),
    root=Path(__file__).parent
)
