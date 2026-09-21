
<p align="center">
  <img src="logo.svg" alt="Koruja Logo" width="160" height="160">
</p>



#  Koruja - Financial API & Rate Limiting Middleware

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

O **Koruja** é uma API de serviços financeiros desenvolvida com FastAPI que inclui uma camada personalizada de Middleware de Rate Limiting (Limitação de Taxas) em tempo real, utilizando armazenamento em memória compatível com Redis.

O projeto foi construído para simular problemas reais de arquitetura de alta escala, protegendo infraestruturas contra abuso de requisições, ataques de negação de serviço (DoS) e garantindo a justa distribuição de recursos da API.

---

##  Principais Funcionalidades

- **Limitação Dinâmica por Cliente:** Identificação de tráfego por IP (utilizadores anônimos) e por `X-API-Key` (utilizadores autenticados).
- **Tratamento de Limites Distintos:**
  - **Anônimos:** 5 requisições por minuto.
  - **Autenticados:** 20 requisições por minuto.
- **Cabeçalhos HTTP Informativos:** A API retorna metadados padrão da indústria em cada resposta:
  - `X-RateLimit-Limit`: Limite máximo da janela atual.
  - `X-RateLimit-Remaining`: Requisições restantes na janela.
  - `X-RateLimit-Reset-Seconds`: Tempo restante até o reset da cota.
- **Tratamento de Erros Padronizado:** Resposta `HTTP 429 Too Many Requests` estruturada quando o limite é excedido.
- **Resiliência:** Armazenamento em memória atômico para contagem de tráfego e cálculo de TTL (Time-To-Live).

---

##  Tecnologias Utilizadas

- **Linguagem:** Python 3
- **Framework Web:** FastAPI
- **Servidor ASGI:** Uvicorn
- **Banco em Memória:** Redis / FakeRedis (para testes locais sem dependências externas)

---

##  Como Executar o Projeto Localmente

### Pré-requisitos
- Python 3.10 ou superior instalado.

### Passo a Passo

1. **Clonar o repositório:**
   ```bash
   git clone [https://github.com/teu-usuario/koruja-financial-api.git](https://github.com/teu-usuario/koruja-financial-api.git)
   cd koruja-financial-api


   # Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# instalar dependencias
pip install -r requirements.txt

# iniciar servidor da API
uvicorn Koruja:app --reload

# Aceda a http://localhost:8000/docs no seu navegador para testar as rotas da API em tempo real.
