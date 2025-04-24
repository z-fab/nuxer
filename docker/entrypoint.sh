#!/bin/sh
set -e

# Só roda migrações se a variável RUN_MIGRATIONS estiver como "true"
if [ "$RUN_MIGRATIONS" = "true" ]; then
  echo "==> Aplicando migrações Alembic"
  alembic upgrade head
  echo "==> Migrações Alembic aplicadas"
  # Se o comando falhar, não executa o próximo comando
  if [ $? -ne 0 ]; then
    echo "==> Falha ao aplicar migrações Alembic"
    exit 1
  fi
else
  echo "==> Pulando migrações Alembic"
fi

# Em seguida, sempre executa o comando passado (python main.py, etc)
exec "$@"