#!/bin/bash -ex
# To be sourced for installation
file_exists () {
    if [[ -f $1]]; code=$?; then
        echo "$1 exists"
    else
        echo "$1 not found" >&2
    fi
}

dir_exists () {

    if [[ -d $1 ]]; code=$?; then
        echo "$1 exists"
    else
        echo "$1 not found" >&2
    fi
}

user_exists () {
    if user_exists "$1"; code=$?; then  # use the function, save the code
        echo "$1 found"
    else
        echo "user $1 not found" >&2  # error messages should go to stderr
    fi
    exit $code  # set the exit code, ultimately the same set by `id`
}
