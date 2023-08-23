// Model for prosocial behavior of chimpanzees with actor but no block effects from page 417.
#include data/chimpanzees.stan

parameters {
    real a_bar;
    vector [n_actors] a;
    vector [4] b;
    real<lower=0> sigma_a;
}

transformed parameters {
    vector [n_experiments] logits = a[actor] + b[treatment];
}

model {
    pulled_left ~ bernoulli_logit(logits);
    a_bar ~ normal(0, 1.5);
    a ~ normal(a_bar, sigma_a);
    b ~ normal(0, 0.5);
    sigma_a ~ exponential(1);
}
