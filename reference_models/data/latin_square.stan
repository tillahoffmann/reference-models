data {
    int n;
    array [n] int<lower=0, upper=5> row_idx, col_idx, treatment;
    vector [n] yield;
}
