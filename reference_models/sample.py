import argparse
import cmdstanpy
from pathlib import Path
import shutil
from typing import Dict
import yaml

from . import COLLECTIONS
from .data import DATA_LOADERS


class Args:
    chains: int | None
    collection: str
    dataset: str
    iter_sampling: int | None
    iter_warmup: int | None
    model: str
    output: Path | None
    stan_file_by_model: Dict[str, Path]
    summary: bool


def __main__(argv: dict | None = None) -> None:
    # Construct hierarchical parsers.
    parser = argparse.ArgumentParser()
    parser.add_argument("--chains", help="number of chains", type=int)
    parser.add_argument("--iter-sampling", help="number of posterior samples per chain", type=int)
    parser.add_argument("--iter-warmup", help="number of warmup samples per chain", type=int)
    parser.add_argument("--summary", action="store_true", help="display summary")
    parser.add_argument("--output", "-o", help="path to output directory for CSV files", type=Path)

    # First level: the collection.
    collection_subparsers = parser.add_subparsers(required=True)
    for collection, experiments in COLLECTIONS.items():
        collection_subparser = collection_subparsers.add_parser(collection)
        collection_subparser.set_defaults(collection=collection)

        # Second level: the dataset.
        dataset_subparsers = collection_subparser.add_subparsers(required=True)
        for dataset, stan_files in experiments.items():
            dataset_subparser = dataset_subparsers.add_parser(dataset)
            stan_file_by_model = \
                {stan_file.with_suffix("").name: stan_file for stan_file in stan_files}
            dataset_subparser.set_defaults(dataset=dataset, stan_file_by_model=stan_file_by_model)
            dataset_subparser.add_argument("model", choices=stan_file_by_model)

    # Parse the arguments and identify the experiment.
    args: Args = parser.parse_args(argv)

    # Compile the model and draw samples.
    stan_file = args.stan_file_by_model[args.model]
    stanc_options = {"include-paths": [Path(__file__).parent]}
    model = cmdstanpy.CmdStanModel(stan_file=stan_file, stanc_options=stanc_options)
    data = DATA_LOADERS[args.dataset]()
    fit = model.sample(data, chains=args.chains, iter_warmup=args.iter_warmup,
                       iter_sampling=args.iter_sampling)

    # Display summary information for "raw" parameters.
    src_info = model.src_info()
    if args.summary:
        summary = fit.summary()
        fltr = summary.index.map(lambda name: name.split("[")[0] in src_info["parameters"])
        print(summary[fltr])

    # Save CSV files for later use.
    if args.output:
        # Remove the directory if it exists to avoid conflicting samples from different runs.
        if args.output.is_dir():
            shutil.rmtree(args.output)
        fit.save_csvfiles(args.output)
        with open(args.output / "src_info.yaml", "w") as fp:
            yaml.dump(src_info, fp)


if __name__ == "__main__":
    __main__()
