data {
    int<lower=1> n_obs;
    int<lower=1> n_dept;
    int<lower=1> dept[n_obs];
    int<lower=0> admit[n_obs];
    int<lower=0> applications[n_obs];
    int<lower=0, upper=1> male[n_obs];
}

parameters {
    vector[n_dept] dept_advantage;
    vector[n_dept] dept_rate;
    real rate;
    real advantage;
    vector<lower=0>[2] sigma;
    corr_matrix[2] rho;
}

transformed parameters {
    vector[2] intercept_slope[n_dept];
    vector[2] mu_rate_advantage;
    cov_matrix[2] sigma_rho;
    for (j in 1:n_dept) {
        intercept_slope[j, 1] = dept_rate[j];
        intercept_slope[j, 2] = dept_advantage[j];
    }
    mu_rate_advantage[1] = rate;
    mu_rate_advantage[2] = advantage;
    sigma_rho = quad_form_diag(rho, sigma);
}

model {
    rate ~ normal(0.0, 10.0);
    advantage ~ normal(0.0, 1.0);
    sigma ~ cauchy(0.0, 2.0);
    rho ~ lkj_corr(2.0);
    intercept_slope ~ multi_normal(mu_rate_advantage, sigma_rho);
    for (i in 1:n_obs) {
        admit[i] ~ binomial_logit(
            applications[i],
            dept_rate[dept[i]] + dept_advantage[dept[i]] * male[i]
        );
    }
}

generated quantities {
    int<lower=0> admit_pred[n_obs];
    for (i in 1:n_obs) {
        admit_pred[i] = binomial_rng(
            applications[i],
            inv_logit(dept_rate[dept[i]] + (dept_advantage[dept[i]] * male[i]))
        );
    }
}
