from typing import Callable, Dict

from . import chimpanzees, election88, reedfrogs, trolley

DATA_LOADERS: Dict[str, Callable[..., Dict]] = {
    "chimpanzees": chimpanzees.load_data,
    "election88": election88.load_data,
    "reedfrogs": reedfrogs.load_data,
    "trolley": trolley.load_data,
}
