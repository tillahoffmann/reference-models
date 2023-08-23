// Model for ratings of morality with scenario predictors form page 387.
#include data/trolley.stan

parameters {
    ordered [n_responses - 1] cutpoints;
    real bA, bC, bI, bIA, bIC;
}

model {
    vector [n_experiments] phi = bA * action + bC * contact
        + (bI + bIA * action + bIC * contact) .* intention;
    response ~ ordered_logistic(phi, cutpoints);
    cutpoints ~ normal(0, 1.5);
    bA ~ normal(0, 0.5);
    bC ~ normal(0, 0.5);
    bI ~ normal(0, 0.5);
    bIA ~ normal(0, 0.5);
    bIC ~ normal(0, 0.5);
}
