#!/bin/bash

# Set default port if not provided
export PORT=${PORT:-8080}

echo "Starting FastAPI server on port $PORT"
exec uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1