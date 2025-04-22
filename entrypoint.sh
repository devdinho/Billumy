#!/bin/sh
export OLLAMA_HOST=0.0.0.0:11414

ollama serve & sleep 5

set -e
if ! ollama list | grep -q "billumy"; then
    ollama create billumy -f /app/Modelfile
fi
wait