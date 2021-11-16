#!/bin/sh

VERSION="0.0.1"

docker build \
    --file irods/Dockerfile \
    --tag irods:${VERSION} \
./irods

docker tag irods:${VERSION} irods:latest
