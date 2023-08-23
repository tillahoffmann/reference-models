from pathlib import Path


ROOT = Path(__file__).parent
EXPERIMENTS = {
    "chimpanzees": [
        ROOT / "chapter_11/m11-4.stan",
        ROOT / "chapter_13/m13-4.stan",
        ROOT / "chapter_13/m13-4nc.stan",
        ROOT / "chapter_13/m13-5.stan",
        ROOT / "chapter_13/m13-6.stan",
    ],
    "reedfrogs": [
        ROOT / "chapter_13/m13-1.stan",
        ROOT / "chapter_13/m13-2.stan",
    ],
    "trolley": [
        ROOT / "chapter_12/m12-4.stan",
    ]
}
