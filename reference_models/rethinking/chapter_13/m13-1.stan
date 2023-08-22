// Varying effects model for tadpole survival from page 402.
#include data/reedfrogs.stan

parameters {
    vector [n_tanks] a;
}

model {
    surv ~ binomial_logit(density, a);
    a ~ normal(0, 1.5);
}
