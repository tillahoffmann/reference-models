/*
Model for CBS poll results with non-nested hierarchical effects from based on page 381 of "Data
Analysis Using Regression and Multilevel/Hierarchical Models". The original BUGS code is
available at http://www.stat.columbia.edu/~gelman/arm/examples/election88/election88.M2.bug.
The model has been modified as follows:
- a_age, a_edu, and a_region are non-centered.
- The hierarchical prior on a_state given regional parameters has been moved to the `logits`.
- Features black, female, black-female interaction, and v_prev_full have been de-meaned.
*/
functions {
    #include util.stan
}

#include data/election88.stan

transformed data {
    // Convert covariates to design matrix.
    int n_features = 5;
    matrix [n_responses, n_features] X;
    X[:, 1] = ones_vector(n_responses);
    X[:, 2] = female - mean(female);
    X[:, 3] = black - mean(black);
    X[:, 4] = X[:, 2] .* X[:, 3];
    X[:, 5] = v_prev_full - mean(v_prev_full);

    array [n_responses] int<lower=1, upper=n_edus * n_ages> edu_age = compress_index(edu, age, n_edus);
}

parameters {
    vector [n_features] b;
    vector [n_ages] a_age_raw;
    vector [n_edus] a_edu_raw;
    matrix [n_edus, n_ages] a_edu_age;
    vector [n_regions] a_region_raw;
    vector [n_states] a_state;
    real<lower=0, upper=100> sigma_state, sigma_age, sigma_edu, sigma_edu_age, sigma_region;

}

transformed parameters {
    vector [n_ages] a_age = sigma_age * a_age_raw;
    vector [n_edus] a_edu = sigma_edu * a_edu_raw;
    vector [n_regions] a_region = sigma_region * a_region_raw;
    vector [n_responses] logits = X * b + a_age[age] + a_edu[edu]
        + to_vector(a_edu_age)[edu_age] + a_state[state] + a_region[region_full];
}

model {
    y ~ bernoulli_logit(logits);
    a_state ~ normal(0, sigma_state);
    a_age_raw ~ normal(0, 1);
    a_edu_raw ~ normal(0, 1);
    to_vector(a_edu_age) ~ normal(0, sigma_edu_age);
    a_region_raw ~ normal(0, 1);

    b ~ normal(0, 100);
    // Implicit uniform prior on (0, 100) for sigma_*.
}
