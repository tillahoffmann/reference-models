from pathlib import Path

from ..data import election88, latin_square, radon, pilots
from ..util import Experiment, experiment_to_dict


EXPERIMENTS = experiment_to_dict(
    Experiment("chapter_12/radon_m0.stan", radon.load_data),
    Experiment("chapter_12/radon_m0_nc.stan", radon.load_data),
    Experiment("chapter_12/radon_m1_nc.stan", radon.load_data),

    Experiment("chapter_13/latin_square_with_predictors.stan", latin_square.load_data,
               sample_kwargs={"adapt_delta": 0.99}),

    Experiment("chapter_14/m1.stan", election88.load_data),
    Experiment("chapter_14/m2.stan", election88.load_data),
    Experiment("chapter_14/m2-nc.stan", election88.load_data),
    Experiment("chapter_14/m2-nc.stan", election88.load_data, {"remove_dc": True},
               name="m2-nc-no-dc"),

    Experiment("chapter_22/latin_square_without_predictors.stan", latin_square.load_data),
    Experiment("chapter_22/pilots-1.stan", pilots.load_data),
    Experiment("chapter_22/pilots-1-nc.stan", pilots.load_data),
    root=Path(__file__).parent,
)
