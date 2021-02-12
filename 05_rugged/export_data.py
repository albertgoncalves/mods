#!/usr/bin/env python3

from json import dump
from os import environ
from os.path import join

from numpy import log
from pandas import read_csv

FILENAME = {
    "data": join(environ["WD"], "data", "rugged.csv"),
    "json": join(environ["WD"], "05_rugged", "out", "data.json")
}


def set_data(df):
    df["log_gdp"] = log(df.rgdppc_2000)
    assert df.rugged.notnull().all()
    assert df.cont_africa.notnull().all()


def main():
    df = read_csv(FILENAME["data"])
    set_data(df)
    df = df.loc[df.log_gdp.notnull()]
    data = df[["log_gdp", "rugged", "cont_africa"]].to_dict(orient="list")
    data["n_obs"] = len(df)
    with open(FILENAME["json"], "w") as file:
        dump(data, file)


if __name__ == "__main__":
    main()
