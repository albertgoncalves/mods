#!/usr/bin/env python3

from json import dump
from numpy import arctan2, cos, degrees, sin, sqrt
from os import environ
from os.path import join

from pandas import read_csv
from sklearn.cluster import MiniBatchKMeans

FILENAME = {
    "data": join(environ["WD"], "data", "shots.csv"),
    "json": join(environ["WD"], "04_xg", "out", "data.json")
}
RINK = {
    "bounds": {
        "x": {
            "lower": 0.0,
            "upper": 200.0,
        },
        "y": {
            "lower": -42.5,
            "upper": 42.5,
        },
    },
    "goal": {
        "x": 11.0,
        "y": 0.0,
    },
    "blue_line": {
        "x": 75.0,
    },
}


def set_data(df):
    df.x = 100.0 - df.x
    assert RINK["bounds"]["x"]["lower"] <= df.x.min()
    assert df.x.max() <= RINK["bounds"]["x"]["upper"]
    assert RINK["bounds"]["y"]["lower"] <= df.y.min()
    assert df.y.max() <= RINK["bounds"]["y"]["upper"]
    columns = ["x", "y"]
    df["cluster"] = MiniBatchKMeans(n_clusters=4, n_init="auto") \
        .fit(df[columns]) \
        .predict(df[columns])
    df.goal = df.goal.astype("int32")
    delta = {
        "x": df.x - RINK["goal"]["x"],
        "y": df.y - RINK["goal"]["y"],
    }
    df["distance"] = \
        sqrt((delta["x"] * delta["x"]) + (delta["y"] * delta["y"]))
    df["radians"] = (
        arctan2(df.y - RINK["goal"]["y"], df.x - RINK["goal"]["x"])
    )
    df["degrees"] = degrees(df.radians)
    df["_x"] = RINK["goal"]["x"] + (df.distance * cos(df.radians))
    df["_y"] = RINK["goal"]["y"] + (df.distance * sin(df.radians))


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
