FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80"]