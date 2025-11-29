FROM ubuntu:latest

RUN apt update && apt install -y curl git iproute2 net-tools

RUN curl -fsSL https://ollama.com/install.sh | sh

WORKDIR /app
COPY Modelfile-qwen* /app/
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 11414
CMD ["/app/entrypoint.sh"]