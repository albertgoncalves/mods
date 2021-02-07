#!/usr/bin/env python3

# NOTE: See `https://youtu.be/DyrUkqK9Tj4?t=2925`.

from os import environ
from os.path import join

from matplotlib.pyplot import close, savefig, subplots, tight_layout
from pandas import DataFrame, read_csv
from seaborn import set_style

import export_data

FILENAME = {
    "samples": join(environ["WD"], "01_ucb_admit", "out", "samples.csv"),
    "results": join(environ["WD"], "01_ucb_admit", "out", "results.png"),
}


def main():
    data = read_csv(export_data.FILENAME["data"])
    export_data.set_data(data)
    data["rate"] = data.admit / data.applications
    data.reset_index(drop=False, inplace=True)
    samples = read_csv(FILENAME["samples"])
    preds = []
    for row in data.itertuples():
        preds.append({
            "index": row.index,
            "dept": row.dept,
            "male": row.male,
            "mean": samples[f"admit_pred.{row.index + 1}"].mean(),
            "std": samples[f"admit_pred.{row.index + 1}"].std(),
            "applications": row.applications,
        })
    preds = DataFrame(preds)
    set_style("darkgrid")
    (_, ax) = subplots(figsize=(6, 6))
    rows = data.male == 1
    ax.scatter(
        data.loc[rows, "index"],
        data.loc[rows, "rate"],
        marker="s",
        label="obs male",
    )
    ax.scatter(
        data.loc[~rows, "index"],
        data.loc[~rows, "rate"],
        marker="s",
        label="obs female",
    )
    ax.scatter(
        preds["index"],
        preds["mean"] / preds.applications,
        marker="o",
        edgecolor="dimgray",
        color="none",
        label="pred mean",
    )
    ax.vlines(
        preds["index"],
        (preds["mean"] - preds["std"]) / preds.applications,
        (preds["mean"] + preds["std"]) / preds.applications,
        label="pred 2*std",
    )
    ax.set_xticks(data["index"])
    ax.legend()
    tight_layout()
    savefig(FILENAME["results"])
    close()


if __name__ == "__main__":
    main()
