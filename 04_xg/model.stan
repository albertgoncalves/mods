data {
    int<lower=1> n_obs;
    vector[n_obs] x;
    vector[n_obs] y;
    int<lower=0, upper=1> goal[n_obs];
}

parameters {
    real shot_mu_x;
    real shot_mu_y;
    real<lower=0.0> shot_sigma_x;
    real<lower=0.0> shot_sigma_y;
    real goal_mu_x;
    real goal_mu_y;
    real<lower=0.0> goal_sigma_x;
    real<lower=0.0> goal_sigma_y;
    real goal_offset;
}

model {
    shot_mu_x ~ normal(0.0, 5.0);
    shot_mu_y ~ normal(0.0, 1.0);
    shot_sigma_x ~ exponential(1.0);
    shot_sigma_y ~ exponential(1.0);
    goal_mu_x ~ normal(0.0, 5.0);
    goal_mu_y ~ normal(0.0, 1.0);
    goal_sigma_x ~ exponential(1.0);
    goal_sigma_y ~ exponential(1.0);
    goal_offset ~ cauchy(0.0, 1.0);
    x ~ normal(shot_mu_x, shot_sigma_x);
    y ~ normal(shot_mu_y, shot_sigma_y);
    for (i in 1:n_obs) {
        goal[i] ~ bernoulli_logit(
            normal_lpdf(x[i] | goal_mu_x, goal_sigma_x) +
            normal_lpdf(y[i] | goal_mu_y, goal_sigma_y) +
            goal_offset
        );
    }
}

generated quantities {
    int pred_goals;
    pred_goals = 0;
    for (i in 1:n_obs) {
        pred_goals += bernoulli_logit_rng(
            normal_lpdf(
                normal_rng(shot_mu_x, shot_sigma_x) |
                goal_mu_x,
                goal_sigma_x
            ) +
            normal_lpdf(
                normal_rng(shot_mu_y, shot_sigma_y) |
                goal_mu_y,
                goal_sigma_y
            ) +
            goal_offset
        );
    }
}
