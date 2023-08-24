import pandas as pd
from pathlib import Path

from .util import get_consecutive_labels


def load_data() -> dict:
    raw = pd.read_csv(Path(__file__).parent / "pilots.csv")
    raw = raw.groupby(["group", "scenario"]).recovered.mean().reset_index()
    return {
        "n": len(raw),
        "n_groups": raw.group.nunique(),
        "n_scenarios": raw.scenario.nunique(),
        "group": get_consecutive_labels(raw.group),
        "scenario": get_consecutive_labels(raw.scenario),
        "y": raw.recovered,
    }
