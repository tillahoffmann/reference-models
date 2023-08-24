// Two-way ANOVA fron page 495 based on
// http://www.stat.columbia.edu/~gelman/arm/examples/pilots/pilots.1.bug.

#include data/pilots.stan

parameters {
    real mu;
    vector [n_groups] g_raw;
    vector [n_scenarios] d_raw;
    real<lower=0, upper=100> sigma_d, sigma_g, sigma_e;
}

transformed parameters {
    vector [n_groups] g = sigma_g * g_raw;
    vector [n_scenarios] d = sigma_d * d_raw;
    vector [n] y_hat = mu + g[group] + d[scenario];
}

model {
    y ~ normal(y_hat, sigma_e);
    g_raw ~ normal(0, 1);
    d_raw ~ normal(0, 1);
}
