#!/usr/bin/env bash

set -eu

if [ ! -d "$WD/rethinking" ]; then
    mkdir "$WD/rethinking"
fi

(
    cd "$WD/rethinking"
    package="1.59.tar.gz"
    if [ ! -e "$package" ]; then
        wget "https://github.com/albertgoncalves/rethinking/archive/$package"
    fi
    if [ ! -e "rethinking" ]; then
        R CMD INSTALL -l "$WD/rethinking" $package
    fi
)
