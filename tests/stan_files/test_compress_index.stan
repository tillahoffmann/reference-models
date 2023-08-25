functions {
    #include util.stan
}

data {
    int n_rows, n_cols, n_idx;
    matrix [n_rows, n_cols] X;
    array [n_idx] int i, j;
}

generated quantities {
    vector [n_idx] Xij = to_vector(X)[compress_index(i, j, n_rows)];
}
