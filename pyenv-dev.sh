#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

uvicorn app.main:app --host localhost --port 5000 --reload --env-file .env
