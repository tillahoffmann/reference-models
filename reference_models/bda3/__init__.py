from pathlib import Path

from ..data import presidential
from ..util import Experiment, experiment_to_dict


EXPERIMENTS = experiment_to_dict(
    Experiment("chapter_15/presidential-olr.stan", presidential.load_data),
    Experiment("chapter_15/presidential-hierarchical.stan", presidential.load_data),
    Experiment("chapter_15/presidential-hierarchical-nc.stan", presidential.load_data),
    root=Path(__file__).parent
)
