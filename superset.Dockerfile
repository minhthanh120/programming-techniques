FROM apache/superset:latest

USER root

# Cài uv (vì image không có sẵn pip lẫn uv trong PATH)
RUN pip3 install uv 2>/dev/null || \
    (apt-get update && apt-get install -y curl && curl -LsSf https://astral.sh/uv/install.sh | sh)

ENV PATH="/root/.local/bin:${PATH}"

RUN uv pip install --python /app/.venv/bin/python "trino[sqlalchemy]"

RUN /app/.venv/bin/python -c "from sqlalchemy.dialects import registry; registry.load('trino'); print('Trino dialect loaded OK')"

USER superset