/**
* Compress a tuple of indices to a single index that can be applied to a vectorized matrix.
*/
array [] int compress_index(array [] int i, array [] int j, int n_rows) {
    int n = size(i);
    array [n] int ij;
    for (k in 1:n) {
        ij[k] = n_rows * (j[k] - 1) + i[k];
    }
    return ij;
}
