/*
Hierarchical linear regression for forecasting presidential elections based on page 387.
Year-effects have been non-centered.
*/

functions {
    #include util.stan
}

#include data/presidential.stan

transformed data {
    // Obtain cross-classified region-year indicators.
    array [n] int<lower=1, upper=n_years * n_regions> year_region = compress_index(year, region, n_years);
}

parameters {
    real a;
    vector [4] b_national;
    vector [9] b_state;
    real<lower=0> sigma;

    vector [n_years] d_raw;
    matrix [n_years, n_regions] g;
    real<lower=0> sigma_d, sigma_g_south, sigma_g_other;
}

transformed parameters {
    vector [n_years] d = sigma_d * d_raw;
    vector [n] predictor = a + X_national * b_national + X_state * b_state + d[year]
        + to_vector(g)[year_region];
}

model {
    Dvote ~ normal(predictor, sigma);
    a ~ normal(0, 100);
    b_national ~ normal(0, 100);
    b_state ~ normal(0, 100);

    d_raw ~ normal(0, 1);
    g[:, 1] ~ normal(0, sigma_g_south);
    to_vector(g[:, 2:]) ~ normal(0, sigma_g_other);
}
