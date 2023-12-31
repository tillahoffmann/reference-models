import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from typing import Callable, Container, Dict, Hashable, Iterable, Optional, Tuple, Type, TypeVar, \
    Union


T = TypeVar("T")


class OrderedLabelEncoder(LabelEncoder):
    """
    Label encoder for consecutive integers preserving the order of first occurrence.
    """
    def fit(self, y: np.ndarray) -> "OrderedLabelEncoder":
        classes = []
        for x in y:
            if x not in classes:
                classes.append(x)
        self.classes_ = np.asarray(classes)
        return self

    def transform(self, y: np.ndarray) -> np.ndarray:
        lookup = pd.Series(np.arange(self.classes_.size), self.classes_)
        return lookup[y]


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
    unique_labels = np.unique(labels)
    if end is None:
        end = unique_labels.max()
    expected_labels = np.arange(start, end + 1)
    np.testing.assert_array_equal(unique_labels, expected_labels)
    return labels


def get_consecutive_labels(labels: np.ndarray, start: int = 1, return_encoder: bool = False,
                           preserve_order: bool = False) \
        -> np.ndarray | Tuple[np.ndarray, LabelEncoder]:
    """
    Convert categorical features to consecutive integer labels.

    Args:
        labels: Labels to convert.
        start: First integer label.
        return_encoder: Return the fitted encoder, e.g., for converting back to the original labels.
        preserve_order: Preserve the order of labels such that the integers labels represent the
            first appearance of a label.

    Returns:
        Consecutive integer labels if :code:`return_encoder is False` else a tuple of consecutive
        integer labels and a :class:`~sklearn.preprocessing.LabelEncoder` instance.
    """
    encoder = OrderedLabelEncoder() if preserve_order else LabelEncoder()
    encoder.fit(labels)
    labels = encoder.transform(labels) + start
    return (labels, encoder) if return_encoder else labels


def group_by(items: Iterable[T], key: Union[Hashable, Callable[[T], Hashable]],
             value: Optional[Union[Hashable, Callable[[T], Hashable]]] = None,
             container_type: Type[Container] = list) -> Dict[Hashable, Container[T]]:
    """
    Group a sequence of values.

    Args:
        values: Values to group.
        key: Key to extract for grouping items. If :code:`key` is callable, it is applied to each
            value. Otherwise, each value is indexed by :code:`key`.
        value: Value to extract from each item.
        container_type: Container type for each group, e.g., :class:`set` for unique values.

    Returns:
        Mapping of keys to list of values.
    """
    groups = {}
    for item in items:
        key_ = key(item) if callable(key) else item[key]
        value_ = item
        if value is not None:
            value_ = value(item) if callable(value) else item[value]
        groups.setdefault(key_, []).append(value_)
    return {key: container_type(value) for key, value in groups.items()}
