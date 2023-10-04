import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import LabelEncoder, StandardScaler


def _parse_time(time: str) -> float:
    hour, minute = time.split(":")
    return (float(hour) + float(minute) / 60) / 24


def load_data() -> dict:
    # Load the data and preprocess as in `Publication script.R` from the supplement of Koster and
    # McElreath (2017).
    raw = pd.read_csv(Path(__file__).parent / "behavior.csv")

    age, house_size, log_wealth, rain, time = StandardScaler().fit_transform(np.transpose([
        raw.age, raw.dynamic_house_size, np.log(raw.wealth), raw.rain, raw.time.apply(_parse_time),
    ])).T
    saturday = (raw.day == "Saturday").astype(float)
    sunday = (raw.day == "Sunday").astype(float)
    X = np.transpose([
        age, age ** 2, log_wealth, sunday, saturday, time, time ** 2, house_size, rain
    ])

    return {
        "N": len(raw),
        "K": raw.response.nunique(),
        "y": LabelEncoder().fit_transform(raw.response) + 1,
        "N_id": raw.subject_id.max(),
        "id": raw.subject_id,
        "N_house": raw.house.max(),
        "house_id": raw.house,
        "N_month": raw.month.max(),
        "month_id": raw.month,
        "age_z": age,
        "age_zq": age ** 2,
        "time_z": time,
        "time_zq": time ** 2,
        "rain_z": rain,
        "house_size_z": house_size,
        "wz": log_wealth,
        "saturday": saturday,
        "sunday": sunday,
        "X": X,
    }
