/*Centered model for eight schools based on section 15.5.*/
#include data/schools.stan

parameters {
    vector [n] theta;
    real mu;
    real<lower=0> tau;
}

model {
    y ~ normal(theta, sigma);
    theta ~ normal(mu, tau);
}
