data {
    int n_actors, n_experiments, n_blocks;
    array [n_experiments] int<lower=1, upper=n_actors> actor;
    array [n_experiments] int<lower=1, upper=n_blocks> block;
    array [n_experiments] int<lower=0, upper=1> pulled_left;
    array [n_experiments] int<lower=1, upper=4> treatment;
}
