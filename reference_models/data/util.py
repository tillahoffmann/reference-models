import numpy as np
from sklearn.preprocessing import LabelEncoder
from typing import Tuple


def check_consecutive_labels(labels: np.ndarray, start: int = 1, end: int | None = None) \
        -> np.ndarray:
    """
    Check that labels are consecutive.

    Args:
        labels: Labels to check.
        start: Expected value of the first label.
        end: Expected value of the last label.

    Returns:
        Checked labels.
    """
    labels = np.asarray(labels)
    unique_labels = np.unique(labels)
    if end is None:
        end = unique_labels.max()
    expected_labels = np.arange(start, end + 1)
    np.testing.assert_array_equal(unique_labels, expected_labels)
    return labels


def get_consecutive_labels(labels: np.ndarray, start: int = 1, return_encoder: bool = False) \
        -> np.ndarray | Tuple[np.ndarray, LabelEncoder]:
    encoder = LabelEncoder()
    labels = encoder.fit_transform(labels) + start
    return (labels, encoder) if return_encoder else labels
