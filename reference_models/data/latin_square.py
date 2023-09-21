import pandas as pd
from pathlib import Path

from .util import get_consecutive_labels


def load_data() -> dict:
    raw = pd.read_csv(Path(__file__).parent / "latin_square.csv")
    return {
        "n": len(raw),
        "row_idx": raw.row_idx,
        "col_idx": raw.col_idx,
        "treatment": get_consecutive_labels(raw.treatment),
        "yield": raw["yield"],
    }
