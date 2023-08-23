import argparse
import cmdstanpy
from pathlib import Path
from typing import Dict

from . import COLLECTIONS
from .data import DATA_LOADERS


class Args:
    chains: int | None
    collection: str
    dataset: str
    iter_sampling: int | None
    iter_warmup: int | None
    model: str
    stan_file_by_model: Dict[str, Path]


def __main__(argv: dict | None = None) -> None:
    # Construct hierarchical parsers.
    parser = argparse.ArgumentParser()
    parser.add_argument("--chains", help="number of chains", type=int)
    parser.add_argument("--iter-sampling", help="number of posterior samples per chain", type=int)
    parser.add_argument("--iter-warmup", help="number of warmup samples per chain", type=int)

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
    print(fit.diagnose())


if __name__ == "__main__":
    __main__()
