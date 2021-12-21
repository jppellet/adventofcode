#!/bin/bash

dir=$(dirname "$0")
cmd="$@"

do_run() {
    clear
    $cmd
}

do_run
while watchdir "$dir"; do
    do_run
    sleep 1
done
