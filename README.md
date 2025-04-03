# 📊 Billumy

**Billumy** é um serviço baseado em **Modelos de Linguagem de Última Geração (LLMs)** para interpretação de dados e geração de insights acionáveis. Ele recebe mensagens de um sistema externo (um backend Django) e retorna respostas processadas pelo modelo.

## 🚀 Funcionalidades

- 🔍 **Interpretação de Dados**: Analisa consultas e retorna respostas contextuais.  
- 🤖 **Processamento via LLMs**: Conecta-se a modelos de linguagem para gerar insights.  
- 🔗 **Integração via API**: Projetado para ser consumido por outros serviços.  
- ⚡ **Escalável com Docker e Nginx**: Fácil de implantar e gerenciar.  

## 🏗 Arquitetura

O sistema é composto por dois componentes principais:

1. **Billumy** (API do modelo de linguagem)  
2. **Nginx** (Proxy reverso para direcionar requisições)  

🔗 **A aplicação Django e o banco de dados são externos**, consumindo a API da Billumy.

## 🛠 Tecnologias Utilizadas

- **Ollama** (Para execução dos modelos de linguagem)  
- **Nginx** (Proxy reverso para segurança e roteamento)  
- **Docker & Docker Compose** (Para deploy e gerenciamento de containers)  

## 📦 Instalação e Configuração

### 1️⃣ Clonando o repositório  
```bash
git clone https://github.com/devdinho/Billumy.git
cd Billumy
```

### 2️⃣ Configuração do ambiente  
Crie um arquivo `.env` e defina as variáveis necessárias:
```ini
BILLUMY_API_KEY=seu_token_secreto
```

### 3️⃣ Subindo os containers  
```bash
docker compose up -d --build
```

### 4️⃣ Acessando o serviço  
Após iniciar os containers, o Billumy estará rodando em:
```
http://localhost:8080
```

## 🔗 Como consumir a API

### 🔹 Enviar uma mensagem para o modelo  
```bash
curl -X POST "http://localhost:8080/api/generate" \
     -H "Authorization: Bearer seu_token_secreto" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "billumy",
           "prompt": "Olá, me chamo Anderson, eu que te criei",
           "stream": false
         }'
```
📍 **Resposta esperada:**  
```json
{
  "model": "billumy",
  "created_at": "2025-04-03T02:42:49.393042808Z",
  "response": "Anderson! É um prazer conhecê-lo! Como você é o criador, posso dizer que estou animada para
    trabalhar com você e fornecer informações precisas e úteis. Qual é o objetivo da nossa conversa hoje? 
    Você em alguma pergunta ou necessidade específica que eu possa ajudar a resolver? Estou aqui para atender 
    às suas necessidades!",
  "done": true,
  "done_reason": "stop",
  "context": [
    128006,
    9125,
    128007,
    ...
    271
  ],
  "total_duration": 16049257639,
  "load_duration": 3826464531,
  "prompt_eval_count": 60,
  "prompt_eval_duration": 1938382879,
  "eval_count": 84,
  "eval_duration": 10283553776
}
```

## 📌 Configuração do Nginx

O **Nginx** dentro do container já está configurado para:
- Redirecionar requisições para a **Billumy**.
- Exigir um **token de autenticação** para acessar a API.

Se necessário, ajuste o `nginx.conf` no repositório para modificar o comportamento.

## 🛡 Segurança

- O serviço só pode ser acessado via **HTTP** no domínio `localhost:8080`.  
- O **token de autenticação** deve ser incluído no cabeçalho da requisição.  

## 📜 Licença  

Este projeto está licenciado sob a **MIT License**. Consulte o arquivo [`LICENSE`](LICENSE) para mais detalhes.  

---