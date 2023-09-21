import pandas as pd
from pathlib import Path


def load_data() -> dict:
    raw = pd.read_csv(Path(__file__).parent / "radon.csv")
    return {
        "n": len(raw),
        "x": raw.x,
        "y": raw.y,
        "u": raw.u,
        "county_ind": raw.county,
        "n_counties": raw.county.nunique(),
    }
