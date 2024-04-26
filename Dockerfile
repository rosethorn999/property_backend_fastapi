ARG PYENV=python:3.9-slim

# ====================
FROM ${PYENV} AS builder
WORKDIR /code
ENV PATH="/venv/bin:$PATH"
RUN apt-get update && \
    apt-get install -y libpq-dev gcc
RUN python -m venv /venv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ====================
FROM ${PYENV} AS runner
WORKDIR /code
ENV PATH="/venv/bin:$PATH"
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev && \
    rm -rf /var/lib/apt/lists/*
COPY --from=builder /venv /venv
COPY ./app ./app
ENV PORT 8000
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]