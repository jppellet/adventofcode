#!/bin/bash

dir=$(dirname "$0")
while watchdir "$dir"; do
    clear
    "$@"
done
