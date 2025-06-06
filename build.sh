#!/usr/bin/env bash

# ------------------------------------------------------------------------------
# build.sh - Setup script for the project
#
# Usage:
#   ./build.sh
#
# Description:
#   - Checks for `uv` (Python package manager); installs it if missing
#   - Installs dependencies via Makefile
#   - Initializes PostgreSQL database using `psql` and the DATABASE_URL
# ------------------------------------------------------------------------------

# Check if `uv` is installed; install if missing
if ! command -v uv &> /dev/null
then
    echo "uv not found. Installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
else
    echo "uv is already installed."
fi

# Install dependencies using Makefile
make install

# Initialize PostgreSQL database
psql -a -d $DATABASE_URL -f database.sql
