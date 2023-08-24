from pathlib import Path


ROOT = Path(__file__).parent
EXPERIMENTS = {
    "election88": [
        ROOT / "chapter_14/m1.stan",
        ROOT / "chapter_14/m2.stan",
        ROOT / "chapter_14/m2-nc.stan",
    ],
    "pilots": [
        ROOT / "chapter_22/pilots-1.stan",
        ROOT / "chapter_22/pilots-1-nc.stan",
    ],
}
