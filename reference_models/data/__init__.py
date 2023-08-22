from typing import Callable, Dict

from . import reedfrogs

DATA_LOADERS: Dict[str, Callable[..., Dict]] = {
    "reedfrogs": reedfrogs.load_data,
}
