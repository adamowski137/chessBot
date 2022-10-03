#!/bin/bash
set -e

build()
{
    cd build
    cmake ..
    make
    cd ..
}

build
