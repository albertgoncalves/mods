#!/usr/bin/env python3

# NOTE: See `https://youtu.be/DyrUkqK9Tj4?t=1898`.

from json import dump
from os import environ
from os.path import join

from pandas import read_csv

FILENAME = {
    "data": join(environ["WD"], "data", "ucb_admit.csv"),
    "json": join(environ["WD"], "01_ucb_admit", "out", "data.json")
}


def set_data(df):
    df["male"] = df.applicant_gender.map({"male": 1, "female": 0})
    assert (df.admit + df.reject == df.applications).all()
    df.drop(columns=["applicant_gender", "reject"], inplace=True)
    df.dept = \
        df.dept.map({key: i + 1 for (i, key) in enumerate(df.dept.unique())})


def main():
    df = read_csv(FILENAME["data"])
    set_data(df)
    data = df.to_dict(orient="list")
    data["n"] = len(df)
    with open(FILENAME["json"], "w") as file:
        dump(data, file)


if __name__ == "__main__":
    main()
