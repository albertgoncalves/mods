data {
    int<lower=1> n_obs;
    int<lower=1> n_dept;
    int<lower=1> dept[n_obs];
    int<lower=0> applications[n_obs];
    int<lower=0> admit[n_obs];
    int<lower=0, upper=1> male[n_obs];
}

parameters {
    vector[n_dept] dept_rate;
    real rate_mu;
    real<lower=0> rate_sigma;
    real advantage;
}

model {
    rate_mu ~ normal(0.0, 10.0);
    rate_sigma ~ cauchy(0.0, 2.0);
    dept_rate ~ normal(rate_mu, rate_sigma);
    advantage ~ normal(0.0, 1.0);
    for (i in 1:n_obs) {
        admit[i] ~ binomial_logit(
            applications[i],
            dept_rate[dept[i]] + (advantage * male[i])
        );
    }
}

generated quantities {
    int<lower=0> admit_pred[n_obs];
    for (i in 1:n_obs) {
        admit_pred[i] = binomial_rng(
            applications[i],
            inv_logit(dept_rate[dept[i]] + (advantage * male[i]))
        );
    }
}
