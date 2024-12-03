#!/usr/bin/env bash

set -eu

flags=(
    "-march=native"
    "-O3"
    "-Wno-deprecated-declarations"
)
export CXXFLAGS="${flags[*]}"
