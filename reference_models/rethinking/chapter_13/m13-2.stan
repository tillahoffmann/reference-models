// Varying effects model for tadpole survival with shrinkage prior from page 403.
data {
    int n_tanks;
    array [n_tanks] int density, surv;
}

parameters {
    vector [n_tanks] a;
    real a_bar;
    real<lower=0> sigma_a;
}

model {
    surv ~ binomial_logit(density, a);
    a ~ normal(a_bar, sigma_a);
    a_bar ~ normal(0, 1.5);
    sigma_a ~ exponential(1);
}
