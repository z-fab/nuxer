# Estágio de build
FROM python:3.12-alpine AS builder

# Instalar dependências de compilação necessárias
RUN apk add --no-cache gcc musl-dev

# Instalar uv
RUN pip install --no-cache-dir uv

# Copiar apenas o pyproject.toml
WORKDIR /app
COPY _back/pyproject.toml .
COPY _back/.python-version .

# Instalar dependências com uv usando pyproject.toml
RUN uv pip install --system .

# Imagem final
FROM python:3.12-alpine

# Copiar apenas os pacotes Python instalados do estágio de build
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Criar usuário não-root para segurança
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Criar diretório de logs e configurar permissões
RUN mkdir -p /app/logs
RUN chown -R appuser:appgroup /app

# Copiar o código da aplicação
WORKDIR /app
COPY _back/src/ /app/
COPY _back/.env /app/.env

# Configurar permissões
RUN chown -R appuser:appgroup /app

# Mudar para o usuário não-root
USER appuser

# O comando será substituído no docker-compose
CMD ["python", "main.py"]
