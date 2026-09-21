from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import fakeredis

app = FastAPI(
    title="Koruja - Financial API & Rate Limiter",
    description="API Financeira de Cotações com limitação de taxa em tempo real.",
    version="1.0.0"
)

# Servidor Redis simulado em memória
redis_client = fakeredis.FakeStrictRedis(decode_responses=True)

# Definição dos limites de requisições por minuto
LIMIT_ANONYMOUS = 5      # Utilizadores sem chave (por IP)
LIMIT_AUTHENTICATED = 20 # Utilizadores com chave de API

# Chaves de API simuladas para testes
VALID_API_KEYS = {"koruja-secret-key-123", "koruja-premium-key-999"}


@app.middleware("http")
async def rate_limiter_middleware(request: Request, call_next):
    # Ignores rotas de documentação para não gastar a cota nos testes visuais
    if request.url.path in ["/docs", "/openapi.json", "/favicon.ico"]:
        return await call_next(request)

    # 1. Identifica o cliente (por API Key no cabeçalho ou por IP)
    api_key = request.headers.get("X-API-Key")
    
    if api_key in VALID_API_KEYS:
        identifier = f"user:{api_key}"
        limit = LIMIT_AUTHENTICATED
    else:
        identifier = f"ip:{request.client.host}"
        limit = LIMIT_ANONYMOUS

    redis_key = f"koruja:rate_limit:{identifier}"

    # 2. Incrementa o contador no Redis simulado
    requests_count = redis_client.incr(redis_key)

    if requests_count == 1:
        redis_client.expire(redis_key, 60)

    ttl = redis_client.ttl(redis_key)

    # 3. Retorna a resposta HTTP 429 diretamente caso o limite seja excedido
    if requests_count > limit:
        return JSONResponse(
            status_code=429,
            content={
                "erro": "Limite de requisições excedido (Rate Limit Exceeded)",
                "mensagem": f"Atingiu o limite de {limit} requisições por minuto.",
                "tente_novamente_em_segundos": ttl
            },
            headers={
                "X-RateLimit-Limit": str(limit),
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset-Seconds": str(ttl)
            }
        )

    # 4. Processa a requisição e gera a resposta da API
    response = await call_next(request)

    # 5. Adiciona cabeçalhos informativos na resposta HTTP
    response.headers["X-RateLimit-Limit"] = str(limit)
    response.headers["X-RateLimit-Remaining"] = str(max(0, limit - requests_count))
    response.headers["X-RateLimit-Reset-Seconds"] = str(ttl)

    return response


# --- ROTAS FINANCEIRAS DA API KORUJA ---

@app.get("/")
async def root():
    return {
        "sistema": "Koruja Financial API",
        "status": "Operacional",
        "documentacao": "/docs"
    }


@app.get("/cotacao/{moeda}")
async def obter_cotacao(moeda: str):
    cotacoes = {
        "USD-BRL": {"par": "USD/BRL", "nome": "Dólar Comercial", "valor": 5.25},
        "EUR-BRL": {"par": "EUR/BRL", "nome": "Euro", "valor": 5.70},
        "BTC-BRL": {"par": "BTC/BRL", "nome": "Bitcoin", "valor": 345000.00}
    }

    dados = cotacoes.get(moeda.upper())
    if not dados:
        return JSONResponse(
            status_code=404, 
            content={"status": "erro", "mensagem": "Moeda não encontrada no Koruja."}
        )

    return {"status": "sucesso", "dados": dados}