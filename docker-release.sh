#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

docker pull python:3.10-alpine

docker compose -f docker-compose.release.yml build

docker compose -f docker-compose.release.yml push
