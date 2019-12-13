#!/usr/bin/env bash

if [ -z "$1" ]; then
    exit 1
fi

__DIR__=`dirname $0`
__DIR__=`(cd $__DIR__; pwd)`

lcov --no-list-full-path --list $1 | ${__DIR__}/lcov2md.py
