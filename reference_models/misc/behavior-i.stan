/*
Model for behavioral data with individual-level random effects only.
*/

#include data/behavior.stan

parameters {
    vector [K - 1] a; 						// intercepts for each behavior, minus reference category
    matrix [K - 1, N_id] z_id;      		// matrix of standardized random effects
    vector<lower=0> [K - 1] sigma_id;   	// stddev of random effects
    cholesky_factor_corr [K - 1] L_Rho_id; // correlation matrix of random effects, Choleskey decomposition
}

transformed parameters {
    // matrix of scaled random effects; note transpose in this transformation
    matrix[N_id, K - 1] v_id = (diag_pre_multiply(sigma_id, L_Rho_id) * z_id)';
}

model {
    // priors for fixed effects, mean followed by standard deviation
    a ~ normal(0, 1);

	// hyper-priors
    to_vector(z_id) ~ normal(0, 1);
    sigma_id ~ exponential(1);
    L_Rho_id ~ lkj_corr_cholesky(2);

    // Likelihood function
    // This code sets up a function for each of the K - 1 responses.
    // For each function (k), an intercept (a) is paramaterized along with
    // a subject-level varying intercept (v_id). We use STAN's built-in categorical_logit
    // function for multinomial logistic regression.

    for (i in 1:N) {
        vector [K] p;
        /*
        // Vectorizing as follows leads to worse performance.
        p[:K - 1] = a + v_id[id[i]]';
        p[K] = 0;
        */
        for (k in 1:(K - 1)) {
            p[k] = a[k] + v_id[id[i], k];
        }
        p[K] = 0;
        y[i] ~ categorical_logit(p);
    }
}

// In this block, we generate the variance-covariance matrix of individual-level
// random effects for the K - 1 responses. We then calculate the correlation between
// these effects, Rho_id, via a recomposition from the Cholesky matrix.
// We also define a vector of length N for the log likelihood values, subsequently calling
// STAN's categorical_logit_lpmf to generate the likelihood of each observation, conditional
// on the model. Note that this step requires a repetition of the likelihood function, as above.
generated quantities {
    matrix [K - 1, K - 1] Rho_id = L_Rho_id * L_Rho_id';
    vector [N] log_lik;

    for (i in 1:N) {
        vector [K] p;
        for (k in 1:(K - 1)) {
            p[k] = a[k] + v_id[id[i], k];
        }
        p[K] = 0;
        log_lik[i] = categorical_logit_lpmf(y[i] | p);
    }
}
