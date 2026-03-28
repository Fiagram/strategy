#! /bin/sh
if [ -d ".venv" ]; then
    echo "The .venv folder already exists"
else
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi



