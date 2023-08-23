from typing import Callable, Dict

from . import chimpanzees, reedfrogs

DATA_LOADERS: Dict[str, Callable[..., Dict]] = {
    "chimpanzees": chimpanzees.load_data,
    "reedfrogs": reedfrogs.load_data,
}
