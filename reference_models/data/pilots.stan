data {
    int n, n_groups, n_scenarios;
    array [n] int<lower=1, upper=n_groups> group;
    array [n] int<lower=1, upper=n_scenarios> scenario;
    vector<lower=0, upper=1> [n] y;
}
