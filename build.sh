#!/usr/bin/env bash

# Usage:
#   ./build.sh [database_engine]
#
# Arguments:
#   database_engine - optional, "postgres" or "sqlite" (default: sqlite)
#
# Description:
#   - Installs uv if not already installed
#   - Installs project dependencies using `make install`
#   - Initializes the database (PostgreSQL or SQLite) using `database.sql`
# 
# Example usage:
# For SQLite (default):
# ./build.sh
# 
# For PostgreSQL:
# ./build.sh postgres


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

# Determine database engine (default: sqlite)
DB_ENGINE="${1:-sqlite}"

# Initialize database
case "$DB_ENGINE" in
    postgres)
        echo "Initializing PostgreSQL database..."
        psql -a -d "$DATABASE_URL" -f database.sql
        ;;
    sqlite)
        echo "Initializing SQLite database..."
        DB_PATH=$(echo "$DATABASE_URL" | sed 's|sqlite:///||')
        sqlite3 "$DB_PATH" < database.sql
        ;;
    *)
        echo "Unknown database engine: $DB_ENGINE"
        echo "Usage: ./build.sh [postgres|sqlite]"
        exit 1
        ;;
esac
