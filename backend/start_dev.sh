#!/bin/bash

# Activate virtual environment (compatible with both venv and .venv)
if [ -d "../.venv" ]; then
    source ../.venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ Virtual environment not found"
    exit 1
fi

# Verify we're using the correct Python
echo "Using Python: $(which python)"
echo "Using uvicorn: $(which uvicorn)"
echo ""
echo "Starting backend on http://localhost:8000"
echo "API docs: http://localhost:8000/docs"
echo ""

# Start uvicorn with reload
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
