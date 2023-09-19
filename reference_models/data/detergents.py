import numpy as np
import pandas as pd
from pathlib import Path


def load_data() -> dict:
    raw = pd.read_csv(Path(__file__).parent / "detergents.csv")
    lookup = pd.Series(np.arange(raw.shape[1]), raw.columns)
    y = raw.choice.map(lookup)
    X = raw.values[:, 1:].astype(float)
    return {
        "n": raw.shape[0],
        "n_choices": y.nunique(),
        "X": X,
        "y": y,
    }
