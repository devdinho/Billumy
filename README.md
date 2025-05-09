# 📊 Billumy

**Billumy** é um serviço baseado em **Modelos de Linguagem de Última Geração (LLMs)** para interpretação de dados e geração de insights acionáveis. Ele atua como intermediário inteligente entre sistemas externos (como um backend Django) e um modelo de linguagem, fornecendo respostas contextualizadas a partir de prompts.

---

## 🚀 Funcionalidades

- 🔍 **Interpretação de Dados**  
  Compreende e responde a perguntas com base em contexto fornecido via prompt.

- 🤖 **Processamento com LLMs**  
  Utiliza modelos de linguagem para gerar respostas ricas e precisas.

- 🔗 **API Integrável**  
  Ideal para ser consumido por outras aplicações via requisições HTTP.

- ⚡ **Escalável com Docker & Nginx**  
  Deploy facilitado com arquitetura modular em containers.

---

## 🏗 Arquitetura

O sistema é composto por três serviços principais:

1. **Billumy** — API responsável pela comunicação com o modelo de linguagem  
2. **Billumy Service** — FastAPI que gerencia as requisições e conversa com MongoDB e Redis  

🔌 A aplicação Django e o banco de dados principal rodam fora do projeto e se conectam à API da Billumy para obter insights.

---

## 🛠 Tecnologias Utilizadas

- **[FastAPI](https://fastapi.tiangolo.com/)**  
- **[Ollama](https://ollama.com/)** (execução de modelos LLM localmente)  
- **MongoDB** (armazenamento das conversas)  
- **Redis** (cache e controle de contexto)  
- **Docker & Docker Compose** (ambiente isolado e replicável)  

---

## ⚙️ Instalação

### 1️⃣ Clone o repositório  
```bash
git clone https://github.com/devdinho/Billumy.git
cd Billumy
```

### 2️⃣ Variáveis de ambiente  
Crie um arquivo `.env` com as configurações necessárias:

```env
MONGO_URL=mongodb://billumy-mongo:27017
REDIS_URL=redis://billumy-redis:6379
BILLUMY_URL=http://billumy:11414
BILLUMY_API_KEY=Seu Token
```

### 3️⃣ Build e execução dos containers  
```bash
docker compose up -d --build
```

---

## 🌐 Acesso

Após subir os containers, a aplicação estará disponível em:  
```
http://localhost:8011
```

## 🚀 Endpoints e Payloads

### Endpoint: `chats/chat/stream`

#### Exemplo de Payload
```json
{
  "model": "billumy",
  "messages": [
    {
      "role": "system",
      "content": "Você é um assistente útil."
    },
    {
      "role": "user",
      "content": "Quais foram meus maiores gastos este mês?"
    }
  ]
}
```

#### Exemplo de Resposta
```json
{
  "id": "e9cbc446026341f6819d675d5a01a445",
  "user_id": "1",
  "title": null,
  "created_at": "2025-04-28T00:27:48.180000",
  "updated_at": "2025-04-28T00:28:07.572000",
  "data": {
    "model": "billumy",
    "messages": [
      {
        "role": "system",
        "content": "Você está interagindo com um assistente de IA."
      },
      {
        "role": "user",
        "content": "Qual é o clima hoje?"
      },
      {
        "role": "assistant",
        "content": "O clima hoje está ensolarado com 28°C."
      }
    ],
    "stream": true
  }
}
```

## 🔐 Segurança

- Requisições só são aceitas com **token válido** no header  
- Comunicação feita localmente por padrão (`localhost:8011`)  
- Pode ser facilmente adaptado para HTTPS com certificados

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License**.  
Confira o arquivo [`LICENSE`](LICENSE) para mais informações.
