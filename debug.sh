#!/usr/bin/env bash
set -x  # Enable debug mode to print each command before executing it

echo ">>> Checking project directory contents:"
ls -lah  # List all files with detailed information

echo ">>> Checking .venv directory:"
ls -lah .venv/bin  # List contents of the virtual environment's bin directory

echo ">>> Checking gunicorn binary:"
file .venv/bin/gunicorn  # Show details about the gunicorn binary

echo ">>> Trying to run gunicorn:"
.venv/bin/gunicorn --version  # Print gunicorn version if executable
