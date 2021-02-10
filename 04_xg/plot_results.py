#!/usr/bin/env python3

from os import environ
from os.path import join

from matplotlib.pyplot import close, figure, savefig, tight_layout
from numpy import empty
from pandas import read_csv
from scipy.special import expit
from scipy.stats import bernoulli, norm
from seaborn import histplot, scatterplot

import export_data

FILENAME = {
    "samples": join(environ["WD"], "04_xg", "out", "samples.csv"),
    "results": join(environ["WD"], "04_xg", "out", "results.png"),
}


def main():
    data = read_csv(export_data.FILENAME["data"])
    export_data.set_data(data)
    samples = read_csv(FILENAME["samples"])
    mean = samples.mean()
    n = 201 * 91
    xs = empty(n)
    ys = empty(n)
    i = 0
    for y in range(-45, 46, 1):
        for x in range(0, 201, 1):
            xs[i] = x
            ys[i] = y
            i += 1
    shot_prob = expit(
        norm.logpdf(xs, mean.shot_mu_x, mean.shot_sigma_x) +
        norm.logpdf(ys, mean.shot_mu_y, mean.shot_sigma_y),
    )
    shot_prob = \
        (shot_prob - shot_prob.min()) / (shot_prob.max() - shot_prob.min())
    goal_prob = bernoulli.pmf(1, expit(
        norm.logpdf(xs, mean.goal_mu_x, mean.goal_sigma_x) +
        norm.logpdf(ys, mean.goal_mu_y, mean.goal_sigma_y) +
        mean.goal_offset,
    ))
    fig = figure(figsize=(10, 13.5), dpi=75)
    gs = fig.add_gridspec(8, 2)
    ax0 = fig.add_subplot(gs[:2, :])
    ax1 = fig.add_subplot(gs[2:, 0])
    ax2 = fig.add_subplot(gs[2:, 1])
    histplot(
        samples.pred_goals,
        kde=True,
        discrete=True,
        color="gray",
        ec="w",
        ax=ax0,
    )
    ax0.set_ylabel("sim goals")
    ax0.axvline(data.goal.sum(), ls="--", color="tomato", label="obs goals")
    ax0.legend()
    kwargs = {
        "cmap": "bone",
    }
    ax1.set_title("shot probability")
    ax1.tricontourf(ys, xs, shot_prob, **kwargs)
    scatterplot(x=data.y, y=data.x, ax=ax1)
    ax2.set_title("goal probability")
    ax2.tricontourf(ys, xs, goal_prob, **kwargs)
    scatterplot(
        x=data.y,
        y=data.x,
        hue=data.goal.map({0: False, 1: True}),
        ax=ax2,
    )
    for ax in [ax1, ax2]:
        ax.set_aspect("equal")
        ax.set_xlim([-45.0, 45.0])
        ax.set_ylim([200.0, 0.0])
        ax.set_xlabel("")
        ax.set_ylabel("")
    tight_layout()
    savefig(FILENAME["results"])
    close()


if __name__ == "__main__":
    main()
