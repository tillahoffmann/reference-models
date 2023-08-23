data {
    int n_responses, n_states, n_ages, n_edus, n_regions;
    array [n_responses] int<lower=0, upper=1> y;
    vector<lower=0, upper=1> [n_responses] black, female;
    array [n_responses] int<lower=1, upper=n_ages> age;
    array [n_responses] int<lower=1, upper=n_edus> edu;
    array [n_responses] int<lower=1, upper=n_ages * n_edus> age_edu;
    array [n_responses] int<lower=1, upper=n_states> state;
    array [n_responses] int<lower=1, upper=n_regions> region_full;
    vector<lower=0, upper=1> [n_responses] v_prev_full;
}
