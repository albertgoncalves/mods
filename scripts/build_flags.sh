#!/usr/bin/env bash

set -eu

flags=(
    "-march=native"
    "-O3"
    "-Wall"
    "-Wcast-align"
    "-Wdate-time"
    "-Wduplicated-cond"
    "-Werror"
    "-Wextra"
    "-Wfatal-errors"
    "-Wformat=2"
    "-Wformat-signedness"
    "-Wlogical-op"
    "-Wmissing-include-dirs"
    "-Wno-analyzer-possible-null-argument"
    "-Wno-deprecated-copy"
    "-Wno-deprecated-declarations"
    "-Wno-error=overloaded-virtual"
    "-Wno-ignored-qualifiers"
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
    "-Wswitch-enum"
    "-Wtrampolines"
    "-Wwrite-strings"
)
export CXXFLAGS="${flags[*]}"
