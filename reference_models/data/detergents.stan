data {
    int n, n_choices;
    array [n] int<lower=1, upper=n_choices> y;
    matrix [n, n_choices] X;
}
