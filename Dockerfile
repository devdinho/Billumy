FROM ubuntu:latest

RUN apt update && apt install -y curl git iproute2 net-tools

RUN curl -fsSL https://ollama.com/install.sh | sh

ENV OLLAMA_HOST=0.0.0.0:11414

RUN ollama serve & sleep 5 && ollama pull llama3

EXPOSE 11414

CMD ["ollama", "serve"]
