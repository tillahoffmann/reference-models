// Two-way ANOVA fron page 495 based on
// http://www.stat.columbia.edu/~gelman/arm/examples/pilots/pilots.1.bug.

#include data/pilots.stan

parameters {
    real mu;
    vector [n_groups] g;
    vector [n_scenarios] d;
    real<lower=0, upper=100> sigma_d, sigma_g, sigma_e;
}

transformed parameters {
    vector [n] y_hat = mu + g[group] + d[scenario];
}

model {
    y ~ normal(y_hat, sigma_e);
    g ~ normal(0, sigma_g);
    d ~ normal(0, sigma_d);
}
