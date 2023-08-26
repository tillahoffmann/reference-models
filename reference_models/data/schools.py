import pandas as pd
from pathlib import Path


def load_data() -> dict:
    raw = pd.read_csv(Path(__file__).parent / "schools.csv")
    return {
        "n": len(raw),
        "y": raw.y,
        "sigma": raw.sigma,
    }
