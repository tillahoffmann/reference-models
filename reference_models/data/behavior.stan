data {
    // Original data as provided in the supplementary material of Koster and McElreath.
    int K;
    int N;
    int N_id;
    int N_house;
    int N_month;
    array [N] int y;
    array [N] int id;
    array [N] int house_id;
    array [N] int month_id;
    vector [N] age_z;
    vector [N] age_zq;
    vector [N] wz;
    vector [N] sunday;
    vector [N] saturday;
    vector [N] time_z;
    vector [N] time_zq;
    vector [N] house_size_z;
    vector [N] rain_z;
}
