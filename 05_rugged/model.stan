data {
    int<lower=1> n_obs;
    array[n_obs] real rugged;
    array[n_obs] int<lower=0, upper=1> cont_africa;
    array[n_obs] real log_gdp;
}

parameters {
    real scale_rugged;
    real scale_africa;
    real scale_interaction;
    real intercept;
    real<lower=0.0> sigma;
}

model {
    scale_africa ~ normal(0.0, 1.0);
    scale_rugged ~ normal(0.0, 1.0);
    scale_interaction ~ normal(0.0, 1.0);
    intercept ~ normal(8.0, 100.0);
    sigma ~ normal(0.0, 10.0);
    for (i in 1:n_obs) {
        log_gdp[i] ~ normal(
            (scale_rugged * rugged[i]) +
            (scale_africa * cont_africa[i]) +
            (scale_interaction * rugged[i] * cont_africa[i]) +
            intercept,
            sigma
        );
    }
}

generated quantities {
    array[n_obs] real log_gdp_pred;
    for (i in 1:n_obs) {
        log_gdp_pred[i] =
            (scale_rugged * rugged[i]) +
            (scale_africa * cont_africa[i]) +
            (scale_interaction * rugged[i] * cont_africa[i]) +
            intercept;
    }
}
