import argparse
import arviz
import cmdstanpy
from matplotlib import pyplot as plt
from pathlib import Path
from snippets.plot import dependence_heatmap
from typing import List
import yaml


class Args:
    all: bool
    method: str
    output: Path | None
    samples: Path


def __main__(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--method", help="method to estimate dependence",
                        choices={"nmi", "corrcoef"}, default="corrcoef")
    parser.add_argument("--all", help="show all quantities instead of just 'raw' parameters",
                        action="store_true")
    parser.add_argument("--output", help="path to write the dependence heatmap figure to",
                        type=Path)
    parser.add_argument("samples", help="directory of samples", type=Path)
    args: Args = parser.parse_args(argv)

    # Load samples and source info.
    fit = cmdstanpy.from_csv(args.samples)
    with (args.samples / "metadata.yaml").open() as fp:
        metadata = yaml.safe_load(fp)

    # Obtain samples.
    samples = fit.stan_variables()
    src_info = metadata["src_info"]
    if not args.all:
        samples = {key: value for key, value in samples.items() if key in src_info["parameters"]}

    # Plot the heatmap.
    fig, ax = plt.subplots()
    im = dependence_heatmap(samples, method=args.method, ax=ax)
    fig.colorbar(im, ax=ax, label=args.method)
    fig.tight_layout()
    if args.output:
        fig.savefig(args.output)
    else:
        plt.show(block=True)

    # Report the WAIC if `log_lik` is available.
    if "log_lik" in src_info["generated quantities"]:
        waic = arviz.waic(arviz.from_cmdstanpy(fit))
        print(f"WAIC: {waic}")


if __name__ == "__main__":
    __main__()
