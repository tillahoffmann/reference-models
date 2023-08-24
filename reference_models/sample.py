import argparse
from pathlib import Path
import shutil
from typing import Dict
import yaml

from . import COLLECTIONS
from .util import Experiment


class Args:
    chains: int | None
    iter_sampling: int | None
    iter_warmup: int | None
    output: Path | None
    seed: int | None
    experiment: str
    experiments: Dict[str, Experiment]
    summary: bool


def __main__(argv: dict | None = None) -> None:
    # Construct a hierarchical parser for different collections of models.
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", help="random number generator seed", type=int)
    parser.add_argument("--chains", help="number of chains", type=int)
    parser.add_argument("--iter-sampling", help="number of posterior samples per chain", type=int)
    parser.add_argument("--iter-warmup", help="number of warmup samples per chain", type=int)
    parser.add_argument("--summary", action="store_true", help="display summary")
    parser.add_argument("--output", "-o", help="path to output directory for CSV files", type=Path)

    collection_subparsers = parser.add_subparsers(required=True)
    for collection, experiments in COLLECTIONS.items():
        collection_subparser = collection_subparsers.add_parser(collection)
        collection_subparser.add_argument("experiment", choices=experiments)
        collection_subparser.set_defaults(experiments=experiments)

    # Parse the arguments and identify the experiment.
    args: Args = parser.parse_args(argv)
    experiment = args.experiments[args.experiment]

    # Compile the model and draw samples.
    model, fit = experiment.run(seed=args.seed, chains=args.chains, iter_warmup=args.iter_warmup,
                                iter_sampling=args.iter_sampling)

    # Save CSV files for later use.
    src_info = model.src_info()
    if args.output:
        # Remove the directory if it exists to avoid conflicting samples from different runs.
        if args.output.is_dir():
            shutil.rmtree(args.output)
        fit.save_csvfiles(args.output)
        with open(args.output / "metadata.yaml", "w") as fp:
            kwargs = {
                key: str(value) if isinstance(value, Path) else value for key, value in
                vars(args).items() if key != "experiments"
            }
            yaml.dump({
                "args": kwargs,
                "src_info": src_info,
            }, fp)

    # Display summary information for "raw" parameters.
    if args.summary:
        summary = fit.summary()
        fltr = summary.index.map(lambda name: name.split("[")[0] in src_info["parameters"])
        print(summary[fltr])


if __name__ == "__main__":
    __main__()
