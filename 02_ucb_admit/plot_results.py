#!/usr/bin/env python3

# NOTE: See `https://youtu.be/DyrUkqK9Tj4?t=3464`.

from os import environ
from os.path import join

from matplotlib.cm import get_cmap
from matplotlib.pyplot import close, savefig, subplots, tight_layout
from pandas import DataFrame, read_csv
from seaborn import set_style

import export_data

FILENAME = {
    "samples": join(environ["WD"], "02_ucb_admit", "out", "samples.csv"),
    "results": join(environ["WD"], "02_ucb_admit", "out", "results.png"),
}


def main():
    data = read_csv(export_data.FILENAME["data"])
    export_data.set_data(data)
    data["rate"] = data.admit / data.applications
    samples = read_csv(FILENAME["samples"])
    preds = []
    for row in data.itertuples():
        preds.append({
            "dept": row.dept,
            "male": row.male,
            "mean": samples[f"admit_pred.{row.Index + 1}"].mean(),
            "std": samples[f"admit_pred.{row.Index + 1}"].std(),
            "applications": row.applications,
        })
    preds = DataFrame(preds)
    set_style("darkgrid")
    (_, ax) = subplots(figsize=(6, 6))
    rows = data.male == 1
    kwargs = {
        "alpha": 0.725,
    }
    ax0 = ax.twinx()
    ax0.bar(
        data.index,
        data.applications,
        color=data.dept.map(lambda i: get_cmap("Dark2")(i - 1)),
        alpha=0.2,
        zorder=1,
    )
    ax0.set_ylabel("applications")
    ax0.grid(None)
    ax.scatter(
        data.loc[rows].index,
        data.loc[rows, "rate"],
        marker="s",
        label="obs male",
        zorder=3,
        **kwargs,
    )
    ax.scatter(
        data.loc[~rows].index,
        data.loc[~rows, "rate"],
        marker="s",
        label="obs female",
        zorder=3,
        **kwargs,
    )
    ax.scatter(
        preds.index,
        preds["mean"] / preds.applications,
        marker="o",
        edgecolor="dimgray",
        color="none",
        label="pred mean",
        zorder=2,
        **kwargs,
    )
    ax.vlines(
        preds.index,
        (preds["mean"] - preds["std"]) / preds.applications,
        (preds["mean"] + preds["std"]) / preds.applications,
        color="dimgray",
        label="pred 2*std",
        zorder=1,
        **kwargs,
    )
    ax.set_xticks(data.index)
    ax.set_ylim([0.0, 1.0])
    ax.set_ylabel("admit rate")
    ax.legend()
    tight_layout()
    savefig(FILENAME["results"])
    close()


if __name__ == "__main__":
    main()
