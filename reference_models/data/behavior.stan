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
    array [N] real age_z;
    array [N] real age_zq;
    array [N] real wz;
    array [N] real sunday;
    array [N] real saturday;
    array [N] real time_z;
    array [N] real time_zq;
    array [N] real house_size_z;
    array [N] real rain_z;
}
