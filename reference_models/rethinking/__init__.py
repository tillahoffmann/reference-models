from pathlib import Path

from ..data import chimpanzees, reedfrogs, trolley
from ..util import Experiment, experiment_to_dict


EXPERIMENTS = experiment_to_dict(
    Experiment("chapter_11/m11-4.stan", chimpanzees.load_data),

    Experiment("chapter_12/m12-4.stan", trolley.load_data),
    Experiment("chapter_12/m12-5.stan", trolley.load_data),

    Experiment("chapter_13/m13-1.stan", reedfrogs.load_data),
    Experiment("chapter_13/m13-2.stan", reedfrogs.load_data),
    Experiment("chapter_13/m13-4.stan", chimpanzees.load_data),
    Experiment("chapter_13/m13-4nc.stan", chimpanzees.load_data),
    Experiment("chapter_13/m13-5.stan", chimpanzees.load_data),
    Experiment("chapter_13/m13-6.stan", chimpanzees.load_data),
    root=Path(__file__).parent
)
