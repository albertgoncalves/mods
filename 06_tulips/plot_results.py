#!/usr/bin/env python3

# NOTE: See `https://youtu.be/QhHfo6-Bx8o?t=2855`.

from os import environ
from os.path import join

from matplotlib.pyplot import close, rcParams, savefig, subplots, tight_layout
from pandas import DataFrame, read_csv
from seaborn import lineplot, scatterplot, set_style

import export_data

FILENAME = {
    "samples": join(environ["WD"], "06_tulips", "out", "samples.csv"),
    "results": join(environ["WD"], "06_tulips", "out", "results.png"),
}


def main():
    data = read_csv(export_data.FILENAME["data"])
    export_data.set_data(data)
    data.reset_index(drop=True, inplace=True)
    samples = read_csv(FILENAME["samples"])
    preds = []
    for row in data.itertuples():
        sample = samples[f"blooms_pred.{row.Index + 1}"].values
        for i in range(len(samples)):
            preds.append({
                "water": row.water,
                "shade": row.shade,
                "blooms_pred": sample[i],
            })
    preds = DataFrame(preds)
    set_style("darkgrid")
    rcParams["font.family"] = "monospace"
    (_, axs) = subplots(2, 3, sharey=True, figsize=(16, 10))
    scatter_kwargs = {
        "palette": "Dark2",
        "alpha": 0.85,
    }
    line_kwargs = {
        "ci": "sd",
        "alpha": 0.35,
    }
    assert data.shade.nunique() == 3
    for (i, shade) in enumerate(sorted(data.shade.unique())):
        cohort = data.loc[data.shade == shade]
        scatterplot(
            x=cohort.water,
            y=cohort.blooms,
            hue=cohort.bed,
            ax=axs[0, i],
            **scatter_kwargs,
        )
        cohort = preds.loc[preds.shade == shade]
        lineplot(
            x=cohort.water,
            y=cohort.blooms_pred,
            ax=axs[0, i],
            **line_kwargs,
        )
        axs[0, i].set_title(f"shade @ {shade}")
        axs[0, i].set_ylabel("blooms")
    assert data.water.nunique() == 3
    for (i, water) in enumerate(sorted(data.water.unique())):
        cohort = data.loc[data.water == water]
        scatterplot(
            x=cohort.shade,
            y=cohort.blooms,
            hue=cohort.bed,
            ax=axs[1, i],
            **scatter_kwargs,
        )
        cohort = preds.loc[preds.water == water]
        lineplot(
            x=cohort.shade,
            y=cohort.blooms_pred,
            ax=axs[1, i],
            **line_kwargs,
        )
        axs[1, i].set_title(f"water @ {water}")
        axs[1, i].set_ylabel("blooms")
        axs[1, i].invert_xaxis()
    tight_layout()
    savefig(FILENAME["results"])
    close()


if __name__ == "__main__":
    main()
