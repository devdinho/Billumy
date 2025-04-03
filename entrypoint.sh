#!/bin/sh
set -a
[ -f .env ] && . .env
set +a

TOKEN="$BILLUMY_AUTH_TOKEN"

echo "🔒 Usando o token do .env"

export OLLAMA_HOST=0.0.0.0:11414

ollama serve & sleep 5

set -e
if ! ollama list | grep -q "billumy"; then
    ollama create billumy -f /app/Modelfile
fi
wait