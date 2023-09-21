import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import StandardScaler


def load_data() -> dict:
    raw = pd.read_csv(Path(__file__).parent / "radon.csv")
    x, u = StandardScaler().fit_transform(np.transpose([raw.x, raw.u])).T
    return {
        "n": len(raw),
        "x": x,
        "y": raw.y,
        "u": u,
        "county_ind": raw.county,
        "n_counties": raw.county.nunique(),
    }
