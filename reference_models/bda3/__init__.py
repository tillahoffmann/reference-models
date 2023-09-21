from pathlib import Path

from ..data import latin_square, presidential, schools
from ..util import Experiment, experiment_to_dict


EXPERIMENTS = experiment_to_dict(
    Experiment("chapter_13/latin_square.stan", latin_square.load_data,
               sample_kwargs={"adapt_delta": 0.99}),
    Experiment("chapter_15/presidential-olr.stan", presidential.load_data),
    Experiment("chapter_15/presidential-hierarchical.stan", presidential.load_data),
    Experiment("chapter_15/presidential-hierarchical-nc.stan", presidential.load_data),
    Experiment("chapter_15/schools.stan", schools.load_data),
    Experiment("chapter_15/schools-nc.stan", schools.load_data),
    root=Path(__file__).parent
)
