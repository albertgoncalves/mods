data {
    int<lower=1> n_obs;
    array[n_obs] int<lower=1> dept;
    array[n_obs] int<lower=0> applications;
    array[n_obs] int<lower=0> admit;
    array[n_obs] int<lower=0, upper=1> male;
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
    array[n_obs] int<lower=0> admit_pred;
    for (i in 1:n_obs) {
        admit_pred[i] = binomial_rng(
            applications[i],
            inv_logit(rate + (advantage * male[i]))
        );
    }
}
