// Non-centered model for eight schools based on section 15.5.
#include data/schools.stan

parameters {
    vector [n] z;
    real mu;
    real<lower=0> tau;
}

transformed parameters {
    vector [n] theta = mu + tau * z;
}

model {
    y ~ normal(theta, sigma);
    z ~ normal(0, 1);
}
