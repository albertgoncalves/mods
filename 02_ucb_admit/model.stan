data {
    int<lower=1> n_obs;
    int<lower=1> n_dept;
    array[n_obs] int<lower=1> dept;
    array[n_obs] int<lower=0> applications;
    array[n_obs] int<lower=0> admit;
    array[n_obs] int<lower=0, upper=1> male;
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
    array[n_obs] int<lower=0> admit_pred;
    for (i in 1:n_obs) {
        admit_pred[i] = binomial_rng(
            applications[i],
            inv_logit(dept_rate[dept[i]] + (advantage * male[i]))
        );
    }
}
