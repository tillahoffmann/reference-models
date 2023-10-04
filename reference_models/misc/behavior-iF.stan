/*
Model for behavioral data with individual-level random effects and fixed effects.
*/

#include data/behavior.stan

parameters {
    vector [K - 1] a;                // intercepts for each behavior
    matrix [9, K - 1] b;  // fixed effects
    matrix [K - 1, N_id] z_id;      // matrix of standardized random effects
    vector<lower=0> [K - 1] sigma_id;   // stddev of random effects
    cholesky_factor_corr [K - 1] L_Rho_id;         // correlation matrix of random effects
}

transformed parameters {
    // matrix of scaled random effects
    matrix[N_id, K - 1] v_id = (diag_pre_multiply(sigma_id, L_Rho_id) * z_id)';
}

model {
    // priors
    a ~ normal(0, 1);
    to_vector(b) ~ normal(0, 1);

    // hyper-prior
    to_vector(z_id) ~ normal(0, 1);
    sigma_id ~ exponential(1);
    L_Rho_id ~ lkj_corr_cholesky(2);

    // likelihood
    for (i in 1:N) {
        vector[K] p;
        p[:K - 1] = a + v_id[id[i]]' + (X[i] * b)';
        p[K] = 0;
        y[i] ~ categorical_logit(p);
    }
}

generated quantities {
    matrix[K - 1,K - 1] Rho_id;
    vector[N] log_lik;
    Rho_id = L_Rho_id * L_Rho_id';

    for (i in 1:N) {
        vector[K] p;
        p[:K - 1] = a + v_id[id[i]]' + (X[i] * b)';
        p[K] = 0;
        log_lik[i] = categorical_logit_lpmf(y[i] | p);
    }
}
