/*Model for prosocial behavior of chimpanzees with actor effects from page 330.*/
#include data/chimpanzees.stan

parameters {
    vector [n_actors] a;
    vector [4] b;
    vector [n_blocks] g;
}

transformed parameters {
    vector [n_experiments] logits = a[actor] + b[treatment];
}

model {
    pulled_left ~ bernoulli_logit(logits);
    a ~ normal(0, 1.5);
    b ~ normal(0, 0.5);
}
