#!/usr/bin/env python3

# NOTE: See `https://youtu.be/OdWXsqYKwHk?t=712`.

from os import environ
from os.path import join

from matplotlib.cm import get_cmap
from matplotlib.pyplot import close, savefig, subplots, tight_layout
from pandas import DataFrame, read_csv
from seaborn import histplot, set_style

import export_data

FILENAME = {
    "samples": join(environ["WD"], "03_ucb_admit", "out", "samples.csv"),
    "results": join(environ["WD"], "03_ucb_admit", "out", "results.png"),
}


def main():
    data = read_csv(export_data.FILENAME["data"])
    export_data.set_data(data)
    data["rate"] = data.admit / data.applications

    samples = read_csv(FILENAME["samples"])
    assert (samples["rho.1.2"] == samples["rho.2.1"]).all()
    assert -1.0 <= samples["rho.1.2"].min()
    assert samples["rho.1.2"].max() <= 1.0

    preds = DataFrame(
        [
            {
                "dept": row.dept,
                "male": row.male,
                "mean": samples[f"admit_pred.{row.Index + 1}"].mean(),
                "std": samples[f"admit_pred.{row.Index + 1}"].std(),
                "applications": row.applications,
            }
            for row in data.itertuples()
        ],
    )

    set_style("darkgrid")
    (_, axs) = subplots(3, figsize=(6, 11.25))
    rows = data.male == 1
    kwargs = {
        "alpha": 0.725,
    }

    ax0 = axs[0].twinx()
    ax0.bar(
        data.index,
        data.applications,
        color=data.dept.map(lambda i: get_cmap("Dark2")(i - 1)),
        alpha=0.2,
        zorder=1,
    )
    ax0.set_ylabel("applications")
    ax0.grid(None)

    axs[0].scatter(
        data.loc[rows].index,
        data.loc[rows, "rate"],
        marker="s",
        label="obs male",
        zorder=3,
        **kwargs,
    )
    axs[0].scatter(
        data.loc[~rows].index,
        data.loc[~rows, "rate"],
        marker="s",
        label="obs female",
        zorder=3,
        **kwargs,
    )
    axs[0].scatter(
        preds.index,
        preds["mean"] / preds.applications,
        marker="o",
        edgecolor="dimgray",
        color="none",
        label="pred mean",
        zorder=2,
        **kwargs,
    )
    axs[0].vlines(
        preds.index,
        (preds["mean"] - preds["std"]) / preds.applications,
        (preds["mean"] + preds["std"]) / preds.applications,
        color="dimgray",
        label="pred std",
        zorder=1,
        **kwargs,
    )
    axs[0].set_xticks(data.index)
    axs[0].set_ylim([0.0, 1.0])
    axs[0].set_ylabel("admit rate")
    axs[0].legend()

    histplot(x=samples["rho.1.2"], kde=True, stat="density", ax=axs[1])
    axs[1].set_xlabel("intercept-slope correlation")
    axs[1].set_ylabel("density")
    axs[1].set_xlim([-1.0, 1.0])

    axs[2].scatter(
        samples[f"mu.1"],
        samples[f"mu.2"],
        ec="w",
        alpha=0.5,
        label="mu",
    )
    for dept in data["dept"].unique():
        axs[2].scatter(
            samples[f"alpha_beta.{dept}.1"],
            samples[f"alpha_beta.{dept}.2"],
            ec="w",
            alpha=0.5,
            label=f"alpha-beta-{dept}",
        )
    axs[2].legend(loc="center left", bbox_to_anchor=(1, 0.5), frameon=False)

    tight_layout()
    savefig(FILENAME["results"])
    close()


if __name__ == "__main__":
    main()
