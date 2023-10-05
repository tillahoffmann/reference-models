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

generated quantities {
    vector [n_experiments] log_lik;
    for (i in 1:n_experiments) {
        log_lik[i] = bernoulli_logit_lpmf(pulled_left[i] | logits[i]);
    }
}
