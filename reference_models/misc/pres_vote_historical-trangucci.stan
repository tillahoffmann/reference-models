/*
Hierarchical Gaussian process model for election forecasting
[presented](https://mc-stan.org/events/stancon2017-notebooks/stancon2017-trangucci-hierarchical-gps.pdf)
by Rob Trangucci at StanCon 2017. The model is largely copied as-is from p. 21--23 with minor
modifications to variable names, changes to comply with recent Stan syntax, and performance
improvements. Generated quantities for actual forecasting are omitted here--future work.
*/

data {
    int<lower=1> n, n_states, n_regions, n_years;
    array [n_states] int<lower=1, upper=n_regions> state_region_ind;
    array [n] int<lower=1, upper=n_states> state_ind;
    array [n] int<lower=1, upper=n_regions> region_ind;
    array [n] int<lower=1, upper=n_years> year_ind;
    vector<lower=0, upper=1> [n] y;
}

transformed data {
    // Two variances for the state-level and region-level GPs each, one for year offsets,
    // one for region offsets, and n_states for state offsets with variance grouped by region.
    int n_var_components = n_regions + 6;
    array [n_years] real years;
    for (t in 1:n_years) {
        years[t] = t;
    }
}

parameters {
    vector[n_years] year_raw;
    vector[n_states] state_raw;
    vector[n_regions] region_raw;
    real<lower=0> tot_var;
    simplex[n_var_components] prop_var;
    real mu;
    real<lower=0> nu;

    // Latent GP parameters and hyperparameters.
    matrix[n_years, n_regions] gp_region_raw;
    matrix[n_years, n_states] gp_state_raw;
    real<lower=0> length_gp_region_long;
    real<lower=0> length_gp_state_long;
    real<lower=0> length_gp_region_short;
    real<lower=0> length_gp_state_short;
}

transformed parameters {
    // Allocate variance components.
    vector[n_var_components] vars = n_var_components * prop_var * tot_var;
    real sigma_year = sqrt(vars[1]);
    real sigma_region = sqrt(vars[2]);
    real sigma_gp_region_long = sqrt(vars[3]);
    real sigma_gp_state_long = sqrt(vars[4]);
    real sigma_gp_region_short = sqrt(vars[5]);
    real sigma_gp_state_short = sqrt(vars[6]);
    vector<lower=0> [n_regions] sigma_state = sqrt(vars[7:]);

    // Idiosyncratic behavior of regions, states, and years.
    vector[n_regions] region_re = sigma_region * region_raw;
    vector[n_years] year_re = sigma_year * year_raw;
    vector[n_states] state_re = sigma_state[state_region_ind] .* state_raw;

    // Evaluate GPs based on whitened variables.
    matrix[n_years, n_regions] gp_region;
    matrix[n_years, n_states] gp_state;
    {
        matrix[n_years, n_years] cov_region = add_diag(
            gp_exp_quad_cov(years, sigma_gp_region_long, length_gp_region_long)
            + gp_exp_quad_cov(years, sigma_gp_region_short, length_gp_region_short), 1e-12);
        matrix[n_years, n_years] cov_state = add_diag(
            gp_exp_quad_cov(years, sigma_gp_state_long, length_gp_state_long)
            + gp_exp_quad_cov(years, sigma_gp_state_short, length_gp_state_short), 1e-12);
        matrix[n_years, n_years] L_cov_region = cholesky_decompose(cov_region);
        matrix[n_years, n_years] L_cov_state = cholesky_decompose(cov_state);
        gp_region = L_cov_region * gp_region_raw;
        gp_state = L_cov_state * gp_state_raw;
    }

    // Evaluate the linear predictor.
    vector[n] obs_mu;
    for (i in 1:n) {
        obs_mu[i] = inv_logit(mu + year_re[year_ind[i]] + state_re[state_ind[i]]
            + region_re[region_ind[i]] + gp_region[year_ind[i], region_ind[i]]
            + gp_state[year_ind[i], state_ind[i]]);
    }
}

model {
    y ~ beta(nu * obs_mu, nu * (1 - obs_mu));
    to_vector(gp_region_raw) ~ normal(0, 1);
    to_vector(gp_state_raw) ~ normal(0, 1);
    year_raw ~ normal(0, 1);
    state_raw ~ normal(0, 1);
    region_raw ~ normal(0, 1);
    mu ~ normal(0, .5);
    tot_var ~ gamma(3, 3);
    nu ~ gamma(5, 0.01);
    prop_var ~ dirichlet(rep_vector(2, n_var_components));
    length_gp_region_long ~ weibull(30, 8);
    length_gp_state_long ~ weibull(30, 8);
    length_gp_region_short ~ weibull(30, 3);
    length_gp_state_short ~ weibull(30, 3);
}
