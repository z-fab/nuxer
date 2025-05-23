# Estágio de build
FROM python:3.12-alpine AS builder

ENV TZ=America/Sao_Paulo

# Instalar dependências de compilação necessárias
RUN apk add --no-cache gcc musl-dev tzdata \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone

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
RUN apk add --no-cache tzdata py3-pillow
ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

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

COPY _back/alembic.ini /app/alembic.ini
COPY _back/migrations /app/migrations

COPY docker/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Configurar permissões
RUN chown -R appuser:appgroup /app

# Mudar para o usuário não-root
USER appuser


ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python", "main.py"]
