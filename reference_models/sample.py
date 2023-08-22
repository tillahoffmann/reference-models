import argparse
import cmdstanpy
import pandas as pd
from pathlib import Path


class Args:
    collection: str
    dataset: str
    model: str


def discover_experiments() -> pd.DataFrame:
    root = Path(__file__).parent
    experiments = []
    for stan_file in root.glob("**/*.stan"):
        collection, *_, dataset_model = stan_file.with_suffix("").relative_to(root).parts
        dataset, model = dataset_model.split("-", 1)
        experiments.append({
            "collection": collection,
            "dataset": dataset,
            "model": model,
            "stan_file": stan_file,
        })
    return pd.DataFrame(experiments)


def load_data(collection: str, dataset: str) -> dict:
    # Import the module to load the data (the [None] argument ensures we get the target module).
    module = __import__(f"reference_models.{collection}.data.{dataset}", fromlist=[None])
    return module.load_data()


def __main__(argv: dict | None = None) -> None:
    # Construct hierarchical parsers.
    parser = argparse.ArgumentParser()
    experiments = discover_experiments()

    # First level: the collection.
    collection_subparsers = parser.add_subparsers()
    for collection, collection_subset in experiments.groupby("collection"):
        collection_subparser = collection_subparsers.add_parser(collection)
        collection_subparser.set_defaults(collection=collection)

        # Second level: the dataset.
        dataset_subparsers = collection_subparser.add_subparsers()
        for dataset, dataset_subset in collection_subset.groupby("dataset"):
            dataset_subparser = dataset_subparsers.add_parser(dataset)
            dataset_subparser.set_defaults(dataset=dataset)
            dataset_subparser.add_argument("model", choices=list(dataset_subset.model))

    # Parse the arguments and identify the experiment.
    args: Args = parser.parse_args(argv)
    key = (args.collection, args.dataset, args.model)
    experiment = experiments.set_index(["collection", "dataset", "model"]).loc[key]

    # Compile the model and draw samples.
    model = cmdstanpy.CmdStanModel(stan_file=experiment.stan_file)
    data = load_data(args.collection, args.dataset)
    fit = model.sample(data)
    print(fit.diagnose())


if __name__ == "__main__":
    __main__()
