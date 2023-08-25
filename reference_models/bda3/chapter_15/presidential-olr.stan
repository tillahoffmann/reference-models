// Ordinary linear regression for forecasting presidential elections based on page 385--386.

#include data/presidential.stan

parameters {
    real a;
    vector [4] b_national;
    vector [9] b_state;
    vector [6] b_regional;
    real<lower=0> sigma;
}

model {
    Dvote ~ normal(a + X_national * b_national + X_state * b_state + X_regional * b_regional, sigma);
    a ~ normal(0, 100);
    b_national ~ normal(0, 100);
    b_state ~ normal(0, 100);
    b_regional ~ normal(0, 100);
}
