from pathlib import Path


ROOT = Path(__file__).parent
EXPERIMENTS = {
    "chimpanzees": [
        ROOT / "chapter_13/m13-4.stan",
        ROOT / "chapter_13/m13-5.stan",
    ],
    "reedfrogs": [
        ROOT / "chapter_13/m13-1.stan",
        ROOT / "chapter_13/m13-2.stan",
    ],
}
