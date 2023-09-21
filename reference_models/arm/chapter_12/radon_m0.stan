/*
Model to predict radon measurements in houses in Minnesota from page 259 of {doc}`arm`.
*/
#include data/radon.stan

parameters {
    vector [n_counties] a;
    real mu;
    real<lower=0> sigma_a, sigma_y;
}

model {
    y ~ normal(mu + a[county_ind], sigma_y);
    a ~ normal(0, sigma_a);
}
