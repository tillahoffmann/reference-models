import pandas as pd
from pathlib import Path

from .util import check_consecutive_labels, get_consecutive_labels


def load_data() -> dict:
    raw = pd.read_csv(Path(__file__).parent / "election88.csv")
    state = get_consecutive_labels(raw.state)
    return {
        "n_responses": len(raw),
        "n_states": raw.state.nunique(),
        "n_ages": raw.age.nunique(),
        "n_edus": raw.edu.nunique(),
        "n_regions": raw.region_full.nunique(),
        "y": check_consecutive_labels(raw.y, 0, 1),
        "black": check_consecutive_labels(raw.black, 0, 1),
        "female": check_consecutive_labels(raw.female, 0, 1),
        "age": check_consecutive_labels(raw.age),
        "edu": check_consecutive_labels(raw.edu),
        "age_edu": check_consecutive_labels(raw.age_edu),
        "state": state,
        "region_full": check_consecutive_labels(raw.region_full),
        "v_prev_full": raw.v_prev_full,
    }
