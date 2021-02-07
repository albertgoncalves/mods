data {
    int<lower=1> n;
    int<lower=1> dept[n];
    int<lower=0> applications[n];
    int<lower=0> admit[n];
    int<lower=0, upper=1> male[n];
}

parameters {
    real rate;
    real advantage;
}

model {
    rate ~ normal(0.0, 10.0);
    advantage ~ normal(0.0, 10.0);
    for (i in 1:n) {
        admit[i] ~ binomial_logit(
            applications[i],
            rate + (advantage * male[i])
        );
    }
}

generated quantities {
    int<lower=0> admit_pred[n];
    for (i in 1:n) {
        admit_pred[i] = binomial_rng(
            applications[i],
            inv_logit(rate + (advantage * male[i]))
        );
    }
}
