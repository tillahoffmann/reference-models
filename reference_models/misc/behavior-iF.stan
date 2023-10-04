/*
Model for behavioral data with individual-level random effects and fixed effects.
*/

#include data/behavior.stan

parameters {
    array [K - 1] real a;                // intercepts for each behavior
    array [K - 1] real bA;				// fixed effect for age
    array [K - 1] real bQ;				// fixed effect for age squared
    array [K - 1] real bW;				// fixed effect for wealth
    array [K - 1] real bN;				// fixed effect for Sunday
    array [K - 1] real bR;				// fixed effect for Saturday
    array [K - 1] real bT;				// fixed effect for time of day
    array [K - 1] real bTQ;				// fixed effect for time of day squared
    array [K - 1] real bH;				// fixed effect for house size
    array [K - 1] real bL;				// fixed effect for rain
    matrix [K - 1, N_id] z_id;      // matrix of standardized random effects
    vector<lower=0> [K - 1] sigma_id;   // stddev of random effects
    cholesky_factor_corr [K - 1] L_Rho_id;         // correlation matrix of random effects
}

transformed parameters {
    // matrix of scaled random effects
    matrix[N_id, K - 1] v_id = (diag_pre_multiply(sigma_id,L_Rho_id) * z_id)';
}

model {
    // priors
    a ~ normal(0, 1);
    bA ~ normal(0, 1);
    bQ ~ normal(0, 1);
    bW ~ normal(0, 1);
    bN ~ normal(0, 1);
    bR ~ normal(0, 1);
    bT ~ normal(0, 1);
    bTQ ~ normal(0, 1);
    bH ~ normal(0, 1);
    bL ~ normal(0, 1);

    // hyper-prior
    to_vector(z_id) ~ normal(0, 1);
    sigma_id ~ exponential(1);
    L_Rho_id ~ lkj_corr_cholesky(2);

    // likelihood
    for (i in 1:N) {
        vector[K] p;
        for (k in 1:(K - 1)) {
            p[k] = a[k] + bA[k] * age_z[i] + bQ[k] * age_zq[i] + bW[k] * wz[i] + bN[k] * sunday[i]
                + bR[k] * saturday[i] + bT[k] * time_z[i] + bTQ[k] * time_zq[i]
                + bH[k] * house_size_z[i] + bL[k] * rain_z[i] + v_id[id[i],k];
        }
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
        for (k in 1:(K - 1)) {
            p[k] = a[k] + bA[k] * age_z[i] + bQ[k] * age_zq[i] + bW[k] * wz[i] + bN[k] * sunday[i]
                + bR[k] * saturday[i] + bT[k] * time_z[i] + bTQ[k] * time_zq[i]
                + bH[k] * house_size_z[i] + bL[k] * rain_z[i] + v_id[id[i], k];
        }
        p[K] = 0;
        log_lik[i] = categorical_logit_lpmf(y[i] | p);
    }
}
