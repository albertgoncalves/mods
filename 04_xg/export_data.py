#!/usr/bin/env python3

from json import dump
from numpy import arctan2, cos, degrees, sin, sqrt
from os import environ
from os.path import join

from pandas import read_csv

FILENAME = {
    "data": join(environ["WD"], "data", "shots.csv"),
    "json": join(environ["WD"], "04_xg", "out", "data.json")
}
BOUNDS = {
    "x": {
        "min": 0.0,
        "max": 200.0,
    },
    "y": {
        "min": -45.0,
        "max": 45.0,
    },
}
GOAL = {
    "x": 11.0,
    "y": 0.0,
}


def set_data(df):
    df.x = 100.0 - df.x
    assert BOUNDS["x"]["min"] <= df.x.min()
    assert df.x.max() <= BOUNDS["x"]["max"]
    assert BOUNDS["y"]["min"] <= df.y.min()
    assert df.y.max() <= BOUNDS["y"]["max"]
    df.goal = df.goal.map({True: 1, False: 0})
    delta = {
        "x": df.x - GOAL["x"],
        "y": df.y - GOAL["y"],
    }
    df["distance"] = \
        sqrt((delta["x"] * delta["x"]) + (delta["y"] * delta["y"]))
    df["radians"] = (
        arctan2(df.y - GOAL["y"], df.x - GOAL["x"])
    )
    df["degrees"] = degrees(df.radians)
    df["_x"] = GOAL["x"] + (df.distance * cos(df.radians))
    df["_y"] = GOAL["y"] + (df.distance * sin(df.radians))


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
