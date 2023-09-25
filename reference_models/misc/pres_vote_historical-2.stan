/*
Hierarchical Gaussian process model for election forecasting inspired by Rob Trangucci's
[presentation](https://mc-stan.org/events/stancon2017-notebooks/stancon2017-trangucci-hierarchical-gps.pdf)
at StanCon 2017. A country-level GP is added and the kernel is reduced from a superposition of two
squared exponentials to one Matern 3/2.
*/

functions {
    #include util.stan
}

data {
    int<lower=1> n, n_states, n_regions, n_years;
    array [n_states] int<lower=1, upper=n_regions> state_region_ind;
    array [n] int<lower=1, upper=n_states> state_ind;
    array [n] int<lower=1, upper=n_regions> region_ind;
    array [n] int<lower=1, upper=n_years> year_ind;
    vector<lower=0, upper=1> [n] y;
}

transformed data {
    // One variance for the state-level and region-level GPs each, one for year offsets,
    // one for region offsets, and n_states for state offsets with variance grouped by region.
    int n_var_components = n_regions + 4;
    array [n_years] real years;
    for (t in 1:n_years) {
        years[t] = t;
    }
    array [n] int year_state_ind = compress_index(year_ind, state_ind, n_years);
    array [n] int year_region_ind = compress_index(year_ind, region_ind, n_years);
}

parameters {
    vector[n_states] state_raw;
    vector[n_regions] region_raw;
    real<lower=0> tot_var;
    simplex[n_var_components] prop_var;
    real mu;
    real<lower=0> nu;

    // Latent GP parameters and hyperparameters.
    vector[n_years] gp_year_raw;
    matrix[n_years, n_regions] gp_region_raw;
    matrix[n_years, n_states] gp_state_raw;
    real<lower=0> length_gp_region, length_gp_state, length_gp_year;
}

transformed parameters {
    // Allocate variance components.
    vector[n_var_components] vars = n_var_components * prop_var * tot_var;
    real sigma_gp_year = sqrt(vars[1]);
    real sigma_region = sqrt(vars[2]);
    real sigma_gp_region = sqrt(vars[3]);
    real sigma_gp_state = sqrt(vars[4]);
    vector<lower=0> [n_regions] sigma_state = sqrt(vars[5:]);

    // Idiosyncratic behavior of regions and states.
    vector[n_regions] region_re = sigma_region * region_raw;
    vector[n_states] state_re = sigma_state[state_region_ind] .* state_raw;

    // Evaluate GPs based on whitened variables.
    matrix[n_years, n_regions] gp_region;
    matrix[n_years, n_states] gp_state;
    vector[n_years] gp_year;
    {
        matrix[n_years, n_years] cov_region = add_diag(
            gp_matern32_cov(years, sigma_gp_region, length_gp_region), 1e-12);
        matrix[n_years, n_years] cov_state = add_diag(
            gp_matern32_cov(years, sigma_gp_state, length_gp_state), 1e-12);
        matrix[n_years, n_years] cov_year = add_diag(
            gp_matern32_cov(years, sigma_gp_year, length_gp_year), 1e-12);
        gp_region = cholesky_decompose(cov_region) * gp_region_raw;
        gp_state = cholesky_decompose(cov_state) * gp_state_raw;
        gp_year = cholesky_decompose(cov_year) * gp_year_raw;
    }

    // Evaluate the linear predictor.
    vector[n] obs_mu = inv_logit(mu + gp_year[year_ind] + state_re[state_ind]
        + region_re[region_ind] + to_vector(gp_region)[year_region_ind]
        + to_vector(gp_state)[year_state_ind]);
}

model {
    y ~ beta(nu * obs_mu, nu * (1 - obs_mu));
    to_vector(gp_region_raw) ~ normal(0, 1);
    to_vector(gp_state_raw) ~ normal(0, 1);
    gp_year_raw ~ normal(0, 1);
    state_raw ~ normal(0, 1);
    region_raw ~ normal(0, 1);
    mu ~ normal(0, .5);
    tot_var ~ gamma(3, 3);
    nu ~ gamma(5, 0.01);
    prop_var ~ dirichlet(rep_vector(2, n_var_components));
    length_gp_region ~ weibull(2, 5);
    length_gp_state ~ weibull(2, 5);
    // Allow smaller length scales for years because they can change relatively rapidly in response
    // to candidates or macroscopic shifts.
    length_gp_year ~ weibull(2, 3);
}
