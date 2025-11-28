FROM python:3.10-slim

WORKDIR /app

COPY app.py .

RUN pip install sqlite3-binary --no-cache-dir || true

CMD ["python", "app.py"]
