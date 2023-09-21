/*
Model to predict radon measurements in houses in Minnesota from page 259 of {doc}`arm` with
non-centered parameterization and floor-level predictor.
*/
#include data/radon.stan

parameters {
    vector [n_counties] a_raw;
    real mu;
    real<lower=0> sigma_a, sigma_y;
    real b_x;
}

transformed parameters {
    vector [n_counties] a = sigma_a * a_raw;
}

model {
    y ~ normal(mu + a[county_ind] + b_x * x, sigma_y);
    a_raw ~ normal(0, 1);
}
