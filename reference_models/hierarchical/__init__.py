from pathlib import Path


ROOT = Path(__file__).parent
EXPERIMENTS = {
    "election88": [
        ROOT / "chapter_14/m1.stan",
        ROOT / "chapter_14/m2.stan",
    ],
}
