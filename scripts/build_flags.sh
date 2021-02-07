#!/usr/bin/env bash

set -eu

flags=(
    "-march=native"
    "-O3"
    "-Wall"
    "-Wcast-align"
    "-Wcast-align=strict"
    "-Wcast-qual"
    "-Wdate-time"
    "-Wduplicated-branches"
    "-Wduplicated-cond"
    "-Werror"
    "-Wextra"
    "-Wfatal-errors"
    "-Wformat=2"
    "-Wformat-signedness"
    "-Winline"
    "-Wlogical-op"
    "-Wmissing-include-dirs"
    "-Wno-analyzer-possible-null-argument"
    "-Wno-deprecated-copy"
    "-Wno-stack-protector"
    "-Wno-type-limits"
    "-Wno-unused-but-set-variable"
    "-Wno-unused-function"
    "-Wno-unused-local-typedefs"
    "-Wno-unused-parameter"
    "-Wno-unused-variable"
    "-Wnull-dereference"
    "-Wpacked"
    "-Wpointer-arith"
    "-Wredundant-decls"
    "-Wstack-protector"
    "-Wswitch-enum"
    "-Wtrampolines"
    "-Wwrite-strings"
)
export CXXFLAGS="${flags[*]}"
