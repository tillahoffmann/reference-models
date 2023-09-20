import pandas as pd
from pathlib import Path
import yaml

from .util import get_consecutive_labels


def load_data(exclude_dc: bool = True) -> dict:
    csv_filename = Path(__file__).parent / "pres_vote_historical.csv"
    raw = pd.read_csv(csv_filename)
    if exclude_dc:
        raw = raw[raw.state != "DC"]

    # Get the region information.
    with open(csv_filename.with_suffix(".schema.yaml")) as fp:
        schema = yaml.safe_load(fp)
    region_lookup = {state: region for region, states in schema["metadata"]["regions"].items()
                     for state in states}
    raw["region"] = raw.state.map(region_lookup)

    # Convert categorical features to integers.
    raw["region_ind"] = get_consecutive_labels(raw.region)
    raw["year_ind"] = get_consecutive_labels(raw.year)
    raw["y"] = raw.rep / (raw.rep + raw.dem)

    # For states, we order them such that they are grouped by region. This means that the state
    # indices are not in alphabetical order. The region lookup already has states sorted by region
    # so we can re-use it.
    state_lookup = {state: i + 1 for i, state in enumerate(region_lookup)}
    raw["state_ind"] = raw.state.map(state_lookup)

    return {
        "n": raw.shape[0],
        "n_years": raw.year.nunique(),
        "n_states": raw.state.nunique(),
        "n_regions": raw.region_ind.nunique(),
        "year_ind": raw.year_ind,
        "state_ind": raw.state_ind,
        "region_ind": raw.region_ind,
        "state_region_ind": raw.groupby("state").region_ind.first(),
        "y": raw.y,
    }, raw
