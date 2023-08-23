import pandas as pd
from pathlib import Path


def load_data() -> dict:
    raw = pd.read_csv(Path(__file__).parent / "chimpanzees.csv")
    # R code 11.2 on page 326 to encode both the presence of a partner and location of the prosocial
    # option.
    treatment = 1 + raw.prosoc_left + 2 * raw.condition
    return {
        "n_actors": raw.actor.nunique(),
        "n_experiments": len(raw),
        "n_blocks": raw.block.nunique(),
        "actor": raw.actor,
        "block": raw.block,
        "pulled_left": raw.pulled_left,
        "treatment": treatment,
    }
