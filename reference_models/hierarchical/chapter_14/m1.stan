// Model for CBS poll results with state-level effects from page 302 of "Data Analysis Using
// Regression and Multilevel/Hierarchical Models".
#include data/election88.stan

parameters {
    vector [n_states] a;
    real mu_a, b_female, b_black;
    real<lower=0> sigma_a;

}

transformed parameters {
    vector [n_responses] logits = a[state] + b_female * female + b_black * black;
}

model {
    y ~ bernoulli_logit(logits);
    a ~ normal(mu_a, sigma_a);
}
