data {
    int<lower=1> n, n_counties;
    vector [n] x, u, y;
    array [n] int<lower=1, upper=n_counties> county_ind;
}
