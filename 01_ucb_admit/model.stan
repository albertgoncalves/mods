data {
    int<lower=1> n_obs;
    int<lower=1> dept[n_obs];
    int<lower=0> applications[n_obs];
    int<lower=0> admit[n_obs];
    int<lower=0, upper=1> male[n_obs];
}

parameters {
    real rate;
    real advantage;
}

model {
    rate ~ normal(0.0, 10.0);
    advantage ~ normal(0.0, 10.0);
    for (i in 1:n_obs) {
        admit[i] ~ binomial_logit(
            applications[i],
            rate + (advantage * male[i])
        );
    }
}

generated quantities {
    int<lower=0> admit_pred[n_obs];
    for (i in 1:n_obs) {
        admit_pred[i] = binomial_rng(
            applications[i],
            inv_logit(rate + (advantage * male[i]))
        );
    }
}
