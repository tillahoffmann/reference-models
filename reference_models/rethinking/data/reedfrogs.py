import pandas as pd
from pathlib import Path


def load_data() -> dict:
    raw = pd.read_csv(Path(__file__).parent / "reedfrogs.csv")
    return {
        "n_tanks": len(raw),
        "density": raw.density,
        "surv": raw.surv,
    }
