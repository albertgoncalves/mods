#!/usr/bin/env python3

from json import dump
from os import environ
from os.path import join

from pandas import read_csv

FILENAME = {
    "data": join(environ["WD"], "data", "tulips.csv"),
    "json": join(environ["WD"], "06_tulips", "out", "data.json")
}


def set_data(df):
    assert df.notnull().values.all()
    df.bed = df.bed.map({
        bed: i + 1 for (i, bed) in enumerate(sorted(df.bed.unique()))
    })
    for column in ["water", "shade"]:
        df[column] -= df[column].mean()
    m = df.blooms.min()
    df.blooms = (df.blooms - m) / (df.blooms.max() - m)


def main():
    df = read_csv(FILENAME["data"])
    set_data(df)
    data = df[["water", "shade", "blooms"]].to_dict(orient="list")
    data["n_obs"] = len(df)
    with open(FILENAME["json"], "w") as file:
        dump(data, file)


if __name__ == "__main__":
    main()
