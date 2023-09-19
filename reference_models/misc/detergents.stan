/*
Multinomial regression model for detergent purchases based on
[Burgette et al. (2021)](https://doi.org/10.1214/20-ba1233), although they consider multinomial
probit regression.
*/
#include data/detergents.stan

parameters {
    vector [n_choices] a;
    real<lower=0> sigma;
    real b;
}

model {
    a ~ normal(0, sigma);
    b ~ normal(0, 100);
    for (i in 1:n) {
        y ~ categorical_logit(a + b * X[i]');
    }
}
