import numpy as np
import pandas as pd
from pathlib import Path

from .util import check_consecutive_labels, get_consecutive_labels


def load_data(remove_dc: bool = False) -> dict:
    """
    Load CBS Press poll data for the 1988 presidential election.

    Args:
        remove_dc: Remove Washington DC (state 9 in the CSV file).
    """
    raw = pd.read_csv(Path(__file__).parent / "election88.csv")
    if remove_dc:
        raw = raw[raw.state != 9]
    state = get_consecutive_labels(raw.state)

    # Evaluate v_prev and region (state level) from v_prev_full and region_full (expanded to
    # response level). Both are required by model hierarchical/m2.stan due to the centered
    # parameterization.
    groups = raw.groupby("state")
    np.testing.assert_array_equal(groups.v_prev_full.nunique(), 1)
    v_prev = groups.v_prev_full.max()
    np.testing.assert_array_equal(groups.region_full.nunique(), 1)
    region = groups.region_full.max()

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

        "v_prev": v_prev,
        "region": region,
    }
