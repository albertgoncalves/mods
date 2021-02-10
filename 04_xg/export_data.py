#!/usr/bin/env python3

from json import dump
from os import environ
from os.path import join

from pandas import read_csv

FILENAME = {
    "data": join(environ["WD"], "data", "shots.csv"),
    "json": join(environ["WD"], "04_xg", "out", "data.json")
}


def set_data(df):
    assert -100.0 <= df.x.min()
    assert df.x.max() <= 100.0
    assert -45.0 <= df.y.min()
    assert df.y.max() <= 45
    df.x = 100.0 - df.x
    df.goal = df.goal.map({True: 1, False: 0})


def main():
    df = read_csv(FILENAME["data"])
    set_data(df)
    columns = ["x", "y", "goal"]
    data = df[columns].to_dict(orient="list")
    data["n_obs"] = len(df)
    with open(FILENAME["json"], "w") as file:
        dump(data, file)


if __name__ == "__main__":
    main()
