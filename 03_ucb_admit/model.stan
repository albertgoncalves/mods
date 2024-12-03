data {
    int<lower=1> n_obs;
    int<lower=1> n_dept;
    array[n_obs] int<lower=1> dept;
    array[n_obs] int<lower=0> admit;
    array[n_obs] int<lower=0> applications;
    array[n_obs] int<lower=0, upper=1> male;
}

transformed data {
    array[n_obs] vector<lower=0.0, upper=1.0>[2] x;
    for (i in 1:n_obs) {
        x[i, 1] = 1.0;
        x[i, 2] = male[i];
    }
}

parameters {
    array[n_dept] vector[2] alpha_beta;
    vector[2] mu;
    vector<lower=0.0>[2] sigma;
    corr_matrix[2] rho;
}

transformed parameters {
    cov_matrix[2] sigma_rho = quad_form_diag(rho, sigma);
}

model {
    mu ~ normal(0.0, 1.0);
    sigma ~ exponential(1.0);
    rho ~ lkj_corr(2.0);

    alpha_beta ~ multi_normal(mu, sigma_rho);

    for (i in 1:n_obs) {
        admit[i] ~ binomial_logit(applications[i], dot_product(alpha_beta[dept[i]], x[i]));
    }
}

generated quantities {
    array[n_obs] int<lower=0> admit_pred;
    for (i in 1:n_obs) {
        admit_pred[i] = binomial_rng(
            applications[i],
            inv_logit(dot_product(alpha_beta[dept[i]], x[i]))
        );
    }
}
