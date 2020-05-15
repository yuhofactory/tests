#!/bin/bash

docker build -t ommohome .

# $1 and $2 are environment variables from Jenkins configuration
docker run --rm --name $1 -h docker ommohome $2

