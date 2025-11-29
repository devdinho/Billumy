#!/bin/sh

set -e

export OLLAMA_HOST=0.0.0.0:11414

ollama serve &
until ollama list > /dev/null 2>&1; do
    echo "Aguardando Ollama subir..."
    sleep 1
done

# Criar modelos customizados
if ! ollama list | grep -q "billumy-14b"; then
    ollama create billumy-14b -f /app/Modelfile-qwen14b
fi

if ! ollama list | grep -q "billumy-32b"; then
    ollama create billumy-32b -f /app/Modelfile-qwen32b
fi

# Puxar modelo de embedding
if ! ollama list | grep -q "mxbai-embed-large"; then
    ollama pull mxbai-embed-large
fi

wait
