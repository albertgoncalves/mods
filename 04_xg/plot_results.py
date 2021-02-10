#!/usr/bin/env python3

from os import environ
from os.path import join

from matplotlib.gridspec import GridSpec
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


def load():
    data = read_csv(export_data.FILENAME["data"])
    export_data.set_data(data)
    return (data, read_csv(FILENAME["samples"]))


def sim(samples):
    n = 201 * 91
    sims = {
        "x": empty(n),
        "y": empty(n),
    }
    i = 0
    for y in range(-45, 46, 1):
        for x in range(0, 201, 1):
            sims["x"][i] = x
            sims["y"][i] = y
            i += 1
    mean = samples.mean()
    sims["shot_prob"] = expit(
        norm.logpdf(sims["x"], mean.shot_mu_x, mean.shot_sigma_x) +
        norm.logpdf(sims["y"], mean.shot_mu_y, mean.shot_sigma_y),
    )
    m = sims["shot_prob"].min()
    sims["shot_prob"] = (sims["shot_prob"] - m) / (sims["shot_prob"].max() - m)
    sims["goal_prob"] = bernoulli.pmf(1, expit(
        norm.logpdf(sims["x"], mean.goal_mu_x, mean.goal_sigma_x) +
        norm.logpdf(sims["y"], mean.goal_mu_y, mean.goal_sigma_y) +
        mean.goal_offset,
    ))
    return sims


def plot(data, samples, sims):
    fig = figure(figsize=(10, 13.5), dpi=75)
    gs = GridSpec(2, 2, figure=fig, height_ratios=[1, 5])
    ax0 = fig.add_subplot(gs[0, :])
    ax1 = fig.add_subplot(gs[1, 0])
    ax2 = fig.add_subplot(gs[1, 1])
    histplot(
        samples.pred_goals,
        kde=True,
        discrete=True,
        color="darkgray",
        ec="w",
        ax=ax0,
    )
    ax0.set_ylabel("sim goals")
    ax0.axvline(data.goal.sum(), ls="--", color="r", lw=2, label="obs goals")
    ax0.legend()
    kwargs = {
        "cmap": "bone",
    }
    ax1.set_title("shot probability")
    ax1.tricontourf(sims["y"], sims["x"], sims["shot_prob"], **kwargs)
    scatterplot(x=data.y, y=data.x, ax=ax1)
    ax2.set_title("goal probability")
    ax2.tricontourf(sims["y"], sims["x"], sims["goal_prob"], **kwargs)
    ax2.set_yticks([])
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


def main():
    (data, samples) = load()
    plot(data, samples, sim(samples))


if __name__ == "__main__":
    main()
