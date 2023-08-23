from typing import Callable, Dict

from . import chimpanzees, reedfrogs, trolley

DATA_LOADERS: Dict[str, Callable[..., Dict]] = {
    "chimpanzees": chimpanzees.load_data,
    "reedfrogs": reedfrogs.load_data,
    "trolley": trolley.load_data,
}
