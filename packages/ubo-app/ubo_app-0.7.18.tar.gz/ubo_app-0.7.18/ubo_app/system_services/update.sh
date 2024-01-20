#!/usr/bin/env bash

set -ue

if [[ $(ls -A "$INSTALLATION_PATH/_update/") ]]; then
  sudo apt install python3-virtualenv
  rm -rf "$INSTALLATION_PATH/env"
  virtualenv --system-site-packages "$INSTALLATION_PATH/env"
  "$INSTALLATION_PATH/env/bin/python" -m pip install --no-index --upgrade --find-links "$INSTALLATION_PATH/_update/" ubo-app[default]
  "$INSTALLATION_PATH/env/bin/ubo" bootstrap && service ubo-app restart
fi
