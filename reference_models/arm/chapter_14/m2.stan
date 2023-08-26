/*
Model for CBS poll results with non-nested hierarchical effects from page 381 of "Data Analysis
Using Regression and Multilevel/Hierarchical Models". The BUGS code is available at
http://www.stat.columbia.edu/~gelman/arm/examples/election88/election88.M2.bug.
*/

functions {
    #include util.stan
}

#include data/election88.stan

transformed data {
    // Convert covariates to design matrix.
    int n_features = 4;
    matrix [n_responses, n_features] X;
    X[:, 1] = ones_vector(n_responses);
    X[:, 2] = female;
    X[:, 3] = black;
    X[:, 4] = female .* black;

    array [n_responses] int<lower=1, upper=n_edus * n_ages> edu_age = compress_index(edu, age, n_edus);
}

parameters {
    vector [n_features] b;
    real b_v_prev;
    vector [n_ages] a_age;
    vector [n_edus] a_edu;
    matrix [n_edus, n_ages] a_edu_age;
    vector [n_regions] a_region;
    vector [n_states] a_state;
    real<lower=0, upper=100> sigma_state, sigma_age, sigma_edu, sigma_edu_age, sigma_region;

}

transformed parameters {
    vector [n_responses] logits = X * b + a_age[age] + a_edu[edu]
        + to_vector(a_edu_age)[edu_age] + a_state[state];
}

model {
    // The code in section 17.4 looks different, but `dnorm` in BUGS uses the precision rather than
    // standard deviation as a parameter
    // (https://www.multibugs.org/documentation/latest/Distributions.html#Normal).
    y ~ bernoulli_logit(logits);
    a_state ~ normal(a_region[region] + b_v_prev * v_prev[region], sigma_state);
    a_age ~ normal(0, sigma_age);
    a_edu ~ normal(0, sigma_edu);
    to_vector(a_edu_age) ~ normal(0, sigma_edu_age);
    a_region ~ normal(0, sigma_region);

    b ~ normal(0, 100);
    b_v_prev ~ normal(0, 100);
    // Implicit uniform prior on (0, 100) for sigma_*.
}
