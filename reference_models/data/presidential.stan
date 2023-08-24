data {
    int n, n_states, n_years;
    matrix [n, 4] X_national;
    matrix [n, 9] X_state;
    matrix [n, 6] X_regional;
    array [n] int<lower=1, upper=n_states> state;
    array [n] int<lower=1, upper=n_years> year;
    vector<lower=0, upper=1> [n] Dvote;
}
