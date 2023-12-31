import jsonschema
import numpy as np
from pathlib import Path
import pandas as pd
import pytest
import yaml
from reference_models.data import util


ROOT = Path("reference_models/data")
DATASETS = ROOT.glob("*.csv")

EXPECTED_STATES_BY_REGION = {
    "west": {"WA", "OR", "CA", "NV", "AZ", "NM", "CO", "UT", "ID", "WY", "MT", "HI", "AK"},
    "midwest": {"ND", "SD", "NE", "KS", "MO", "IA", "MN", "WI", "IL", "IN", "MI", "OH"},
    "south": {"TX", "OK", "AR", "LA", "MS", "AL", "TN", "KY", "GA", "FL", "SC", "NC", "VA"},
    "northeast": {"PA", "NY", "CT", "RI", "NH", "VT", "MA", "ME", "NJ", "MD", "DE", "WV"},
    "dc": {"DC"},
}


@pytest.mark.parametrize("dataset_path", DATASETS, ids=lambda path: path.name)
def test_dataset(dataset_path: Path) -> None:
    # Load the corresponding schema.
    schema_path = dataset_path.with_suffix(".schema.yaml")
    with schema_path.open() as fp:
        schema: dict = yaml.safe_load(fp)

    # Ensure the schema has license information.
    assert schema.get("license")

    # Load and validate the data. We replace `nan` with `None` for json schema validation.
    dataset = pd.read_csv(dataset_path).replace(float("nan"), None)
    jsonschema.validate(dataset.to_dict(orient="records"), schema)


def test_presidential_state_region_assignment() -> None:
    with (ROOT / "presidential.schema.yaml").open() as fp:
        schema = yaml.safe_load(fp)

    # Assign states to regions based on the expected assignment from the US Census Bureau
    # (https://en.wikipedia.org/wiki/List_of_regions_of_the_United_States) to ensure the indices are
    # right. The following states in the South have been moved to the North East: MD, DE, WV.
    actual = {
        region: {schema["metadata"]["states"][index - 1] for index in indices}
        for region, indices in schema["metadata"]["regions"].items()
    }
    assert actual == {key: value for key, value in EXPECTED_STATES_BY_REGION.items() if key != "dc"}


def test_presidential_national_variables() -> None:
    presidential = pd.read_csv(ROOT / "presidential.csv")
    # Incumbent indicator (+1 for Democrat, -1 for Republican).
    inc = np.sign(presidential.groupby("year").n2.first())
    np.testing.assert_array_equal(inc, [
        1,  # 1948; Truman vs Warren -> Truman.
        1,  # 1952; Eisenhower vs Stevenson -> Eisenhower.
        -1,  # 1956; Eisenhower vs Stevenson -> Eisenhower.
        -1,  # 1960; JFK vs Nixon -> JFK; then Johnson after JFK assassination.
        1,  # 1964; Johnson vs Goldwater -> Johnson.
        1,  # 1968; Nixon vs Humphrey -> Nixon.
        -1,  # 1972; Nixon vs McGovern -> Nixon then Ford after Nixon resignation.
        -1,  # 1976; Ford vs Carter -> Crater.
        1,  # 1980; Carter vs Reagan -> Reagan.
        -1,  # 1984; Reagan vs Mondale -> Reagan.
        -1,  # 1988; Bush vs Dukakis -> Bush.
        -1,  # 1992; Bush vs Clinton -> Clinton.
    ])
    # "presinc" indicator equal to the incumbent indicator if the incubment is running for
    # re-election.
    presinc = np.sign(presidential.groupby("year").n3.first())
    np.testing.assert_array_equal(presinc, [
        1,
        0,
        -1,
        0,
        1,
        0,
        -1,
        0,
        1,
        -1,
        0,
        -1,
    ])


def test_election88_state_region_assignment() -> None:
    with (ROOT / "election88.schema.yaml").open() as fp:
        schema = yaml.safe_load(fp)

    actual = {
        region: {schema["metadata"]["states"][index - 1] for index in indices}
        for region, indices in schema["metadata"]["regions"].items()
    }
    assert actual == EXPECTED_STATES_BY_REGION


def test_get_consecutive_labels() -> None:
    # Test that labels get sorted before encoding to consecutive labels.
    base = 7 + np.arange(10)
    labels = np.random.permutation(np.repeat(base, 10))
    consecutive, encoder = util.get_consecutive_labels(labels, return_encoder=True)
    np.testing.assert_array_equal(encoder.classes_, base)
    np.testing.assert_array_equal(consecutive, labels - 6)

    # Test that labels do not get sorted if preserve_order is set.
    labels = list("bbazzb")
    consecutive = util.get_consecutive_labels(labels, preserve_order=True)
    np.testing.assert_array_equal(consecutive, [1, 1, 2, 3, 3, 1])
    consecutive = util.get_consecutive_labels(labels, preserve_order=False)
    np.testing.assert_array_equal(consecutive, [2, 2, 1, 3, 3, 2])


def test_group_by() -> None:
    items = list(enumerate("eabaccde"))
    expected = {
        "e": [0, 7],
        "a": [1, 3],
        "b": [2],
        "c": [4, 5],
        "d": [6],
    }
    assert util.group_by(items, 1, 0) == expected
    assert util.group_by(items, lambda x: x[1], lambda x: x[0]) == expected


def test_pres_vote_historical() -> None:
    pres_vote_historical = pd.read_csv(ROOT / "pres_vote_historical.csv")
    np.testing.assert_array_less(pres_vote_historical.dem + pres_vote_historical.rep,
                                 pres_vote_historical.total + 1e-6)
