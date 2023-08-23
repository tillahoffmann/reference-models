#include data/chimpanzees.stan

parameters {
    real a_bar;
    vector [n_actors] a;
    vector [4] b;
    vector [n_blocks] g;
    real<lower=0> sigma_a, sigma_g;
}

transformed parameters {
    vector [n_experiments] logits = a[actor] + b[treatment] + g[block];
}

model {
    pulled_left ~ bernoulli_logit(logits);
    a ~ normal(a_bar, sigma_a);
    b ~ normal(0, 0.5);
    g ~ normal(0, sigma_g);
    sigma_a ~ exponential(1);
    sigma_g ~ exponential(1);
}
