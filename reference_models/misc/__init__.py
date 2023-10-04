from pathlib import Path

from ..data import behavior, detergents, pres_vote_historical
from ..util import Experiment, experiment_to_dict


EXPERIMENTS = experiment_to_dict(
    Experiment("behavior-i.stan", behavior.load_data),
    Experiment("behavior-iF.stan", behavior.load_data),
    Experiment("behavior-ihm.stan", behavior.load_data),
    Experiment("behavior-ihmF.stan", behavior.load_data),
    Experiment("detergents.stan", detergents.load_data),
    Experiment("pres_vote_historical-trangucci.stan", pres_vote_historical.load_data),
    Experiment("pres_vote_historical-2.stan", pres_vote_historical.load_data),
    root=Path(__file__).parent
)
