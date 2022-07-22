#!/usr/bin/env bash

# set -o errexit
set -o pipefail
set -o nounset

PYENV_VIRTUALENV_DISABLE_PROMPT=1

eval "$(pyenv init -)"

pyenv install 3.10.3

pyenv virtualenv 3.10.3 rewardsapi

_OLD_VIRTUAL_PATH=""
_OLD_VIRTUAL_PYTHONHOME=""
_OLD_VIRTUAL_PS1=""
pyenv activate rewardsapi

python -m pip install -r requirements.txt
