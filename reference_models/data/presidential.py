import pandas as pd
from pathlib import Path
import re
import yaml

from .util import check_consecutive_labels, get_consecutive_labels


def load_data(exclude_1992: bool = True) -> dict:
    path = Path(__file__).parent / "presidential.csv"
    raw = pd.read_csv(path).dropna()
    if exclude_1992:
        raw = raw[raw.year < 1992]
        assert len(raw) == 511, "number of records does not match page 383"

    # Obtain the region identifier from metadata.
    with path.with_suffix(".schema.yaml").open() as fp:
        schema = yaml.safe_load(fp)
    region_definitions = schema["metadata"]["regions"]
    region_definitions = {state: region for region, states in region_definitions.items() for state
                          in states}
    region = raw.state.map(region_definitions.__getitem__)
    # Convert to integers in a specific order for easier distinction between South and non-South in
    # `presidential-hierarchical.stan`.
    region_lookup = pd.Series({"south": 1, "northeast": 2, "midwest": 3, "west": 4})
    region = check_consecutive_labels(region_lookup.loc[region])

    year = pd.Series(get_consecutive_labels(raw.year))
    state = pd.Series(get_consecutive_labels(raw.state))
    X_national = raw[[col for col in raw if re.fullmatch(r"n\d+", col)]]
    X_state = raw[[col for col in raw if re.fullmatch(r"s\d+", col)]]
    X_regional = raw[[col for col in raw if re.fullmatch(r"r\d+", col)]]

    region_by_state = pd.DataFrame({"state": state.values, "region": region.values}) \
        .drop_duplicates().sort_values("state").region.values

    return {
        "n": len(raw),
        "n_states": state.nunique(),
        "n_years": year.nunique(),
        "n_regions": region.nunique(),
        "X_national": X_national - X_national.mean(),
        "X_state": X_state - X_state.mean(),
        "X_regional": X_regional - X_regional.mean(),
        "state": state,
        "year": year,
        "region": region,
        "Dvote": raw.Dvote,
        "region_by_state": region_by_state,
    }
