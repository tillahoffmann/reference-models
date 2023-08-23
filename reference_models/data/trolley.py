import pandas as pd
from pathlib import Path


def load_data() -> dict:
    raw = pd.read_csv(Path(__file__).parent / "trolley.csv")
    return {
        "n_experiments": len(raw),
        "n_responses": raw.response.nunique(),
        "response": raw.response,
    }
