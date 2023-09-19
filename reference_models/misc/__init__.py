from pathlib import Path

from ..data import detergents, pres_vote_historical
from ..util import Experiment, experiment_to_dict


EXPERIMENTS = experiment_to_dict(
    Experiment("detergents.stan", detergents.load_data),
    Experiment("pres_vote_historical-trangucci.stan", pres_vote_historical.load_data),
    root=Path(__file__).parent
)
