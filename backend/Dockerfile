FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir poetry==1.8.5

COPY pyproject.toml poetry.lock* poetry.toml* ./
RUN poetry install --no-root --no-interaction --no-ansi

COPY . .

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser \
    && chown -R appuser:appgroup /app
USER appuser

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "core.server:app", "--host", "0.0.0.0", "--port", "8000"]
