import pandas as pd
from pathlib import Path
import re

from .util import get_consecutive_labels


def load_data(exclude_1992: bool = True) -> dict:
    raw = pd.read_csv(Path(__file__).parent / "presidential.csv").dropna()
    if exclude_1992:
        raw = raw[raw.year < 1992]
        assert len(raw) == 511, "number of records does not match page 383"
    year = pd.Series(get_consecutive_labels(raw.year))
    state = pd.Series(get_consecutive_labels(raw.state))
    return {
        "n": len(raw),
        "n_states": state.nunique(),
        "n_years": year.nunique(),
        "X_national": raw[[col for col in raw if re.fullmatch(r"n\d+", col)]],
        "X_state": raw[[col for col in raw if re.fullmatch(r"s\d+", col)]],
        "X_regional": raw[[col for col in raw if re.fullmatch(r"r\d+", col)]],
        "state": state,
        "year": year,
        "Dvote": raw.Dvote,
    }
