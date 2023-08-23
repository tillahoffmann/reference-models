data {
    int n_experiments;
    int n_responses;
    array [n_experiments] int<lower=1, upper=n_responses> response;
    // Scenarios are encoded as vectors rather than arrays of integers to provide more concise
    // notation, e.g., using vector notation.
    vector<lower=0, upper=1> [n_experiments] action, contact, intention;
}
