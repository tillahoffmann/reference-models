from pathlib import Path

from .data import reedfrogs


ROOT = Path(__file__).parent
EXPERIMENTS = {
    "reedfrogs": {
        "load_data": reedfrogs.load_data,
        "stan_files": {
            "m13-1": ROOT / "chapter_13/m13-1.stan",
        },
    }
}
