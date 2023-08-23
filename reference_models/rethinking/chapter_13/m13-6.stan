// Model for prosocial behavior of chimpanzees with actor and block effects and shrinkage prior on
// treatment coefficients from page 419.
#include data/chimpanzees.stan

parameters {
    real a_bar;
    vector [n_actors] a;
    vector [4] b;
    vector [n_blocks] g;
    real<lower=0> sigma_a, sigma_b, sigma_g;
}

transformed parameters {
    vector [n_experiments] logits = a[actor] + b[treatment] + g[block];
}

model {
    pulled_left ~ bernoulli_logit(logits);
    a_bar ~ normal(0, 1.5);
    a ~ normal(a_bar, sigma_a);
    b ~ normal(0, sigma_b);
    g ~ normal(0, sigma_g);
    sigma_a ~ exponential(1);
    sigma_b ~ exponential(1);
    sigma_g ~ exponential(1);
}
