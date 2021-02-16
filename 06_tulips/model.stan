data {
    int<lower=1> n_obs;
    vector[n_obs] water;
    vector[n_obs] shade;
    vector[n_obs] blooms;
}

parameters {
    real scale_water;
    real scale_shade;
    real scale_interaction;
    real intercept;
    real<lower=0.0> sigma;
}

model {
    scale_water ~ normal(0.0, 0.25);
    scale_shade ~ normal(0.0, 0.25);
    scale_interaction ~ normal(0.0, 0.25);
    intercept ~ normal(0.5, 0.25);
    sigma ~ exponential(1.0);
    for (i in 1:n_obs) {
        blooms[i] ~ normal(
            (scale_water * water[i]) +
            (scale_shade * shade[i]) +
            (scale_interaction * water[i] * shade[i]) +
            intercept,
            sigma
        );
    }
}

generated quantities {
    real blooms_pred[n_obs];
    for (i in 1:n_obs) {
        blooms_pred[i] =
            (scale_water * water[i]) +
            (scale_shade * shade[i]) +
            (scale_interaction * water[i] * shade[i]) +
            intercept;
    }
}
