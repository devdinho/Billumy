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
3. **Nginx** — Proxy reverso responsável pela autenticação e roteamento  

🔌 A aplicação Django e o banco de dados principal rodam fora do projeto e se conectam à API da Billumy para obter insights.

---

## 🛠 Tecnologias Utilizadas

- **[FastAPI](https://fastapi.tiangolo.com/)**  
- **[Ollama](https://ollama.com/)** (execução de modelos LLM localmente)  
- **MongoDB** (armazenamento das conversas)  
- **Redis** (cache e controle de contexto)  
- **Nginx** (roteamento e segurança)  
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

---

## 📡 Uso da API

### 🔹 Enviar um prompt para o modelo
```bash
curl -X POST "http://localhost:8011/api/generate" \
     -H "Authorization: Bearer seu_token_secreto" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "billumy",
           "prompt": "Olá, me chamo Anderson, eu que te criei",
           "stream": false
         }'
```

### 📥 Exemplo de resposta
```json
{
  "model": "billumy",
  "created_at": "2025-04-03T02:42:49.393Z",
  "response": "Anderson! É um prazer conhecê-lo! Como você é o criador...",
  "done": true,
  "done_reason": "stop",
  "context": [...],
  "total_duration": 16049257639,
  "prompt_eval_count": 60,
  "eval_count": 84
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
