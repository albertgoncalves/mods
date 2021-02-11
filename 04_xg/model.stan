data {
    int<lower=1> n_obs;
    vector[n_obs] x;
    vector[n_obs] y;
    int<lower=0, upper=1> goal[n_obs];
    // vector[n_obs] radians;
    // vector[n_obs] distance;
    // real<lower=0.0> goal_x;
    // real goal_y;
    // real min_x;
    // real max_x;
    // real min_y;
    // real max_y;
}

// transformed data {
//     vector<lower=0.0, upper=1.0>[n_obs] scale_x;
//     vector<lower=0.0, upper=1.0>[n_obs] scale_y;
//     real delta_x;
//     real delta_y;
//     scale_x = (x - min_x) / (max_x - min_x);
//     scale_y = (y - min_y) / (max_y - min_y);
//     delta_x = max_x - min_x;
//     delta_y = max_y - min_y;
// }

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
    // real distance_mu;
    // real<lower=0.0> distance_sigma;
    // real radians_mu;
    // real<lower=0.0> radians_sigma;
    // real<lower=0.0> alpha_x;
    // real<lower=0.0> alpha_y;
    // real<lower=0.0> beta_x;
    // real<lower=0.0> beta_y;
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
    // distance_mu ~ normal(0.0, 5.0);
    // distance_sigma ~ exponential(1.0);
    // radians_mu ~ normal(0.0, 1.0);
    // radians_sigma ~ exponential(1.0);
    x ~ normal(shot_mu_x, shot_sigma_x);
    y ~ normal(shot_mu_y, shot_sigma_y);
    // distance ~ normal(distance_mu, distance_sigma);
    // radians ~ normal(radians_mu, radians_sigma);
    // alpha_x ~ exponential(1.0);
    // beta_x ~ exponential(1.0);
    // alpha_y ~ exponential(1.0);
    // beta_y ~ exponential(1.0);
    // scale_x ~ beta(alpha_x, beta_x);
    // scale_y ~ beta(alpha_y, beta_y);
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
    // real pred_distance;
    // real pred_radians;
    pred_goals = 0;
    for (i in 1:n_obs) {
        // pred_distance = normal_rng(distance_mu, distance_sigma);
        // pred_radians = normal_rng(radians_mu, radians_sigma);
        pred_goals += bernoulli_logit_rng(
            normal_lpdf(
                normal_rng(shot_mu_x, shot_sigma_x) |
                // goal_x + (pred_distance * cos(pred_radians)) |
                // (beta_rng(alpha_x, beta_x) * delta_x) + min_x |
                goal_mu_x,
                goal_sigma_x
            ) +
            normal_lpdf(
                normal_rng(shot_mu_y, shot_sigma_y) |
                // goal_y + (pred_distance * sin(pred_radians)) |
                // (beta_rng(alpha_y, beta_y) * delta_y) + min_y |
                goal_mu_y,
                goal_sigma_y
            ) +
            goal_offset
        );
    }
}
