#!/usr/bin/env bash

# download uv and run dependencies install
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
make install

#source .venv/bin/activate

#bash debug.sh  # Run the debug script
