// Hierarchical linear regression for forecasting presidential elections based on page 387.

#include data/presidential.stan

transformed data {
    // Obtain cross-classified region-year indicators. We ensure the first n_year elements
    // correspond to the South because the model uses a different hierarchical variance parameter.
    int n_region_year = n_regions * n_years;
    array [n] int<lower=1, upper=n_region_year> region_year;
    for (i in 1:n) {
        region_year[i] = n_years * (region[i] - 1) + year[i];
    }
}

parameters {
    real a;
    vector [4] b_national;
    vector [9] b_state;
    real<lower=0> sigma;

    vector [n_years] d_raw;
    vector [n_region_year] g;
    real<lower=0> sigma_d, sigma_g_south, sigma_g_other;
}

transformed parameters {
    vector [n_years] d = sigma_d * d_raw;
    vector [n] predictor = a + X_national * b_national + X_state * b_state + d[year]
        + g[region_year];
}

model {
    Dvote ~ normal(predictor, sigma);
    a ~ normal(0, 100);
    b_national ~ normal(0, 100);
    b_state ~ normal(0, 100);

    d_raw ~ normal(0, 1);
    // We don't need the zeros_vector here, and could just use the literal "0". But using the vector
    // implicitly checks we haven't messed up the sizes of arrays.
    g[:n_years] ~ normal(zeros_vector(n_years), sigma_g_south);
    g[n_years + 1:] ~ normal(zeros_vector(n_years * (n_regions - 1)), sigma_g_other);
}
