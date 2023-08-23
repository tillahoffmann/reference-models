// Marginal model for ratings of morality form page 385.
#include data/trolley.stan

parameters {
    ordered [n_responses - 1] cutpoints;
}

model {
    response ~ ordered_logistic(zeros_vector(n_experiments), cutpoints);
    cutpoints ~ normal(0, 1.5);
}
