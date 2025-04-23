#!/bin/sh

set -e

export OLLAMA_HOST=0.0.0.0:11434

ollama serve &
until ollama list > /dev/null 2>&1; do
    echo "Aguardando Ollama subir..."
    sleep 1
done

if ! ollama list | grep -q "billumy"; then
    ollama create billumy -f /app/Modelfile
fi

wait
