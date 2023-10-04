#include data/behavior.stan
parameters{
    array [K-1] real a;                  // intercepts for each behavior
    matrix[K-1,N_id] z_id;      		// matrix of indiv-level standardized random effects
    vector<lower=0>[K-1] sigma_id;  	 // stddev of indiv-level random effects
    cholesky_factor_corr[K-1] L_Rho_id;  // correlation matrix of indiv-level random effects
    matrix[K-1,N_house] z_house;     		 // matrix of house-level standardized random effects
    vector<lower=0>[K-1] sigma_house;   // stddev of house-level random effects
    cholesky_factor_corr[K-1] L_Rho_house;         // correlation matrix of house-level random effects
    matrix[K-1,N_month] z_month;      // matrix of house-level standardized random effects
    vector<lower=0>[K-1] sigma_month;   // stddev of house-level random effects
    cholesky_factor_corr[K-1] L_Rho_month;         // correlation matrix of house-level random effects
}
transformed parameters{
    matrix[N_id,K-1] v_id;
    matrix[N_house,K-1] v_house;
    matrix[N_month,K-1] v_month;
    v_id = (diag_pre_multiply(sigma_id,L_Rho_id) * z_id)';
	v_house = (diag_pre_multiply(sigma_house,L_Rho_house) * z_house)';
	v_month = (diag_pre_multiply(sigma_month,L_Rho_month) * z_month)';
}
model{
    // priors
    a ~ normal(0,1);

    // hyper-priors
    to_vector(z_id) ~ normal(0,1);
    sigma_id ~ exponential(1);
    L_Rho_id ~ lkj_corr_cholesky(2);
    to_vector(z_house) ~ normal(0,1);
    sigma_house ~ exponential(1);
    L_Rho_house ~ lkj_corr_cholesky(2);
    to_vector(z_month) ~ normal(0,1);
    sigma_month ~ exponential(1);
    L_Rho_month ~ lkj_corr_cholesky(2);

    // likelihood
    for ( i in 1:N ) {
        vector[K] p;
        for ( k in 1:(K-1) )
            p[k] = a[k] + v_id[id[i],k] + v_house[house_id[i],k] + v_month[month_id[i],k];
        p[K] = 0;
        y[i] ~ categorical_logit( p );
    }
}
generated quantities{
    matrix[K-1,K-1] Rho_id;
    matrix[K-1,K-1] Rho_house;
    matrix[K-1,K-1] Rho_month;
    vector[N] log_lik;
    Rho_id = L_Rho_id * L_Rho_id';
    Rho_house = L_Rho_house * L_Rho_house';
    Rho_month = L_Rho_month * L_Rho_month';

        for ( i in 1:N ) {
        vector[K] p;
        for ( k in 1:(K-1) )
           p[k] = a[k] + v_id[id[i],k] + v_house[house_id[i],k] + v_month[month_id[i],k];
        p[K] = 0;
        log_lik[i] = categorical_logit_lpmf( y[i] | p );
    }
}
