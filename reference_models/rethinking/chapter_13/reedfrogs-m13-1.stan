// Varying effects model for tadpole survival from page 402.
data {
    int n_tanks;
    array [n_tanks] int density, surv;
}

parameters {
    vector [n_tanks] a;
}

model {
    surv ~ binomial_logit(density, a);
    a ~ normal(0, 1.5);
}
