from pathlib import Path
from reference_models import dependence_heatmap, sample
from unittest import mock


def test_dependence_heatmap(tmp_path: Path) -> None:
    args = ["--chains=1", "--iter-warmup=10", "--iter-sampling=5", "--summary", "--output",
            str(tmp_path), "rethinking", "chimpanzees", "m11-4"]
    sample.__main__(args)
    with mock.patch("matplotlib.pyplot.show"):
        dependence_heatmap.__main__([str(tmp_path)])
