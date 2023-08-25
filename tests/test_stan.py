import cmdstanpy
import numpy as np
from pathlib import Path
from reference_models.util import get_stanc_options


ROOT = Path(__file__).parent / "stan_files"


def test_indexing() -> None:
    n_rows = 5
    n_cols = 9
    n_idx = 3

    X = (1 + np.arange(n_rows * n_cols)).reshape((n_rows, n_cols))

    i = np.random.choice(n_rows, size=n_idx, replace=False)
    j = np.random.choice(n_cols, size=n_idx, replace=False)

    data = {
        "n_rows": n_rows,
        "n_cols": n_cols,
        "n_idx": n_idx,
        "X": X,
        "i": i + 1,
        "j": j + 1,
    }

    model = cmdstanpy.CmdStanModel(stan_file=ROOT / "test_compress_index.stan",
                                   stanc_options=get_stanc_options())
    fit = model.sample(data, fixed_param=True, iter_sampling=1)
    np.testing.assert_allclose(fit.Xij[0], X[i, j])
