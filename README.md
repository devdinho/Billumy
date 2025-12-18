![Billumy-logo](https://portifolio.dinho.dev/media/projetos/Billumy_site.png)

# 🧠 Billumy – Assistente de IA com Ollama

### Modelos customizados, embeddings e arquitetura segura com Nginx + NMS

A **Billumy** é uma assistente de IA especializada em análise de dados, construída sobre modelos **Qwen 2.5** personalizados e executada dentro do ambiente **Ollama**.  
O projeto utiliza um pipeline seguro de validação de acesso com **Nginx + Nubo Management System (NMS)** para garantir isolamento, autenticação e controle granular sobre cada rota de modelo.

---

## 🚀 Visão Geral da Arquitetura

A arquitetura deste projeto combina:

### **1. Ollama**

Servindo os modelos customizados:

- `billumy-qwen14b` → rápido e econômico (14B parâmetros)
- `billumy-qwen32b` → raciocínio mais robusto (32B parâmetros)
- `billumy-maestro` → classificador de complexidade de perguntas (1.5B parâmetros)
- `mxbai-embed-large` → geração de embeddings

### **2. Nginx (Servidor)**

Configurado como **site em `sites-available`** para:

- interceptar todas as requisições HTTP/S
- validar o **Token de Operação (TOC)** via NMS
- rotear o tráfego para o servidor Ollama
- garantir logs centralizados, isolamento e regras de acesso corporativas

### **3. Nubo Management System (NMS)**

Responsável por:

- autenticação e autorização do TOC
- validação de permissões para rotas e modelos específicos
- registro de auditoria
- controle granular de uso de modelos de linguagem corporativos

### **4. Billumy (Prompt Engineering)**

Os modelos carregam um sistema prompt personalizado:

> “Você é a Billumy, uma assistente de IA especializada em análise de dados. Todas as respostas devem ser em português, com explicações claras, educadas e profissionais. Este projeto é parte do TCC de Anderson Freitas, sob orientação do Prof. Dr. Ary Henrique Morais Oliveira e Prof. Dr. Eduardo Ribeiro.”

---

## 🛡️ Segurança e Controle de Acesso

A combinação **Nginx + TOC + NMS** fornece:

- 🔐 **Autenticação obrigatória**
- 🧩 **Validação de permissão por modelo (14B, 32B, embeddings)**
- 🔍 **Auditoria centralizada**
- 🧱 **Isolamento entre instâncias**
- ⚙️ **Consulta dinâmica de permissões antes de rotear ao Ollama**

Isso permite que cada chamada ao modelo seja controlada, rastreável e alinhada com políticas corporativas.

> Observação: A configuração do Nginx fica no servidor, em `/etc/nginx/sites-available/billumy` (ou similar), e não dentro do container.

---

## 🏗️ Estrutura do Projeto

```
/
├─ Modelfile-qwen14b      # Modelo Qwen 14B customizado
├─ Modelfile-qwen32b      # Modelo Qwen 32B customizado
├─ Modelfile-qwenMaestro  # Modelo classificador de complexidade
├─ entrypoint.sh          # Script de inicialização automática
├─ Dockerfile             # Imagem Docker do Ollama
├─ docker-compose.yml     # Orquestração do ambiente
└─ README.md              # Documentação do projeto
```

---

## 🔧 Como funciona a inicialização

O script `entrypoint.sh`:

1. Sobe o servidor Ollama
2. Aguarda ele ficar disponível
3. Cria automaticamente:
   - `billumy-qwen14b` (a partir do Modelfile-qwen14b)
   - `billumy-qwen32b` (a partir do Modelfile-qwen32b)
   - `billumy-maestro` (a partir do Modelfile-qwenMaestro)
4. Puxa o modelo de embeddings na primeira execução
5. Acessos HTTP passam pelo **Nginx configurado no servidor**, que valida o TOC antes de rotear ao Ollama

> **Nota importante**: Os Modelfiles usam o comando `SYSTEM` (não `PARAMETER system`) para definir o prompt do sistema, conforme especificação do Ollama.

---

## 🧪 Exemplos de Uso

### Chat com o modelo 14B

```bash
curl https://billumy.a6n.tech/api/chat -H "Authorization: Bearer <TOC>" -d '{
  "model": "billumy-qwen14b",
  "messages": [{"role": "user", "content": "Olá, Billumy!"}]
}'
```

### Classificação de complexidade com Maestro

```bash
curl https://billumy.a6n.tech/api/chat -H "Authorization: Bearer <TOC>" -d '{
  "model": "billumy-maestro",
  "messages": [{"role": "user", "content": "Qual é a capital do Brasil?"}]
}'
```

### Geração de Embeddings

```bash
curl https://billumy.a6n.tech/api/embed -H "Authorization: Bearer <TOC>" -d '{
  "model": "mxbai-embed-large",
  "input": "Texto para embutir"
}'
```

(Nginx valida o TOC antes da requisição chegar ao Ollama)

---

## 📦 Modelos Utilizados

### 🧩 billumy-qwen14b

Baseado no **Qwen2.5 14B**, balanceado entre velocidade e qualidade. Ideal para consultas rápidas e análise de dados.

### 🧩 billumy-qwen32b

Baseado no **Qwen2.5 32B**, ideal para raciocínio complexo e respostas longas e detalhadas.

### 🎯 billumy-maestro

Baseado no **Qwen2.5 1.5B**, classificador especializado que identifica a complexidade de perguntas (simples, média ou profunda) para roteamento inteligente.

### 🔎 mxbai-embed-large

Modelo de embeddings de alta performance para uso em pipelines RAG e buscas semânticas.

---

## 🛠️ Customização

- **Temperatura**
- **Contexto máximo**
- **Prompt do sistema Billumy**
- **Regras de acesso no NMS**
- **Interceptação e roteamento via Nginx no servidor**

---

## 📚 Tecnologias Empregadas

- **Ollama** – Servidor local de LLMs
- **Qwen2.5** – Base dos modelos de linguagem
- **mxbai-embed-large** – Embeddings otimizados
- **Nginx (servidor)** – Proxy reverso + camada de segurança
- **NMS (Nubo Management System)** – Autorização corporativa
- **Docker** – Empacotamento do ambiente
- **Shell Script** – Automação do bootstrap

---

## 📄 Licença

MIT. Livre para usar, modificar e contribuir.
