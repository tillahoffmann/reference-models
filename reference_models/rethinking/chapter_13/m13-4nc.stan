/*Non-centered parameterization of model for prosocial behavior of chimpanzees with actor and block
effects from page 424.*/
#include data/chimpanzees.stan

parameters {
    real a_bar;
    vector [n_actors] a_raw;  // z in the book.
    vector [4] b;
    vector [n_blocks] g_raw;  // x in the book.
    real<lower=0> sigma_a, sigma_g;
}

transformed parameters {
    vector [n_actors] a = a_bar + sigma_a * a_raw;
    vector [n_blocks] g = sigma_g * g_raw;
    vector [n_experiments] logits = a[actor] + b[treatment] + g[block];
}

model {
    pulled_left ~ bernoulli_logit(logits);
    a_bar ~ normal(0, 1.5);
    a_raw ~ normal(0, 1);
    b ~ normal(0, 0.5);
    g_raw ~ normal(0, 1);
    sigma_a ~ exponential(1);
    sigma_g ~ exponential(1);
}
