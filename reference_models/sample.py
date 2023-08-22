import argparse
import cmdstanpy

from . import COLLECTIONS


class Args:
    collection: str
    dataset: str
    model: str


def __main__(argv: dict | None = None) -> None:
    # Construct hierarchical parsers.
    parser = argparse.ArgumentParser()

    # First level: the collection.
    collection_subparsers = parser.add_subparsers()
    for collection, experiments in COLLECTIONS.items():
        collection_subparser = collection_subparsers.add_parser(collection)
        collection_subparser.set_defaults(collection=collection)

        # Second level: the dataset.
        dataset_subparsers = collection_subparser.add_subparsers()
        for dataset, spec in experiments.items():
            dataset_subparser = dataset_subparsers.add_parser(dataset)
            dataset_subparser.set_defaults(dataset=dataset, spec=spec)
            dataset_subparser.add_argument("model", choices=spec["stan_files"])

    # Parse the arguments and identify the experiment.
    args: Args = parser.parse_args(argv)

    # Compile the model and draw samples.
    stan_file = args.spec["stan_files"][args.model]
    model = cmdstanpy.CmdStanModel(stan_file=stan_file)
    data = args.spec["load_data"]()
    fit = model.sample(data)
    print(fit.diagnose())


if __name__ == "__main__":
    __main__()
