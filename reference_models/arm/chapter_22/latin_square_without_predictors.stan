/*
Non-centered variant of the ANOVA model for latin square experiment from equation 22.6 on page 497
of {doc}`arm`. This is a simplified version of {ref}`arm-chapter_13-latin_square_with_predictors`,
not including linear predictors for rows, columns, or treatments.
*/

#include data/latin_square.stan

parameters {
    real mu;
    vector [5] b_row_raw, b_col_raw, b_treatment_raw;
    real<lower=0> sigma_row, sigma_col, sigma_treatment, sigma_yield;
}

transformed parameters {
    vector [5] b_row = sigma_row * b_row_raw;
    vector [5] b_col = sigma_col * b_col_raw;
    vector [5] b_treatment = sigma_treatment * b_treatment_raw;
}

model {
    yield ~ normal(mu + b_row[row_idx] + b_col[col_idx] + b_treatment[treatment], sigma_yield);

    b_row_raw ~ normal(0, 1);
    b_col_raw ~ normal(0, 1);
    b_treatment_raw ~ normal(0, 1);

    sigma_row ~ cauchy(0, 25);
    sigma_col ~ cauchy(0, 25);
    sigma_treatment ~ cauchy(0, 25);
    sigma_yield ~ cauchy(0, 25);
}
