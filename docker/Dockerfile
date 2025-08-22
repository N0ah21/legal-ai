FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["bash", "-c", "python -m app.build_index && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
