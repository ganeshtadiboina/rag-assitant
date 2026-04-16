#!/bin/bash
echo "Starting RAG Assistant Backend..."
uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-10000}