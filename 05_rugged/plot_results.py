#!/usr/bin/env python3

# NOTE: See `https://speakerdeck.com/rmcelreath/statistical-rethinking-fall-2017-lecture-09?slide=19`.

from os import environ
from os.path import join

from matplotlib import colormaps
from matplotlib.pyplot import close, rcParams, savefig, subplots, tight_layout
from pandas import DataFrame, read_csv
from seaborn import lineplot, set_style

import export_data

FILENAME = {
    "samples": join(environ["WD"], "05_rugged", "out", "samples.csv"),
    "results": join(environ["WD"], "05_rugged", "out", "results.png"),
}


def main():
    data = read_csv(export_data.FILENAME["data"])
    export_data.set_data(data)
    data = data.loc[data.log_gdp.notnull()].copy()
    data.reset_index(drop=True, inplace=True)
    samples = read_csv(FILENAME["samples"])
    preds = []
    for row in data.itertuples():
        sample = samples[f"log_gdp_pred.{row.Index + 1}"].values
        for i in range(len(samples)):
            preds.append({
                "rugged": row.rugged,
                "cont_africa": row.cont_africa,
                "log_gdp_pred": sample[i],
            })
    preds = DataFrame(preds)
    set_style("darkgrid")
    rcParams["font.family"] = "monospace"
    (_, axs) = subplots(2, figsize=(7, 13.5), dpi=75)
    for i in range(2):
        rows = data.cont_africa == i
        axs[i].set_title(f"cont_africa = {i}")
        axs[i].scatter(
            data.loc[rows, "rugged"],
            data.loc[rows, "log_gdp"],
            color=colormaps.get_cmap("Set1")(i),
        )
        rows = preds.cont_africa == i
        lineplot(
            x=preds.loc[rows, "rugged"],
            y=preds.loc[rows, "log_gdp_pred"],
            errorbar="sd",
            alpha=0.35,
            ax=axs[i],
        )
    tight_layout(h_pad=4.0)
    savefig(FILENAME["results"])
    close()


if __name__ == "__main__":
    main()
