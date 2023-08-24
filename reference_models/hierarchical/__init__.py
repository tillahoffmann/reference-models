from pathlib import Path

from ..data import election88, pilots
from ..util import Experiment, experiment_to_dict


EXPERIMENTS = experiment_to_dict(
    Experiment("chapter_14/m1.stan", election88.load_data),
    Experiment("chapter_14/m2.stan", election88.load_data),
    Experiment("chapter_14/m2-nc.stan", election88.load_data),
    Experiment("chapter_14/m2-nc.stan", election88.load_data, {"remove_dc": True},
               name="m2-nc-no-dc"),

    Experiment("chapter_22/pilots-1.stan", pilots.load_data),
    Experiment("chapter_22/pilots-1-nc.stan", pilots.load_data),
    root=Path(__file__).parent,
)
