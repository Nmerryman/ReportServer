FROM python:3.11-slim

RUN pip install --upgrade pip && pip install --no-cache-dir fastapi uvicorn watchfiles python-multipart

WORKDIR /app

# COPY main.py .

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]