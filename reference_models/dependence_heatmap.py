import argparse
import cmdstanpy
from matplotlib import pyplot as plt
from pathlib import Path
from snippets.plot import dependence_heatmap
from typing import List
import yaml


class Args:
    method: str
    all: bool
    samples: Path


def __main__(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--method", help="method to estimate dependence",
                        choices={"nmi", "corrcoef"}, default="corrcoef")
    parser.add_argument("--all", help="show all quantities instead of just 'raw' parameters",
                        action="store_true")
    parser.add_argument("samples", help="directory of samples", type=Path)
    args: Args = parser.parse_args(argv)

    # Load samples and source info.
    fit = cmdstanpy.from_csv(args.samples)
    with (args.samples / "src_info.yaml").open() as fp:
        src_info = yaml.safe_load(fp)

    # Obtain samples.
    samples = fit.stan_variables()
    if not args.all:
        samples = {key: value for key, value in samples.items() if key in src_info["parameters"]}

    # Plot the heatmap.
    fig, ax = plt.subplots()
    im = dependence_heatmap(samples, method=args.method, ax=ax)
    fig.colorbar(im, ax=ax, label=args.method)
    plt.show(block=True)


if __name__ == "__main__":
    __main__()
