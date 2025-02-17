#!/usr/bin/env bash

if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

check_uv_installed() {
    if command -v uv &> /dev/null; then
        return 0
    else
        return 1
    fi
}

if [[ "$DEVELOPMENT" == "true" ]]; then
    echo "Local development detected."

    if check_uv_installed; then
        echo "uv is already installed."
    else
        echo "Installing uv..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
    fi

    uv pip freeze > requirements.txt
#    source $HOME/.local/bin/env
    make install
else
    echo "Deployment detected, using pip for dependency installation"
    pip install -r requirements.txt
fi

psql -a -d $DATABASE_URL -f database.sql