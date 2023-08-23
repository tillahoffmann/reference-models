data {
    int n_experiments;
    int n_responses;
    array [n_experiments] int<lower=1, upper=n_responses> response;
}
